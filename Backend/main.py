from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.base_datos import inicializar
from routers import clientes, productos, ventas

# ─────────────────────────────────────────────────────────────────────────────
# APLICACIÓN FASTAPI — semana-14
# FastAPI es un framework web moderno para construir APIs REST en Python.
# Genera automáticamente documentación interactiva en /docs (Swagger UI)
# y /redoc, lo que facilita mucho probar y compartir la API.
# ─────────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Sistema de Gestión POO",
    version="1.0",
    description="API REST para gestión de clientes, productos y ventas",
)

# ─────────────────────────────────────────────────────────────────────────────
# MIDDLEWARE CORS (Cross-Origin Resource Sharing)
# Por defecto, los navegadores bloquean peticiones de JavaScript a un servidor
# en un dominio/puerto diferente al de la página web (política de mismo origen).
# CORS permite configurar excepciones: aquí habilitamos el frontend React
# (que corre en puerto 5173 o 3000) para consumir esta API (puerto 8000).
# ─────────────────────────────────────────────────────────────────────────────
# CORS: permite que React (semana-10-F) consuma esta API
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["http://localhost:5173", "http://localhost:3000"],
    
    allow_origins=["http://localhost:5173", "http://localhost:3000", "https://gestiopro-frontend.onrender.com"],

    allow_methods=["*"],   # permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],   # permite cualquier cabecera HTTP
)

# Crea las tablas en PostgreSQL si no existen, al arrancar la aplicación.
# Es seguro llamarlo siempre gracias a "CREATE TABLE IF NOT EXISTS".
inicializar()  # crea las tablas si no existen

# include_router() registra todos los endpoints de cada router en la app.
# FastAPI concatenará el prefix del router con las rutas individuales:
# /clientes + / = GET /clientes/
# /clientes + /{id} = GET /clientes/{id}
app.include_router(clientes.router)
app.include_router(productos.router)
app.include_router(ventas.router)

# Endpoint raíz — responde a GET /
# Sirve como "health check" para verificar que la API está activa.
@app.get("/")
def inicio():
    return {
        "mensaje": "API Sistema de Gestión POO",
        "version": "1.0",
        "docs":    "/docs",  # la documentación automática de FastAPI
    }
