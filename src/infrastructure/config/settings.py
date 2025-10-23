"""
Configuración de la aplicación
"""
import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # API Keys
    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    
    # Modelos IA
    groq_model: str = Field(default="llama-3.1-70b-versatile", alias="GROQ_MODEL")
    openai_model: str = Field(default="gpt-4-turbo-preview", alias="OPENAI_MODEL")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    debug: bool = Field(default=True, alias="DEBUG")
    
    # Environment
    environment: str = Field(default="development", alias="ENVIRONMENT")
    
    # Base de datos
    database_url: str = "sqlite:///./dashboard_ia.db"
    
    # Archivos
    upload_dir: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    
    # CORS
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173,http://localhost:4200",
        alias="CORS_ORIGINS"
    )
    
    @property
    def allowed_origins(self) -> List[str]:
        """Convierte CORS_ORIGINS string a lista"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        populate_by_name = True
        extra = "allow"  # Permite campos adicionales sin error

# Instancia global de configuración
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Obtiene la configuración de la aplicación"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings