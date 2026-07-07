# ─────────────────────────────────────────────────────────────────────────────
# MODELO — Cliente (semana-14: igual a semanas anteriores)
# ─────────────────────────────────────────────────────────────────────────────
class Cliente:
    def __init__(self, nombre, ruc, email, telefono):
        # El id empieza en None; en semana-14 lo asigna PostgreSQL con SERIAL.
        self.id       = None
        self.nombre   = nombre
        self.ruc      = ruc
        self.email    = email
        self.telefono = telefono

    def __str__(self):
        return f"[{self.id}] {self.nombre} | RUC:{self.ruc} | {self.email} | {self.telefono}"

    # Convierte el objeto a diccionario (necesario para JSON)
    def to_dict(self):
        # FastAPI usa este diccionario para construir la respuesta JSON del endpoint.
        return {
            "id":       self.id,
            "nombre":   self.nombre,
            "ruc":      self.ruc,
            "email":    self.email,
            "telefono": self.telefono,
        }

    # Crea un objeto Cliente desde un diccionario (necesario para cargar JSON)
    @classmethod
    def from_dict(cls, datos):
        c = cls(datos["nombre"], datos["ruc"], datos["email"], datos["telefono"])
        c.id = datos["id"]
        return c
