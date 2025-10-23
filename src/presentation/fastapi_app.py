"""
FastAPI Application Factory
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.presentation.api.routes import analysis, charts
from src.presentation.api.middleware.cors import configurar_cors

def crear_app() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI
    """
    app = FastAPI(
        title="Dashboard IA Backend",
        description="API para análisis de datos con IA y generación de gráficos",
        version="1.0.0"
    )
    
    # Configurar CORS
    configurar_cors(app)
    
    # Incluir rutas SIN prefijo (legacy/compatibilidad)
    app.include_router(analysis.router, tags=["subida"])
    app.include_router(charts.router, tags=["graficos"])
    
    # Nota: no incluimos aquí el router con prefijo /api/analisis porque el usuario
    # pidió mantener solo los endpoints originales y evitar rutas adicionales.
    
    @app.get("/")
    async def raiz():
        return {"mensaje": "Dashboard IA Backend API", "estado": "ejecutando"}
    
    @app.get("/salud")
    async def verificar_salud():
        return {"estado": "saludable"}
    
    return app