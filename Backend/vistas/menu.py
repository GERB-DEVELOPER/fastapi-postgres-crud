import json
from config.logger import Logger
from modelos.cliente import Cliente
from modelos.producto import Producto
from dao.cliente_dao import ClienteDAO, ClienteNoEncontradoError, RUCDuplicadoError
from dao.producto_dao import ProductoDAO, ProductoNoEncontradoError

def mostrar_menu(cfg):
    print(f"\n{'=' * 45}")
    print(f"  {cfg.nombre} v{cfg.version}")
    print(f"  {cfg.empresa}")
    print(f"{'=' * 45}")
    print("  1. Agregar cliente")
    print("  2. Agregar producto")
    print("  3. Listar todo cliente")
    print("  4. Listar todo producto")
    print("  5. Eliminar cliente")
    print("  6. Eliminar producto")
    print("  7. Actualizar cliente")
    print("  8. Actualizar producto")
    print("  9. Ver clientes en JSON")
    print("  10. Ver productos en JSON")
    print("  11. Ver historial de logs")
    print("  12. Limpiar historial de logs")
    print("  0. Salir")
    print(f"{'=' * 45}")

def agregar_cliente(cdao):
    print("\n--- AGREGAR CLIENTE ---")
    nombre   = input("  Nombre   : ")
    ruc      = input("  RUC      : ")
    email    = input("  Email    : ")
    telefono = input("  Teléfono : ")
    try:
        c = cdao.insertar(Cliente(nombre, ruc, email, telefono))
        print(f"  OK Cliente agregado con ID={c.id}")
    except RUCDuplicadoError as ex:
        print(f"  ERROR: {ex}")

def agregar_producto(pdao):
    print("\n--- AGREGAR PRODUCTO ---")
    nombre = input("  Nombre  : ")
    try:
        precio = float(input("  Precio  : "))
        p = pdao.insertar(Producto(nombre, precio))
        print(f"  OK Producto agregado con ID={p.id}")
    except ValueError:
        print("  ERROR: El precio debe ser un número")

def listar_todocliente(cdao):
    print("\n--- CLIENTES ---")
    clientes = cdao.obtener_todos()
    if clientes:
        for c in clientes: print(f"  {c}")
    else:
        print("  (No hay clientes registrados)")

def listar_todoproducto(pdao):
    print("\n--- PRODUCTOS ---")
    productos = pdao.obtener_todos()
    if productos:
        for p in productos: print(f"  {p}")
    else:
        print("  (No hay productos registrados)")

def eliminar_cliente(cdao):
    print("\n--- ELIMINAR CLIENTE ---")
    try:
        cliente_id = int(input("  ID del cliente a eliminar: "))
        cdao.eliminar(cliente_id)
        print(f"  OK Cliente ID={cliente_id} eliminado")
    except ClienteNoEncontradoError as ex:
        print(f"  ERROR: {ex}")
    except ValueError:
        print("  ERROR: El ID debe ser un número entero")

def eliminar_producto(pdao):
    print("\n--- ELIMINAR PRODUCTO ---")
    try:
        prod_id = int(input("  ID del producto a eliminar: "))
        pdao.eliminar(prod_id)
        print(f"  OK Producto ID={prod_id} eliminado")
    except ProductoNoEncontradoError as ex:
        print(f"  ERROR: {ex}")
    except ValueError:
        print("  ERROR: El ID debe ser un número entero")

def actualizar_cliente(cdao):
    print("\n--- ACTUALIZAR CLIENTE ---")
    try:
        cliente_id = int(input("  ID del cliente a actualizar: "))
        nombre     = input("  Nuevo nombre   (Enter para no cambiar): ").strip()
        email      = input("  Nuevo email    (Enter para no cambiar): ").strip()
        telefono   = input("  Nuevo teléfono (Enter para no cambiar): ").strip()
        c = cdao.actualizar(cliente_id, nombre or None, email or None, telefono or None)
        print(f"  OK Cliente actualizado: {c}")
    except ClienteNoEncontradoError as ex:
        print(f"  ERROR: {ex}")
    except ValueError:
        print("  ERROR: El ID debe ser un número entero")

def actualizar_producto(pdao):
    print("\n--- ACTUALIZAR PRODUCTO ---")
    try:
        prod_id    = int(input("  ID del producto a actualizar: "))
        nombre     = input("  Nuevo nombre  (Enter para no cambiar): ").strip()
        precio_str = input("  Nuevo precio  (Enter para no cambiar): ").strip()
        precio     = float(precio_str) if precio_str else None
        p = pdao.actualizar(prod_id, nombre or None, precio)
        print(f"  OK Producto actualizado: {p}")
    except ProductoNoEncontradoError as ex:
        print(f"  ERROR: {ex}")
    except ValueError:
        print("  ERROR: ID debe ser entero y precio debe ser número")

def ver_clientes_json(cdao):
    print("\n--- CLIENTES EN JSON ---")
    clientes = cdao.obtener_todos()
    if clientes:
        datos = [c.to_dict() for c in clientes]
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    else:
        print("  (No hay clientes registrados)")

def ver_productos_json(pdao):
    print("\n--- PRODUCTOS EN JSON ---")
    productos = pdao.obtener_todos()
    if productos:
        datos = [p.to_dict() for p in productos]
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    else:
        print("  (No hay productos registrados)")
