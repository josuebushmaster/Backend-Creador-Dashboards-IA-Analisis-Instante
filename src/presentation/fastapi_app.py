"""
FastAPI Application Factory
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.presentation.api.routes import analysis, charts
from src.presentation.api.middleware.cors import setup_cors

def create_app() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI
    """
    app = FastAPI(
        title="Dashboard IA Backend",
        description="API para análisis de datos con IA y generación de gráficos",
        version="1.0.0"
    )
    
    # Configurar CORS
    setup_cors(app)
    
    # Incluir rutas
    app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
    app.include_router(charts.router, prefix="/api/charts", tags=["charts"])
    
    # Incluir también las rutas de analysis sin prefijo para compatibilidad
    app.include_router(analysis.router, tags=["upload"])
    
    @app.get("/")
    async def root():
        return {"message": "Dashboard IA Backend API", "status": "running"}
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    return app