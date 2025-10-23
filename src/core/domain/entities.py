"""
Entidades de dominio para el dashboard IA
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

@dataclass
class DatosArchivo:
    """Entidad para datos de archivo"""
    id_archivo: str
    nombre_archivo: str
    tipo_archivo: str
    contenido: bytes
    subido_en: datetime
    tamano: int
    
    @classmethod
    def crear(cls, nombre_archivo: str, contenido: bytes, tipo_archivo: str) -> 'DatosArchivo':
        return cls(
            id_archivo=str(uuid.uuid4()),
            nombre_archivo=nombre_archivo,
            tipo_archivo=tipo_archivo,
            contenido=contenido,
            subido_en=datetime.now(),
            tamano=len(contenido)
        )

@dataclass
class ResultadoAnalisis:
    """Entidad para resultado de análisis"""
    id_analisis: str
    id_archivo: str
    resumen: str
    insights: List[str]
    sugerencias_graficos: List[Dict[str, Any]]
    creado_en: datetime
    estado: str
    
    @classmethod
    def crear(cls, id_archivo: str, resumen: str, insights: List[str], 
               sugerencias_graficos: List[Dict[str, Any]]) -> 'ResultadoAnalisis':
        return cls(
            id_analisis=str(uuid.uuid4()),
            id_archivo=id_archivo,
            resumen=resumen,
            insights=insights,
            sugerencias_graficos=sugerencias_graficos,
            creado_en=datetime.now(),
            estado="completado"
        )

@dataclass
class DatosGrafico:
    """Entidad para datos de gráfico"""
    id_grafico: str
    tipo_grafico: str
    datos: List[Dict[str, Any]]
    configuracion: Dict[str, Any]
    metadatos: Dict[str, Any]
    creado_en: datetime
    
    @classmethod
    def crear(cls, tipo_grafico: str, datos: List[Dict[str, Any]], 
               configuracion: Dict[str, Any], metadatos: Dict[str, Any]) -> 'DatosGrafico':
        return cls(
            id_grafico=str(uuid.uuid4()),
            tipo_grafico=tipo_grafico,
            datos=datos,
            configuracion=configuracion,
            metadatos=metadatos,
            creado_en=datetime.now()
        )