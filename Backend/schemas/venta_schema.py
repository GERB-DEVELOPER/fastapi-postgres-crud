from pydantic import BaseModel

# ─────────────────────────────────────────────────────────────────────────────
# SCHEMAS PYDANTIC — Venta (semana-14)
# Las ventas no tienen schema de "actualizar" porque son inmutables:
# una venta registrada no se modifica, sólo se consulta.
# ─────────────────────────────────────────────────────────────────────────────

# Lo que el cliente envía al registrar una venta (POST /ventas)
class VentaCrear(BaseModel):
    # Solo se necesitan los IDs y la cantidad; el total y la fecha los calcula el DAO.
    cliente_id:  int
    producto_id: int
    cantidad:    int

# Lo que la API devuelve (incluye nombres del JOIN, no solo IDs)
class VentaRespuesta(BaseModel):
    id:          int
    cliente_id:  int
    producto_id: int
    # "cliente" y "producto" son los NOMBRES obtenidos del JOIN en VentaDAO,
    # más útiles para el frontend que los IDs numéricos.
    cliente:     str
    producto:    str
    cantidad:    int
    fecha:       str
    total:       float
