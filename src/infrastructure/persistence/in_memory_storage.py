"""
Almacenamiento en memoria para desarrollo
"""
from typing import Dict, Any, Optional
import uuid
import pandas as pd
from src.core.domain.entities import FileData, AnalysisResult, ChartData

class InMemoryStorage:
    """Implementación de almacenamiento en memoria"""
    
    def __init__(self):
        self._files: Dict[str, FileData] = {}
        self._dataframes: Dict[str, pd.DataFrame] = {}
        self._analyses: Dict[str, AnalysisResult] = {}
        self._charts: Dict[str, ChartData] = {}
    
    def save_file(self, file_id: str, file_data: FileData) -> str:
        """Guarda archivo en memoria"""
        self._files[file_id] = file_data
        return file_id
    
    def get_file(self, file_id: str) -> Optional[FileData]:
        """Obtiene archivo de memoria"""
        return self._files.get(file_id)
    
    def save_dataframe(self, file_id: str, dataframe: pd.DataFrame) -> None:
        """Guarda DataFrame asociado a un archivo"""
        self._dataframes[file_id] = dataframe
    
    def get_dataframe(self, file_id: str) -> Optional[pd.DataFrame]:
        """Obtiene DataFrame de un archivo"""
        return self._dataframes.get(file_id)
    
    def save_analysis(self, analysis_id: str, analysis: AnalysisResult) -> None:
        """Guarda resultado de análisis"""
        self._analyses[analysis_id] = analysis
    
    def get_analysis(self, analysis_id: str) -> Optional[AnalysisResult]:
        """Obtiene resultado de análisis"""
        return self._analyses.get(analysis_id)
    
    def save_chart(self, chart_id: str, chart_data: ChartData) -> None:
        """Guarda datos de gráfico"""
        self._charts[chart_id] = chart_data
    
    def get_chart(self, chart_id: str) -> Optional[ChartData]:
        """Obtiene datos de gráfico"""
        return self._charts.get(chart_id)
    
    def delete_file(self, file_id: str) -> bool:
        """Elimina archivo y datos asociados de memoria"""
        deleted = False
        
        if file_id in self._files:
            del self._files[file_id]
            deleted = True
        
        if file_id in self._dataframes:
            del self._dataframes[file_id]
        
        return deleted
    
    def list_files(self) -> list:
        """Lista todos los archivos almacenados"""
        return list(self._files.keys())
    
    def clear_all(self) -> None:
        """Limpia todo el almacenamiento"""
        self._files.clear()
        self._dataframes.clear()
        self._analyses.clear()
        self._charts.clear()