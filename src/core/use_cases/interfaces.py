"""
Interfaces para casos de uso
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class InterfazAnalisisArchivo(ABC):
    """Interfaz para análisis de archivos"""
    
    @abstractmethod
    async def procesar_archivo(self, nombre_archivo: str, contenido: bytes):
        """Procesa archivo subido"""
        pass
    
    @abstractmethod
    async def analizar_archivo(self, ruta_archivo: str, tipo_analisis: str, incluir_graficos: bool):
        """Analiza archivo"""
        pass

class InterfazDatosGrafico(ABC):
    """Interfaz para datos de gráficos"""
    
    @abstractmethod
    async def generar_datos_grafico(self, datos: List[Dict[str, Any]], tipo_grafico: str, 
                                 columna_x: str, columna_y: str, titulo: str = None):
        """Genera datos de gráfico"""
        pass