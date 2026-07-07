from datetime import datetime
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.venta import Venta

# ─────────────────────────────────────────────────────────────────────────────
# EXCEPCIÓN PERSONALIZADA
# ─────────────────────────────────────────────────────────────────────────────
class VentaNoEncontradaError(Exception):
    def __init__(self, venta_id):
        super().__init__(f"Venta ID={venta_id} no encontrada")

# ─────────────────────────────────────────────────────────────────────────────
# PATRÓN DAO — VentaDAO con PostgreSQL (semana-14)
# Diferencias respecto a SQLite:
#   - Usa %s en lugar de ?
#   - Usa RETURNING id en lugar de cursor.lastrowid
#   - Convierte filas con dict(fila) porque RealDictCursor ya devuelve dicts reales
# ─────────────────────────────────────────────────────────────────────────────
class VentaDAO:
    def __init__(self):
        self.__log = Logger()

    def registrar(self, venta, precio_producto):
        # Calculamos el total multiplicando cantidad × precio.
        # round(..., 2) evita errores de precisión con números de punto flotante.
        venta.total = round(venta.cantidad * precio_producto, 2)
        venta.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = obtener_conexion()
        cursor = conn.cursor()
        # RETURNING id devuelve el id generado por SERIAL inmediatamente.
        cursor.execute(
            "INSERT INTO ventas (cliente_id, producto_id, cantidad, fecha, total) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (venta.cliente_id, venta.producto_id, venta.cantidad, venta.fecha, venta.total)
        )
        venta.id = cursor.fetchone()["id"]
        conn.commit()
        conn.close()
        self.__log.info(f"Venta registrada: ID={venta.id} Total=S/.{venta.total:.2f}")
        return venta

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        # JOIN: combina datos de tres tablas en una sola consulta.
        # "v.cliente_id" y "v.producto_id" se incluyen en el SELECT para que
        # FastAPI pueda construir el schema VentaRespuesta completo.
        cursor.execute("""
            SELECT v.id, c.nombre AS cliente, p.nombre AS producto,
                   v.cantidad, v.fecha, v.total,
                   v.cliente_id, v.producto_id
            FROM ventas v
            JOIN clientes  c ON v.cliente_id  = c.id
            JOIN productos p ON v.producto_id = p.id
            ORDER BY v.fecha DESC
        """)
        filas = cursor.fetchall()
        conn.close()
        # dict(f) convierte cada RealDictRow en un diccionario estándar de Python,
        # lo que permite que FastAPI lo serialice directamente a JSON.
        return [dict(f) for f in filas]

    def buscar_por_id(self, venta_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.id, c.nombre AS cliente, p.nombre AS producto,
                   v.cantidad, v.fecha, v.total,
                   v.cliente_id, v.producto_id
            FROM ventas v
            JOIN clientes  c ON v.cliente_id  = c.id
            JOIN productos p ON v.producto_id = p.id
            WHERE v.id = %s
        """, (venta_id,))
        fila = cursor.fetchone()
        conn.close()
        # dict(fila) convierte el resultado a diccionario para que FastAPI lo serialice.
        return dict(fila) if fila else None

    def buscar_por_cliente(self, cliente_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.id, c.nombre AS cliente, p.nombre AS producto,
                   v.cantidad, v.fecha, v.total,
                   v.cliente_id, v.producto_id
            FROM ventas v
            JOIN clientes  c ON v.cliente_id  = c.id
            JOIN productos p ON v.producto_id = p.id
            WHERE v.cliente_id = %s
            ORDER BY v.fecha DESC
        """, (cliente_id,))
        filas = cursor.fetchall()
        conn.close()
        return [dict(f) for f in filas]

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM ventas")
        total = cursor.fetchone()["total"]
        conn.close()
        return total
