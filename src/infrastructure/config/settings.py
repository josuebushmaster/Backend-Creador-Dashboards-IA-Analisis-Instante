"""
Configuración de la aplicación
"""
import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field

class Configuracion(BaseSettings):
    """Configuración de la aplicación"""
    
    # API Keys
    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    
    # Modelos IA
    groq_model: str = Field(default="llama-3.3-70b-versatile", alias="GROQ_MODEL")
    openai_model: str = Field(default="gpt-4-turbo-preview", alias="OPENAI_MODEL")
    
    # Configuración del servidor
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    debug: bool = Field(default=True, alias="DEBUG")
    
    # Entorno
    environment: str = Field(default="development", alias="ENVIRONMENT")
    
    # Base de datos
    url_base_datos: str = "sqlite:///./dashboard_ia.db"
    
    # Archivos
    directorio_subidas: str = "uploads"
    tamano_maximo_archivo: int = 10 * 1024 * 1024  # 10MB
    
    # CORS
    origenes_cors: str = Field(
        default="http://localhost:3000,http://localhost:5173,http://localhost:4200",
        alias="CORS_ORIGINS"
    )
    
    @property
    def origenes_permitidos(self) -> List[str]:
        """Convierte CORS_ORIGINS string a lista"""
        return [origen.strip() for origen in self.origenes_cors.split(",")]
    
    # Logging
    nivel_log: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        populate_by_name = True
        extra = "allow"  # Permite campos adicionales sin error

# Instancia global de configuración
_configuracion: Optional[Configuracion] = None

def obtener_configuracion() -> Configuracion:
    """Obtiene la configuración de la aplicación"""
    global _configuracion
    if _configuracion is None:
        _configuracion = Configuracion()
    return _configuracion