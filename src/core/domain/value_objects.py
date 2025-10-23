"""
Value Objects del dominio
"""
from dataclasses import dataclass
from typing import List, Any
from enum import Enum

class TipoArchivo(Enum):
    """Tipos de archivo soportados"""
    CSV = "csv"
    EXCEL = "xlsx"
    JSON = "json"

class TipoGrafico(Enum):
    """Tipos de gráficos"""
    BARRAS = "bar"
    LINEAS = "line"
    PASTEL = "pie"
    DISPERSION = "scatter"
    AREA = "area"

class TipoAnalisis(Enum):
    """Tipos de análisis"""
    GENERAL = "general"
    ESTADISTICO = "statistical"
    PREDICTIVO = "predictive"

@dataclass(frozen=True)
class MetadatosArchivo:
    """Metadatos de archivo"""
    nombre_archivo: str
    tamano: int
    tipo_archivo: TipoArchivo
    
    def __post_init__(self):
        if self.tamano <= 0:
            raise ValueError("El tamaño del archivo debe ser mayor a 0")
        if not self.nombre_archivo:
            raise ValueError("El nombre del archivo no puede estar vacío")

@dataclass(frozen=True)
class ConfiguracionGrafico:
    """Configuración de gráfico"""
    titulo: str
    etiqueta_x: str
    etiqueta_y: str
    esquema_color: str = "default"
    
    def __post_init__(self):
        if not self.titulo:
            raise ValueError("El título del gráfico es requerido")
        if not self.etiqueta_x or not self.etiqueta_y:
            raise ValueError("Las etiquetas de los ejes son requeridas")

@dataclass(frozen=True)
class ParametrosGrafico:
    """Parámetros para generación de gráficos"""
    eje_x: str
    eje_y: str
    agregacion: str = "sum"
    
    def __post_init__(self):
        if not self.eje_x or not self.eje_y:
            raise ValueError("Los ejes X e Y son requeridos")
        
        agregaciones_validas = ["sum", "count", "avg", "max", "min"]
        if self.agregacion not in agregaciones_validas:
            raise ValueError(f"Agregación debe ser una de: {agregaciones_validas}")

@dataclass(frozen=True)
class SolicitudAnalisis:
    """Solicitud para análisis de datos"""
    id_archivo: str
    tipo_analisis: str = "general"
    incluir_graficos: bool = True
    
    def __post_init__(self):
        if not self.id_archivo:
            raise ValueError("El ID del archivo es requerido")
        
        tipos_validos = ["general", "statistical", "predictive"]
        if self.tipo_analisis not in tipos_validos:
            raise ValueError(f"Tipo de análisis debe ser uno de: {tipos_validos}")