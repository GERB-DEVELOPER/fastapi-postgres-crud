from fastapi import APIRouter, HTTPException
from dao.producto_dao import ProductoDAO, ProductoNoEncontradoError
from modelos.producto import Producto
from schemas.producto_schema import ProductoCrear, ProductoActualizar, ProductoRespuesta

# ─────────────────────────────────────────────────────────────────────────────
# ROUTER — Productos (semana-14, FastAPI)
# Misma estructura que routers/clientes.py pero para productos.
# Cada método HTTP mapea a una operación CRUD:
#   GET    → Read (leer)
#   POST   → Create (crear)
#   PUT    → Update (actualizar)
#   DELETE → Delete (eliminar)
# ─────────────────────────────────────────────────────────────────────────────
router = APIRouter(prefix="/productos", tags=["Productos"])
dao = ProductoDAO()

# GET /productos/ — devuelve todos los productos ordenados por nombre
@router.get("/", response_model=list[ProductoRespuesta])
def listar_productos():
    return [p.to_dict() for p in dao.obtener_todos()]

# GET /productos/{prod_id} — devuelve un producto por su ID
@router.get("/{prod_id}", response_model=ProductoRespuesta)
def obtener_producto(prod_id: int):
    p = dao.buscar(prod_id)
    if not p:
        raise HTTPException(status_code=404, detail=f"Producto ID={prod_id} no encontrado")
    return p.to_dict()

# POST /productos/ — crea un nuevo producto; responde con 201 Created
@router.post("/", response_model=ProductoRespuesta, status_code=201)
def crear_producto(datos: ProductoCrear):
    # Pydantic ya validó que datos.nombre es str y datos.precio es float.
    p = dao.insertar(Producto(datos.nombre, datos.precio))
    return p.to_dict()

# PUT /productos/{prod_id} — actualiza nombre y/o precio de un producto
@router.put("/{prod_id}", response_model=ProductoRespuesta)
def actualizar_producto(prod_id: int, datos: ProductoActualizar):
    try:
        p = dao.actualizar(prod_id, datos.nombre, datos.precio)
        return p.to_dict()
    except ProductoNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

# DELETE /productos/{prod_id} — elimina un producto
@router.delete("/{prod_id}")
def eliminar_producto(prod_id: int):
    try:
        dao.eliminar(prod_id)
        return {"mensaje": f"Producto ID={prod_id} eliminado"}
    except ProductoNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
