"""
Interfaces para servicios externos
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class AIClientInterface(ABC):
    """Interfaz para clientes de IA"""
    
    @abstractmethod
    async def generate_analysis(self, prompt: str) -> str:
        """Genera análisis basado en prompt"""
        pass
    
    @abstractmethod
    async def generate_chart_suggestions(self, data_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Genera sugerencias de gráficos"""
        pass

class StorageInterface(ABC):
    """Interfaz para almacenamiento"""
    
    @abstractmethod
    async def save_file(self, file_id: str, content: bytes) -> str:
        """Guarda archivo y retorna path"""
        pass
    
    @abstractmethod
    async def get_file(self, file_id: str) -> bytes:
        """Obtiene archivo por ID"""
        pass
    
    @abstractmethod
    async def delete_file(self, file_id: str) -> bool:
        """Elimina archivo"""
        pass