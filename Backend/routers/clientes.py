from fastapi import APIRouter, HTTPException
from dao.cliente_dao import ClienteDAO, ClienteNoEncontradoError, RUCDuplicadoError
from modelos.cliente import Cliente
from schemas.cliente_schema import ClienteCrear, ClienteActualizar, ClienteRespuesta

# ─────────────────────────────────────────────────────────────────────────────
# ROUTER — Clientes (semana-14, FastAPI)
# Un Router agrupa endpoints relacionados.  Se "incluye" en la app principal
# (main.py) con app.include_router().
# prefix="/clientes" significa que todas las rutas aquí empiezan con /clientes.
# tags=["Clientes"] agrupa estos endpoints en la documentación automática /docs.
# ─────────────────────────────────────────────────────────────────────────────
router = APIRouter(prefix="/clientes", tags=["Clientes"])

# La instancia del DAO se crea a nivel de módulo (fuera de las funciones).
# Esto es equivalente a crear un "repositorio" compartido para todos los endpoints.
dao = ClienteDAO()

# GET /clientes/ — devuelve la lista de todos los clientes
# response_model=list[ClienteRespuesta] le dice a FastAPI qué estructura devolver.
# FastAPI valida automáticamente que el retorno coincida con el schema.
@router.get("/", response_model=list[ClienteRespuesta])
def listar_clientes():
    # to_dict() convierte cada objeto Cliente en un diccionario que Pydantic
    # puede validar y serializar a JSON.
    return [c.to_dict() for c in dao.obtener_todos()]

# GET /clientes/{cliente_id} — busca un cliente por su ID
# {cliente_id} es un parámetro de ruta; FastAPI lo extrae de la URL automáticamente.
@router.get("/{cliente_id}", response_model=ClienteRespuesta)
def obtener_cliente(cliente_id: int):
    c = dao.buscar_por_id(cliente_id)
    if not c:
        # HTTPException envía al cliente un código HTTP + mensaje de error en JSON.
        # 404 = "Not Found": el recurso solicitado no existe.
        raise HTTPException(status_code=404, detail=f"Cliente ID={cliente_id} no encontrado")
    return c.to_dict()

# POST /clientes/ — crea un nuevo cliente
# status_code=201 indica "Created"; por defecto FastAPI devuelve 200 "OK".
@router.post("/", response_model=ClienteRespuesta, status_code=201)
def crear_cliente(datos: ClienteCrear):
    # "datos: ClienteCrear" hace que FastAPI deserialice el JSON del body
    # y valide que tenga los campos correctos antes de llamar a esta función.
    try:
        c = dao.insertar(Cliente(datos.nombre, datos.ruc, datos.email, datos.telefono))
        return c.to_dict()
    except RUCDuplicadoError as ex:
        # 400 = "Bad Request": el cliente envió datos inválidos (RUC ya existe).
        raise HTTPException(status_code=400, detail=str(ex))

# PUT /clientes/{cliente_id} — actualiza los datos de un cliente existente
@router.put("/{cliente_id}", response_model=ClienteRespuesta)
def actualizar_cliente(cliente_id: int, datos: ClienteActualizar):
    try:
        c = dao.actualizar(cliente_id, datos.nombre, datos.email, datos.telefono)
        return c.to_dict()
    except ClienteNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

# DELETE /clientes/{cliente_id} — elimina un cliente
@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int):
    try:
        dao.eliminar(cliente_id)
        # Devolvemos un mensaje de confirmación en lugar de 204 No Content.
        return {"mensaje": f"Cliente ID={cliente_id} eliminado"}
    except ClienteNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
