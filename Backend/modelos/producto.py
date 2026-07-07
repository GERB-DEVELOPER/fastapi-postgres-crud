# ─────────────────────────────────────────────────────────────────────────────
# MODELO — Producto (semana-14: igual a semanas anteriores)
# ─────────────────────────────────────────────────────────────────────────────
class Producto:
    def __init__(self, nombre, precio):
        # El id empieza en None; en semana-14 lo asigna PostgreSQL con SERIAL.
        self.id     = None
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        return f"[{self.id}] {self.nombre} | S/.{self.precio:.2f}"

    # Convierte el objeto a diccionario (necesario para JSON)
    def to_dict(self):
        return {
            "id":     self.id,
            "nombre": self.nombre,
            "precio": self.precio,
        }

    # Crea un objeto Producto desde un diccionario (necesario para cargar JSON)
    @classmethod
    def from_dict(cls, datos):
        p = cls(datos["nombre"], datos["precio"])
        p.id = datos["id"]
        return p
