from pydantic import BaseModel
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# SCHEMAS PYDANTIC — Producto (semana-14)
# Los tres schemas siguen el mismo patrón que ClienteSchema:
# Crear (entrada sin id), Actualizar (campos opcionales), Respuesta (con id).
# ─────────────────────────────────────────────────────────────────────────────

# Lo que el cliente envía al CREAR un producto (POST /productos)
class ProductoCrear(BaseModel):
    nombre: str
    precio: float  # Pydantic convierte automáticamente entero a float si es necesario

# Lo que el cliente envía al ACTUALIZAR un producto (PUT /productos/{id})
class ProductoActualizar(BaseModel):
    # Optional[tipo] = None hace que el campo sea opcional en el JSON de entrada.
    nombre: Optional[str]   = None
    precio: Optional[float] = None

# Lo que la API devuelve en las respuestas
class ProductoRespuesta(BaseModel):
    id:     int
    nombre: str
    precio: float
