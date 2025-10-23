"""
Sugerencia: Container de Dependencias
"""
from typing import Protocol
from src.core.use_cases.file_analysis import CasoUsoAnalisisArchivo
from src.infrastructure.external.groq_client import ClienteGroq
from src.infrastructure.persistence.in_memory_storage import AlmacenamientoMemoria

class Contenedor:
    """Container de dependencias siguiendo principios SOLID"""
    
    def __init__(self):
        # Infraestructura
        self._almacenamiento = AlmacenamientoMemoria()
        self._cliente_ia = ClienteGroq()
        
        # Casos de uso
        self._caso_uso_analisis_archivo = None
    
    @property
    def caso_uso_analisis_archivo(self) -> CasoUsoAnalisisArchivo:
        if self._caso_uso_analisis_archivo is None:
            self._caso_uso_analisis_archivo = CasoUsoAnalisisArchivo(
                cliente_ia=self._cliente_ia,
                almacenamiento=self._almacenamiento
            )
        return self._caso_uso_analisis_archivo

# Singleton global
contenedor = Contenedor()