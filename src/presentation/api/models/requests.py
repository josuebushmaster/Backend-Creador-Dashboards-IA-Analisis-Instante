"""
Modelos de datos para requests y responses de la API
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from enum import Enum

class TipoGrafico(str, Enum):
    """Tipos de gráficos disponibles"""
    BARRAS = "barras"
    LINEAS = "lineas"
    PASTEL = "pastel"
    DISPERSION = "dispersion"
    AREA = "area"

class SolicitudSubirArchivo(BaseModel):
    """Request para subir archivo"""
    nombre_archivo: str
    contenido: str  # Base64 encoded content
    tipo_archivo: str

class SolicitudAnalisis(BaseModel):
    """Request para análisis de archivo"""
    ruta_archivo: str
    tipo_analisis: str = "general"
    incluir_graficos: bool = True

class SolicitudDatosGrafico(BaseModel):
    """Request para generar datos de gráfico"""
    datos: List[Dict[str, Any]]
    tipo_grafico: TipoGrafico
    columna_x: str
    columna_y: str
    titulo: Optional[str] = None
    
class RespuestaAnalisis(BaseModel):
    """Response del análisis"""
    id_analisis: str
    resumen: str
    insights: List[str]
    sugerencias_graficos: List[Dict[str, Any]]
    estado: str

class RespuestaDatosGrafico(BaseModel):
    """Response con datos del gráfico"""
    id_grafico: str
    tipo_grafico: str
    datos: List[Dict[str, Any]]
    configuracion: Dict[str, Any]
    metadatos: Dict[str, Any]

class RespuestaError(BaseModel):
    """Response de error"""
    error: str
    detalle: str
    codigo_estado: int