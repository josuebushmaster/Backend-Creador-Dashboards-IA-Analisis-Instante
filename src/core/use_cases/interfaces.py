"""
Interfaces para casos de uso
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class FileAnalysisInterface(ABC):
    """Interfaz para análisis de archivos"""
    
    @abstractmethod
    async def process_file(self, filename: str, content: bytes):
        """Procesa archivo subido"""
        pass
    
    @abstractmethod
    async def analyze_file(self, file_path: str, analysis_type: str, include_charts: bool):
        """Analiza archivo"""
        pass

class ChartDataInterface(ABC):
    """Interfaz para datos de gráficos"""
    
    @abstractmethod
    async def generate_chart_data(self, data: List[Dict[str, Any]], chart_type: str, 
                                 x_column: str, y_column: str, title: str = None):
        """Genera datos de gráfico"""
        pass