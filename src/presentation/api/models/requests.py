"""
Modelos de datos para requests y responses de la API
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from enum import Enum

class ChartType(str, Enum):
    """Tipos de gráficos disponibles"""
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    SCATTER = "scatter"
    AREA = "area"

class FileUploadRequest(BaseModel):
    """Request para subir archivo"""
    filename: str
    content: str  # Base64 encoded content
    file_type: str

class AnalysisRequest(BaseModel):
    """Request para análisis de archivo"""
    file_path: str
    analysis_type: str = "general"
    include_charts: bool = True

class ChartDataRequest(BaseModel):
    """Request para generar datos de gráfico"""
    data: List[Dict[str, Any]]
    chart_type: ChartType
    x_column: str
    y_column: str
    title: Optional[str] = None
    
class AnalysisResponse(BaseModel):
    """Response del análisis"""
    analysis_id: str
    summary: str
    insights: List[str]
    chart_suggestions: List[Dict[str, Any]]
    status: str

class ChartDataResponse(BaseModel):
    """Response con datos del gráfico"""
    chart_id: str
    chart_type: str
    data: List[Dict[str, Any]]
    config: Dict[str, Any]
    metadata: Dict[str, Any]

class ErrorResponse(BaseModel):
    """Response de error"""
    error: str
    detail: str
    status_code: int