"""
Configuración de CORS para la aplicación
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.config.settings import get_settings

def setup_cors(app: FastAPI) -> None:
    """
    Configura CORS para permitir comunicación con el frontend
    """
    settings = get_settings()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )