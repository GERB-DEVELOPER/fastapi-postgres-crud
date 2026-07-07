from pydantic import BaseModel
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# SCHEMAS PYDANTIC — Cliente (semana-14)
# Un "schema" define la estructura de los datos que entran y salen de la API.
# Pydantic valida automáticamente que los datos recibidos tengan el tipo correcto;
# si no, FastAPI devuelve un error 422 (Unprocessable Entity) con detalles claros.
# Separar schemas de modelos es buena práctica: el modelo maneja la BD,
# el schema maneja la interfaz HTTP.
# ─────────────────────────────────────────────────────────────────────────────

# Lo que el cliente envía al CREAR un cliente (POST /clientes)
class ClienteCrear(BaseModel):
    # Todos los campos son obligatorios: si falta alguno, Pydantic rechaza la petición.
    nombre:   str
    ruc:      str
    email:    str
    telefono: str

# Lo que el cliente envía al ACTUALIZAR un cliente (PUT /clientes/{id})
class ClienteActualizar(BaseModel):
    # Optional[str] = None significa que el campo puede omitirse en el JSON.
    # Esto permite actualizar sólo los campos que el usuario quiera cambiar
    # (PATCH parcial simulado con PUT).
    nombre:   Optional[str] = None
    email:    Optional[str] = None
    telefono: Optional[str] = None

# Lo que la API devuelve en las respuestas (GET, POST, PUT)
class ClienteRespuesta(BaseModel):
    # Incluye el id porque es un dato que sólo existe después de guardar en BD.
    id:       int
    nombre:   str
    ruc:      str
    email:    str
    telefono: str
