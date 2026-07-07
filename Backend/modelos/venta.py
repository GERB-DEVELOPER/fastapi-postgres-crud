# ─────────────────────────────────────────────────────────────────────────────
# MODELO — Venta (semana-14: igual a semana-13)
# Representa una transacción: qué cliente compró qué producto, en qué cantidad,
# cuándo y por cuánto dinero.  Los campos cliente_id y producto_id son claves
# foráneas que apuntan a sus tablas respectivas en la base de datos.
# ─────────────────────────────────────────────────────────────────────────────
class Venta:
    def __init__(self, cliente_id, producto_id, cantidad):
        self.id          = None    # asignado por PostgreSQL con SERIAL
        self.cliente_id  = cliente_id   # FK → tabla clientes
        self.producto_id = producto_id  # FK → tabla productos
        self.cantidad    = cantidad
        self.fecha       = None    # se asigna en VentaDAO.registrar() con la hora actual
        self.total       = 0.0     # se calcula en VentaDAO: cantidad × precio_producto

    def __str__(self):
        return (f"[{self.id}] Cliente ID={self.cliente_id} | "
                f"Producto ID={self.producto_id} | "
                f"Cant:{self.cantidad} | S/.{self.total:.2f} | {self.fecha}")

    def to_dict(self):
        # FastAPI puede usar este diccionario como respuesta JSON.
        return {
            "id":          self.id,
            "cliente_id":  self.cliente_id,
            "producto_id": self.producto_id,
            "cantidad":    self.cantidad,
            "fecha":       self.fecha,
            "total":       self.total,
        }
