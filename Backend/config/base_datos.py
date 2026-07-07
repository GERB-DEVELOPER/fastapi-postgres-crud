import os
import psycopg2
from psycopg2.extras import RealDictCursor

# ─────────────────────────────────────────────────────────────────────────────
# CONEXIÓN A POSTGRESQL — semana-14
# A diferencia de SQLite (un archivo), PostgreSQL es un servidor de base de datos
# completo que requiere host, puerto, usuario y contraseña.
# psycopg2 es el driver más popular para conectar Python con PostgreSQL.
# ─────────────────────────────────────────────────────────────────────────────

def obtener_conexion():
    conn = psycopg2.connect(
        # os.getenv() lee variables de entorno del sistema operativo.
        # El segundo parámetro es el valor por defecto si la variable no está definida.
        # Usar variables de entorno evita escribir contraseñas directamente en el código.
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "sistema_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "")
    )
    # RealDictCursor hace que cada fila se devuelva como un diccionario real de Python,
    # a diferencia de sqlite3.Row (que también actúa como dict pero no es exactamente uno).
    # Esto permite hacer dict(fila) y retornar las filas directamente a FastAPI.
    conn.cursor_factory = RealDictCursor
    return conn

def inicializar():
    # Crea las tablas si no existen al arrancar la aplicación.
    conn = obtener_conexion()
    cursor = conn.cursor()

    # En PostgreSQL, SERIAL es el equivalente de INTEGER AUTOINCREMENT en SQLite.
    # SERIAL crea una secuencia automática que incrementa el id con cada inserción.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id       SERIAL PRIMARY KEY,
            nombre   TEXT   NOT NULL,
            ruc      TEXT   UNIQUE NOT NULL,
            email    TEXT   NOT NULL,
            telefono TEXT   NOT NULL
        )
    """)

    # NUMERIC(10,2) guarda números decimales con hasta 10 dígitos y exactamente 2 decimales,
    # más preciso que REAL/FLOAT para valores monetarios (evita errores de punto flotante).
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id     SERIAL PRIMARY KEY,
            nombre TEXT          NOT NULL,
            precio NUMERIC(10,2) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id          SERIAL PRIMARY KEY,
            cliente_id  INTEGER       NOT NULL,
            producto_id INTEGER       NOT NULL,
            cantidad    INTEGER       NOT NULL,
            fecha       TEXT          NOT NULL,
            total       NUMERIC(10,2) NOT NULL,
            FOREIGN KEY (cliente_id)  REFERENCES clientes(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    """)

    conn.commit()
    conn.close()
