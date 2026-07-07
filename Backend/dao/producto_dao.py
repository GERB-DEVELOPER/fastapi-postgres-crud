from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.producto import Producto

# ─────────────────────────────────────────────────────────────────────────────
# EXCEPCIÓN PERSONALIZADA
# ─────────────────────────────────────────────────────────────────────────────
class ProductoNoEncontradoError(Exception):
    def __init__(self, prod_id):
        super().__init__(f"Producto ID={prod_id} no encontrado")

# ─────────────────────────────────────────────────────────────────────────────
# PATRÓN DAO — ProductoDAO con PostgreSQL (semana-14)
# Usa %s como marcador de posición y RETURNING id para obtener el id generado.
# ─────────────────────────────────────────────────────────────────────────────
class ProductoDAO:
    def __init__(self):
        self.__log = Logger()

    def insertar(self, p):
        conn = obtener_conexion()
        cursor = conn.cursor()
        # RETURNING id: PostgreSQL devuelve el id asignado por SERIAL en la misma sentencia.
        cursor.execute(
            "INSERT INTO productos (nombre, precio) VALUES (%s, %s) RETURNING id",
            (p.nombre, p.precio)
        )
        # RealDictCursor permite acceder al resultado como diccionario.
        p.id = cursor.fetchone()["id"]
        conn.commit()
        conn.close()
        self.__log.info(f"Producto agregado: {p.nombre} S/.{p.precio:.2f} (ID={p.id})")
        return p

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos ORDER BY nombre")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_producto(f) for f in filas]

    def buscar(self, prod_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = %s", (prod_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_producto(fila) if fila else None

    def actualizar(self, prod_id, nombre=None, precio=None):
        p = self.buscar(prod_id)
        if not p:
            self.__log.error(f"Actualizar fallido: Producto ID={prod_id} no existe")
            raise ProductoNoEncontradoError(prod_id)
        nuevo_nombre = nombre or p.nombre
        nuevo_precio = precio or p.precio
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE productos SET nombre=%s, precio=%s WHERE id=%s",
            (nuevo_nombre, nuevo_precio, prod_id)
        )
        conn.commit()
        conn.close()
        p.nombre = nuevo_nombre
        p.precio = nuevo_precio
        self.__log.info(f"Producto actualizado: ID={prod_id}")
        return p

    def eliminar(self, prod_id):
        p = self.buscar(prod_id)
        if not p:
            self.__log.error(f"Eliminar fallido: Producto ID={prod_id} no existe")
            raise ProductoNoEncontradoError(prod_id)
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (prod_id,))
        conn.commit()
        conn.close()
        self.__log.info(f"Producto eliminado: {p.nombre} (ID={prod_id})")
        return True

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM productos")
        total = cursor.fetchone()["total"]
        conn.close()
        return total

    def __fila_a_producto(self, fila):
        # Convierte un diccionario (fila de PostgreSQL) en un objeto Producto.
        p = Producto(fila["nombre"], fila["precio"])
        p.id = fila["id"]
        return p
