"""
Repository Pattern para abstraer persistencia
"""
from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd
from src.core.domain.entities import DatosArchivo, ResultadoAnalisis

class RepositorioArchivos(ABC):
    """Repositorio para archivos"""
    
    @abstractmethod
    async def guardar(self, datos_archivo: DatosArchivo) -> str:
        pass
    
    @abstractmethod
    async def encontrar_por_id(self, id_archivo: str) -> Optional[DatosArchivo]:
        pass
    
    @abstractmethod
    async def eliminar(self, id_archivo: str) -> bool:
        pass

class RepositorioDataFrame(ABC):
    """Repositorio para DataFrames"""
    
    @abstractmethod
    async def guardar(self, id_archivo: str, dataframe: pd.DataFrame) -> None:
        pass
    
    @abstractmethod
    async def encontrar_por_id_archivo(self, id_archivo: str) -> Optional[pd.DataFrame]:
        pass

class RepositorioAnalisis(ABC):
    """Repositorio para análisis"""
    
    @abstractmethod
    async def guardar(self, analisis: ResultadoAnalisis) -> str:
        pass
    
    @abstractmethod
    async def encontrar_por_id(self, id_analisis: str) -> Optional[ResultadoAnalisis]:
        pass