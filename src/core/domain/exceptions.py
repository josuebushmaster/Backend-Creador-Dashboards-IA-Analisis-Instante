"""
Excepciones del dominio
"""

class ExcepcionDominio(Exception):
    """Excepción base del dominio"""
    pass

class ErrorProcesarArchivo(ExcepcionDominio):
    """Error al procesar archivo"""
    pass

class ErrorAnalisis(ExcepcionDominio):
    """Error durante el análisis"""
    pass

class ErrorGeneracionGrafico(ExcepcionDominio):
    """Error al generar gráfico"""
    pass

class ErrorTipoArchivoNoSoportado(ErrorProcesarArchivo):
    """Tipo de archivo no soportado"""
    pass

class ErrorDatosInvalidos(ExcepcionDominio):
    """Datos inválidos"""
    pass

class ErrorServicioIA(ExcepcionDominio):
    """Error en servicio de IA"""
    pass