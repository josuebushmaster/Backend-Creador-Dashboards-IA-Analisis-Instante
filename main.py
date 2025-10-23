#!/usr/bin/env python3
"""
Dashboard IA - Backend
Aplicación FastAPI para análisis de datos con IA
"""
import uvicorn

def main():
    """Punto de entrada principal de la aplicación"""
    # Configuración para desarrollo
    uvicorn.run(
        "src.presentation.fastapi_app:create_app",
        factory=True,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()