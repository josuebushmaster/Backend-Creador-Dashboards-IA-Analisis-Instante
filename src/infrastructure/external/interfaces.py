"""
Interfaces para servicios externos
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class AIClientInterface(ABC):
    """Interfaz para clientes de IA"""
    
    @abstractmethod
    async def generar_analisis(self, prompt: str) -> str:
        """Genera análisis basado en prompt"""
        pass
    
    @abstractmethod
    async def generar_sugerencias_grafico(self, contexto_datos: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Genera sugerencias de gráficos"""
        pass

class InterfazAlmacenamiento(ABC):
    """Interfaz para almacenamiento"""
    
    @abstractmethod
    async def guardar_archivo(self, id_archivo: str, contenido: bytes) -> str:
        """Guarda archivo y retorna path"""
        pass
    
    @abstractmethod
    async def obtener_archivo(self, id_archivo: str) -> bytes:
        """Obtiene archivo por ID"""
        pass
    
    @abstractmethod
    async def eliminar_archivo(self, id_archivo: str) -> bool:
        """Elimina archivo"""
        pass