"""
Value Objects del dominio
"""
from dataclasses import dataclass
from typing import List, Any
from enum import Enum

class FileType(Enum):
    """Tipos de archivo soportados"""
    CSV = "csv"
    EXCEL = "xlsx"
    JSON = "json"

class ChartType(Enum):
    """Tipos de gráficos"""
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    SCATTER = "scatter"
    AREA = "area"

class AnalysisType(Enum):
    """Tipos de análisis"""
    GENERAL = "general"
    STATISTICAL = "statistical"
    PREDICTIVE = "predictive"

@dataclass(frozen=True)
class FileMetadata:
    """Metadatos de archivo"""
    filename: str
    size: int
    file_type: FileType
    
    def __post_init__(self):
        if self.size <= 0:
            raise ValueError("El tamaño del archivo debe ser mayor a 0")
        if not self.filename:
            raise ValueError("El nombre del archivo no puede estar vacío")

@dataclass(frozen=True)
class ChartConfig:
    """Configuración de gráfico"""
    title: str
    x_label: str
    y_label: str
    color_scheme: str = "default"
    
    def __post_init__(self):
        if not self.title:
            raise ValueError("El título del gráfico es requerido")
        if not self.x_label or not self.y_label:
            raise ValueError("Las etiquetas de los ejes son requeridas")

@dataclass(frozen=True)
class ChartParameters:
    """Parámetros para generación de gráficos"""
    x_axis: str
    y_axis: str
    aggregation: str = "sum"
    
    def __post_init__(self):
        if not self.x_axis or not self.y_axis:
            raise ValueError("Los ejes X e Y son requeridos")
        
        valid_aggregations = ["sum", "count", "avg", "max", "min"]
        if self.aggregation not in valid_aggregations:
            raise ValueError(f"Agregación debe ser una de: {valid_aggregations}")

@dataclass(frozen=True)
class AnalysisRequest:
    """Request para análisis de datos"""
    file_id: str
    analysis_type: str = "general"
    include_charts: bool = True
    
    def __post_init__(self):
        if not self.file_id:
            raise ValueError("El ID del archivo es requerido")
        
        valid_types = ["general", "statistical", "predictive"]
        if self.analysis_type not in valid_types:
            raise ValueError(f"Tipo de análisis debe ser uno de: {valid_types}")