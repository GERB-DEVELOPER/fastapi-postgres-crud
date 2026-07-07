from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.cliente import Cliente

# ─────────────────────────────────────────────────────────────────────────────
# EXCEPCIONES PERSONALIZADAS
# ─────────────────────────────────────────────────────────────────────────────
class ClienteNoEncontradoError(Exception):
    def __init__(self, cliente_id):
        super().__init__(f"Cliente ID={cliente_id} no encontrado")

class RUCDuplicadoError(Exception):
    def __init__(self, ruc):
        super().__init__(f"RUC '{ruc}' ya registrado")

# ─────────────────────────────────────────────────────────────────────────────
# PATRÓN DAO — ClienteDAO con PostgreSQL (semana-14)
# Diferencias clave respecto a SQLite (semana-13):
#   1. El marcador de posición es %s en lugar de ?
#   2. INSERT usa "RETURNING id" para obtener el id generado sin lastrowid
#   3. La fila ya es un dict real (RealDictCursor), no un sqlite3.Row
# ─────────────────────────────────────────────────────────────────────────────
class ClienteDAO:
    def __init__(self):
        self.__log = Logger()

    def insertar(self, cliente):
        if self.buscar_por_ruc(cliente.ruc):
            self.__log.warning(f"RUC duplicado: {cliente.ruc}")
            raise RUCDuplicadoError(cliente.ruc)
        conn = obtener_conexion()
        cursor = conn.cursor()
        # En PostgreSQL usamos %s como marcador de posición (no ? como en SQLite).
        # RETURNING id hace que PostgreSQL devuelva el id generado por SERIAL,
        # de modo que no necesitamos cursor.lastrowid (que no existe en psycopg2).
        cursor.execute(
            "INSERT INTO clientes (nombre, ruc, email, telefono) VALUES (%s, %s, %s, %s) RETURNING id",
            (cliente.nombre, cliente.ruc, cliente.email, cliente.telefono)
        )
        # fetchone() devuelve un RealDictCursor row; accedemos con clave ["id"].
        cliente.id = cursor.fetchone()["id"]
        conn.commit()
        conn.close()
        self.__log.info(f"Cliente agregado: {cliente.nombre} (ID={cliente.id})")
        return cliente

    def buscar_por_ruc(self, ruc):
        conn = obtener_conexion()
        cursor = conn.cursor()
        # En PostgreSQL, la tupla de un solo elemento también lleva coma: (ruc,)
        cursor.execute("SELECT * FROM clientes WHERE ruc = %s", (ruc,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_cliente(fila) if fila else None

    def buscar_por_id(self, cliente_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id = %s", (cliente_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_cliente(fila) if fila else None

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes ORDER BY nombre")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_cliente(f) for f in filas]

    def actualizar(self, cliente_id, nombre=None, email=None, telefono=None):
        c = self.buscar_por_id(cliente_id)
        if not c:
            self.__log.error(f"Actualizar fallido: Cliente ID={cliente_id} no existe")
            raise ClienteNoEncontradoError(cliente_id)
        nuevo_nombre   = nombre   or c.nombre
        nuevo_email    = email    or c.email
        nuevo_telefono = telefono or c.telefono
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE clientes SET nombre=%s, email=%s, telefono=%s WHERE id=%s",
            (nuevo_nombre, nuevo_email, nuevo_telefono, cliente_id)
        )
        conn.commit()
        conn.close()
        c.nombre   = nuevo_nombre
        c.email    = nuevo_email
        c.telefono = nuevo_telefono
        self.__log.info(f"Cliente actualizado: ID={cliente_id}")
        return c

    def eliminar(self, cliente_id):
        c = self.buscar_por_id(cliente_id)
        if not c:
            self.__log.error(f"Eliminar fallido: Cliente ID={cliente_id} no existe")
            raise ClienteNoEncontradoError(cliente_id)
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
        conn.commit()
        conn.close()
        self.__log.info(f"Cliente eliminado: {c.nombre} (ID={cliente_id})")
        return True

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        # "AS total" nombra la columna; accedemos con ["total"] gracias a RealDictCursor.
        cursor.execute("SELECT COUNT(*) AS total FROM clientes")
        total = cursor.fetchone()["total"]
        conn.close()
        return total

    def __fila_a_cliente(self, fila):
        # Convierte un diccionario (fila de PostgreSQL) en un objeto Cliente.
        c = Cliente(fila["nombre"], fila["ruc"], fila["email"], fila["telefono"])
        c.id = fila["id"]
        return c
