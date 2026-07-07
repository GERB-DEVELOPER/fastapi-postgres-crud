from fastapi import APIRouter, HTTPException
from dao.venta_dao import VentaDAO, VentaNoEncontradaError
from dao.producto_dao import ProductoDAO, ProductoNoEncontradoError
from dao.cliente_dao import ClienteDAO, ClienteNoEncontradoError
from modelos.venta import Venta
from schemas.venta_schema import VentaCrear, VentaRespuesta

# ─────────────────────────────────────────────────────────────────────────────
# ROUTER — Ventas (semana-14, FastAPI)
# Las ventas son más complejas porque requieren validar que el cliente
# y el producto existan ANTES de registrar la venta.
# ─────────────────────────────────────────────────────────────────────────────
router = APIRouter(prefix="/ventas", tags=["Ventas"])

# Tres DAOs necesarios para este router: ventas, clientes y productos.
vdao = VentaDAO()
cdao = ClienteDAO()
pdao = ProductoDAO()

# GET /ventas/ — devuelve todas las ventas con nombres de cliente y producto
@router.get("/", response_model=list[VentaRespuesta])
def listar_ventas():
    # obtener_todos() ya devuelve una lista de diccionarios gracias a dict(fila).
    # FastAPI valida cada diccionario contra VentaRespuesta antes de enviarlo.
    return vdao.obtener_todos()

# GET /ventas/{venta_id} — busca una venta específica por su ID
@router.get("/{venta_id}", response_model=VentaRespuesta)
def obtener_venta(venta_id: int):
    v = vdao.buscar_por_id(venta_id)
    if not v:
        raise HTTPException(status_code=404, detail=f"Venta ID={venta_id} no encontrada")
    return v

# GET /ventas/cliente/{cliente_id} — filtra las ventas de un cliente específico
# Nota: esta ruta debe estar ANTES de /{venta_id} para evitar que FastAPI
# interprete "cliente" como un ID numérico.
@router.get("/cliente/{cliente_id}", response_model=list[VentaRespuesta])
def ventas_por_cliente(cliente_id: int):
    # Verificamos que el cliente exista antes de buscar sus ventas.
    c = cdao.buscar_por_id(cliente_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Cliente ID={cliente_id} no encontrado")
    return vdao.buscar_por_cliente(cliente_id)

# POST /ventas/ — registra una nueva venta
@router.post("/", response_model=VentaRespuesta, status_code=201)
def registrar_venta(datos: VentaCrear):
    # Validamos que existan tanto el cliente como el producto antes de insertar.
    c = cdao.buscar_por_id(datos.cliente_id)
    p = pdao.buscar(datos.producto_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Cliente ID={datos.cliente_id} no encontrado")
    if not p:
        raise HTTPException(status_code=404, detail=f"Producto ID={datos.producto_id} no encontrado")
    # Registramos la venta pasando el precio del producto para calcular el total.
    v = vdao.registrar(Venta(datos.cliente_id, datos.producto_id, datos.cantidad), p.precio)
    # Hacemos una segunda consulta para obtener la venta con los nombres del JOIN.
    # Esto asegura que la respuesta incluya "cliente" y "producto" como strings.
    return vdao.buscar_por_id(v.id)
