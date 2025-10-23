"""
Dependencias compartidas para la aplicación
"""
from src.infrastructure.persistence.in_memory_storage import AlmacenamientoMemoria
from src.infrastructure.external.groq_client import ClienteGroq
from src.infrastructure.external.openai_client import ClienteOpenAI

# Singleton compartido entre todos los routers
almacenamiento_compartido = AlmacenamientoMemoria()

# Lazy initialization para evitar errores en import time
_cliente_groq = None
_cliente_openai = None

def obtener_cliente_groq() -> ClienteGroq:
    """Obtiene o crea el cliente Groq compartido"""
    global _cliente_groq
    if _cliente_groq is None:
        _cliente_groq = ClienteGroq()
    return _cliente_groq

def obtener_cliente_openai() -> ClienteOpenAI:
    """Obtiene o crea el cliente OpenAI compartido"""
    global _cliente_openai
    if _cliente_openai is None:
        _cliente_openai = ClienteOpenAI()
    return _cliente_openai
