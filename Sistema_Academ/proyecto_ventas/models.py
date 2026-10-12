from datetime import date


# =====================================================================
# CLASE BASE: lo que los tres modelos comparten
# =====================================================================
class ModeloBase:
    """Padre de todos los modelos. Guarda el id y define el comportamiento común."""

    def __init__(self, id_registro):
        self.id = int(id_registro)

    # ---- ÚNICO MÉTODO DE CLASE DEL PROYECTO ----
    @classmethod
    def desde_diccionario(cls, datos):
        """Diccionario -> objeto. Escrito UNA vez y usado por los tres modelos.
        cls es la clase que llamó: Cliente, Producto o Venta."""
        datos = dict(datos)                 # copia, para no tocar el original
        id_registro = datos.pop("id")
        return cls(id_registro, **datos)

    def a_diccionario(self):
        return {"id": self.id}

    def etiqueta(self):
        # POLIMORFISMO: cada hijo la reescribe a su manera
        return f"registro {self.id}"

    def __str__(self):
        # print(objeto) llama a etiqueta(): cada modelo se imprime distinto
        return f"[{self.id}] {self.etiqueta()}"


# =====================================================================
# HERENCIA: Persona es la base de Cliente
# =====================================================================
class Persona(ModeloBase):
    def __init__(self, id_registro, nombre, apellido, email):
        super().__init__(id_registro)
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["apellido"] = self.apellido
        datos["email"] = self.email
        return datos

    def etiqueta(self):
        return self.nombre_completo()


class Cliente(Persona):
    """Cliente ES UNA Persona, con teléfono y ciudad."""

    def __init__(self, id_registro, nombre, apellido, email, telefono="", ciudad=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.telefono = telefono
        self.ciudad = ciudad

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["telefono"] = self.telefono
        datos["ciudad"] = self.ciudad
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · {self.email} · {self.ciudad or 'sin ciudad'}"


# =====================================================================
# ÚNICA CLASE CON ATRIBUTOS Y MÉTODOS ESTÁTICOS
# =====================================================================
class Producto(ModeloBase):
    # ATRIBUTOS ESTÁTICOS (de clase): una sola vez, no por objeto
    STOCK_MINIMO = 5
    IVA = 0.15
    total_creados = 0

    def __init__(self, id_registro, nombre, precio, stock=0):
        super().__init__(id_registro)
        self.nombre = nombre
        self.precio = float(precio)
        self.stock = int(stock)
        Producto.total_creados += 1        # en la CLASE, no en self

    # MÉTODOS ESTÁTICOS: no usan self ni cls
    @staticmethod
    def es_precio_valido(valor):
        try:
            return float(valor) > 0
        except (TypeError, ValueError):
            return False

    @staticmethod
    def con_iva(monto):
        return round(monto * (1 + Producto.IVA), 2)

    # MÉTODOS DE INSTANCIA
    def stock_bajo(self):
        return self.stock <= Producto.STOCK_MINIMO

    def hay_stock(self, cantidad):
        return 0 < cantidad <= self.stock

    def descontar_stock(self, cantidad):
        self.stock -= cantidad

    def devolver_stock(self, cantidad):
        self.stock += cantidad

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["precio"] = self.precio
        datos["stock"] = self.stock
        return datos

    def etiqueta(self):
        alerta = " ⚠ stock bajo" if self.stock_bajo() else ""
        return f"{self.nombre} · ${self.precio:.2f} · stock {self.stock}{alerta}"


class Venta(ModeloBase):
    """Venta simple: un cliente, un producto, una cantidad."""

    def __init__(self, id_registro, cliente_id, producto_id, cantidad,
                 precio_unitario, fecha=""):
        super().__init__(id_registro)
        self.cliente_id = int(cliente_id)
        self.producto_id = int(producto_id)
        self.cantidad = int(cantidad)
        self.precio_unitario = float(precio_unitario)   # foto del precio del momento
        self.fecha = fecha or date.today().isoformat()

    def calcular_total(self):
        # Se calcula cada vez; NO se guarda, para que nunca quede desactualizado
        return round(self.cantidad * self.precio_unitario, 2)

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["cliente_id"] = self.cliente_id
        datos["producto_id"] = self.producto_id
        datos["cantidad"] = self.cantidad
        datos["precio_unitario"] = self.precio_unitario
        datos["fecha"] = self.fecha
        return datos

    def etiqueta(self):
        return (f"{self.fecha} · cliente {self.cliente_id} · "
                f"{self.cantidad} x producto {self.producto_id} "
                f"= ${self.calcular_total():.2f}")
