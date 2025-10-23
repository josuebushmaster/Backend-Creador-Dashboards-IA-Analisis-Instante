"""
Excepciones del dominio
"""

class DomainException(Exception):
    """Excepción base del dominio"""
    pass

class FileProcessingError(DomainException):
    """Error al procesar archivo"""
    pass

class AnalysisError(DomainException):
    """Error durante el análisis"""
    pass

class ChartGenerationError(DomainException):
    """Error al generar gráfico"""
    pass

class UnsupportedFileTypeError(FileProcessingError):
    """Tipo de archivo no soportado"""
    pass

class InvalidDataError(DomainException):
    """Datos inválidos"""
    pass

class AIServiceError(DomainException):
    """Error en servicio de IA"""
    pass