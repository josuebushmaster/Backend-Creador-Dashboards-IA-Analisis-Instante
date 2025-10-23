"""
Repository Pattern para abstraer persistencia
"""
from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd
from src.core.domain.entities import FileData, AnalysisResult

class FileRepository(ABC):
    """Repositorio para archivos"""
    
    @abstractmethod
    async def save(self, file_data: FileData) -> str:
        pass
    
    @abstractmethod
    async def find_by_id(self, file_id: str) -> Optional[FileData]:
        pass
    
    @abstractmethod
    async def delete(self, file_id: str) -> bool:
        pass

class DataFrameRepository(ABC):
    """Repositorio para DataFrames"""
    
    @abstractmethod
    async def save(self, file_id: str, dataframe: pd.DataFrame) -> None:
        pass
    
    @abstractmethod
    async def find_by_file_id(self, file_id: str) -> Optional[pd.DataFrame]:
        pass

class AnalysisRepository(ABC):
    """Repositorio para análisis"""
    
    @abstractmethod
    async def save(self, analysis: AnalysisResult) -> str:
        pass
    
    @abstractmethod
    async def find_by_id(self, analysis_id: str) -> Optional[AnalysisResult]:
        pass