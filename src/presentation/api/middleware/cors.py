"""
Configuración de CORS para la aplicación
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.config.settings import obtener_configuracion

def configurar_cors(app: FastAPI) -> None:
    """
    Configura CORS para permitir comunicación con el frontend
    """
    configuracion = obtener_configuracion()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=configuracion.origenes_permitidos,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )