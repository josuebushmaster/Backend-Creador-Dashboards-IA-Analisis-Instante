"""
Rutas para información del sistema y cache
"""
from fastapi import APIRouter
from src.presentation.api.dependencies import almacenamiento_compartido

router = APIRouter()

@router.get("/estadisticas-cache")
async def obtener_estadisticas_cache():
    """
    📊 Endpoint de utilidad: Estadísticas del cache
    
    Retorna información sobre el uso de memoria y disco del sistema de cache.
    Útil para:
    - Monitorear uso de recursos
    - Debug de problemas de almacenamiento
    - Verificar que los datos se están guardando correctamente
    
    Response incluye:
    - archivos_memoria: Cantidad de archivos en memoria RAM
    - dataframes_memoria: Cantidad de DataFrames en memoria RAM
    - dataframes_disco: Cantidad de DataFrames en cache de disco
    - tamano_cache_mb: Tamaño total del cache en MB
    """
    stats = almacenamiento_compartido.obtener_estadisticas_cache()
    
    return {
        "estado": "ok",
        "estadisticas": stats,
        "mensaje": f"Cache activo con {stats.get('dataframes_memoria', 0)} DataFrames en memoria"
    }

@router.post("/limpiar-cache")
async def limpiar_cache():
    """
    🗑️ Endpoint de utilidad: Limpiar todo el cache
    
    Elimina todos los datos almacenados en memoria y disco.
    ⚠️ PRECAUCIÓN: Esta acción no se puede deshacer.
    
    Úsalo para:
    - Liberar espacio en disco
    - Resetear el sistema durante desarrollo
    - Limpiar datos de prueba
    """
    almacenamiento_compartido.limpiar_todo()
    
    return {
        "estado": "ok",
        "mensaje": "Cache limpiado exitosamente (memoria y disco)"
    }

@router.get("/archivos-almacenados")
async def listar_archivos_almacenados():
    """
    📁 Endpoint de utilidad: Lista de archivos almacenados
    
    Retorna los IDs de todos los archivos actualmente en el sistema.
    Útil para debug y verificar qué archivos están disponibles.
    """
    ids = almacenamiento_compartido.listar_archivos()
    
    return {
        "estado": "ok",
        "total": len(ids),
        "archivos": ids
    }
