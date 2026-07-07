import json
from modelos.cliente import Cliente
from modelos.producto import Producto

# Nota: en semana-14 la persistencia principal es PostgreSQL.
# Este módulo se mantiene por referencia histórica de semanas anteriores.
ARCHIVO_CLIENTES  = "datos_clientes.json"
ARCHIVO_PRODUCTOS = "datos_productos.json"

def guardar_clientes(cdao):
    datos = [c.to_dict() for c in cdao.obtener_todos()]
    with open(ARCHIVO_CLIENTES, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(f"  OK Clientes guardados en '{ARCHIVO_CLIENTES}'")

def cargar_clientes(cdao):
    try:
        with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as f:
            datos = json.load(f)
        for d in datos:
            cliente = Cliente.from_dict(d)
            # Acceso al atributo privado mediante name mangling.
            cdao._ClienteDAO__bd.append(cliente)
            if cliente.id >= cdao._ClienteDAO__cid:
                cdao._ClienteDAO__cid = cliente.id + 1
        print(f"  OK {len(datos)} clientes cargados desde '{ARCHIVO_CLIENTES}'")
    except FileNotFoundError:
        print(f"  AVISO: No existe '{ARCHIVO_CLIENTES}', se empieza desde cero")

def guardar_productos(pdao):
    datos = [p.to_dict() for p in pdao.obtener_todos()]
    with open(ARCHIVO_PRODUCTOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(f"  OK Productos guardados en '{ARCHIVO_PRODUCTOS}'")

def cargar_productos(pdao):
    try:
        with open(ARCHIVO_PRODUCTOS, "r", encoding="utf-8") as f:
            datos = json.load(f)
        for d in datos:
            producto = Producto.from_dict(d)
            pdao._ProductoDAO__bd.append(producto)
            if producto.id >= pdao._ProductoDAO__cid:
                pdao._ProductoDAO__cid = producto.id + 1
        print(f"  OK {len(datos)} productos cargados desde '{ARCHIVO_PRODUCTOS}'")
    except FileNotFoundError:
        print(f"  AVISO: No existe '{ARCHIVO_PRODUCTOS}', se empieza desde cero")
