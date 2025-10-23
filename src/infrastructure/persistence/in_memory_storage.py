"""
Almacenamiento híbrido: memoria + disco para persistencia
"""
from typing import Dict, Any, Optional
import uuid
import pandas as pd
from pathlib import Path
import pickle
from src.core.domain.entities import DatosArchivo, ResultadoAnalisis, DatosGrafico

class AlmacenamientoMemoria:
    """Implementación de almacenamiento híbrido (memoria + disco)"""
    
    def __init__(self, usar_cache_disco: bool = True):
        self._archivos: Dict[str, DatosArchivo] = {}
        self._dataframes: Dict[str, pd.DataFrame] = {}
        self._analisis: Dict[str, ResultadoAnalisis] = {}
        self._graficos: Dict[str, DatosGrafico] = {}
        
        # Configuración de cache en disco
        self.usar_cache_disco = usar_cache_disco
        self.directorio_cache = Path("cache_datos")
        
        if self.usar_cache_disco:
            # Crear directorio de cache si no existe
            self.directorio_cache.mkdir(exist_ok=True)
            (self.directorio_cache / "dataframes").mkdir(exist_ok=True)
            (self.directorio_cache / "archivos").mkdir(exist_ok=True)
    
    def guardar_archivo(self, id_archivo: str, datos_archivo: DatosArchivo) -> str:
        """Guarda archivo en memoria"""
        self._archivos[id_archivo] = datos_archivo
        return id_archivo
    
    def obtener_archivo(self, id_archivo: str) -> Optional[DatosArchivo]:
        """Obtiene archivo de memoria"""
        return self._archivos.get(id_archivo)
    
    def guardar_dataframe(self, id_archivo: str, dataframe: pd.DataFrame) -> None:
        """Guarda DataFrame en memoria y opcionalmente en disco"""
        # Guardar en memoria
        self._dataframes[id_archivo] = dataframe
        
        # Guardar en disco como cache (formato Parquet - más eficiente)
        if self.usar_cache_disco:
            ruta_cache = self.directorio_cache / "dataframes" / f"{id_archivo}.parquet"
            try:
                dataframe.to_parquet(ruta_cache, index=False)
            except Exception as e:
                print(f"[!] No se pudo guardar DataFrame en cache: {e}")
    
    def obtener_dataframe(self, id_archivo: str) -> Optional[pd.DataFrame]:
        """Obtiene DataFrame de memoria o disco"""
        # Intentar desde memoria primero
        if id_archivo in self._dataframes:
            return self._dataframes[id_archivo]
        
        # Si no está en memoria, intentar cargar desde disco
        if self.usar_cache_disco:
            ruta_cache = self.directorio_cache / "dataframes" / f"{id_archivo}.parquet"
            if ruta_cache.exists():
                try:
                    df = pd.read_parquet(ruta_cache)
                    # Guardar en memoria para próxima vez
                    self._dataframes[id_archivo] = df
                    return df
                except Exception as e:
                    print(f"[!] Error al cargar DataFrame desde cache: {e}")
        
        return None
    
    def guardar_analisis(self, id_analisis: str, analisis: ResultadoAnalisis) -> None:
        """Guarda resultado de análisis"""
        self._analisis[id_analisis] = analisis
    
    def obtener_analisis(self, id_analisis: str) -> Optional[ResultadoAnalisis]:
        """Obtiene resultado de análisis"""
        return self._analisis.get(id_analisis)
    
    def guardar_grafico(self, id_grafico: str, datos_grafico: DatosGrafico) -> None:
        """Guarda datos de gráfico"""
        self._graficos[id_grafico] = datos_grafico
    
    def obtener_grafico(self, id_grafico: str) -> Optional[DatosGrafico]:
        """Obtiene datos de gráfico"""
        return self._graficos.get(id_grafico)
    
    def eliminar_archivo(self, id_archivo: str) -> bool:
        """Elimina archivo y datos asociados de memoria y disco"""
        eliminado = False
        
        if id_archivo in self._archivos:
            del self._archivos[id_archivo]
            eliminado = True
        
        if id_archivo in self._dataframes:
            del self._dataframes[id_archivo]
        
        # Eliminar cache del disco
        if self.usar_cache_disco:
            ruta_cache = self.directorio_cache / "dataframes" / f"{id_archivo}.parquet"
            if ruta_cache.exists():
                try:
                    ruta_cache.unlink()
                except Exception as e:
                    print(f"[!] Error al eliminar cache: {e}")
        
        return eliminado
    
    def listar_archivos(self) -> list:
        """Lista todos los archivos almacenados"""
        return list(self._archivos.keys())
    
    def limpiar_todo(self) -> None:
        """Limpia todo el almacenamiento (memoria y disco)"""
        self._archivos.clear()
        self._dataframes.clear()
        self._analisis.clear()
        self._graficos.clear()
        
        # Limpiar cache del disco
        if self.usar_cache_disco:
            try:
                import shutil
                if self.directorio_cache.exists():
                    shutil.rmtree(self.directorio_cache)
                    self.directorio_cache.mkdir(exist_ok=True)
                    (self.directorio_cache / "dataframes").mkdir(exist_ok=True)
                    (self.directorio_cache / "archivos").mkdir(exist_ok=True)
            except Exception as e:
                print(f"⚠️  Error al limpiar cache del disco: {e}")
    
    def obtener_estadisticas_cache(self) -> Dict[str, Any]:
        """Obtiene estadísticas del cache"""
        stats = {
            "archivos_memoria": len(self._archivos),
            "dataframes_memoria": len(self._dataframes),
            "analisis_memoria": len(self._analisis),
            "graficos_memoria": len(self._graficos)
        }
        
        if self.usar_cache_disco and self.directorio_cache.exists():
            dir_df = self.directorio_cache / "dataframes"
            stats["dataframes_disco"] = len(list(dir_df.glob("*.parquet"))) if dir_df.exists() else 0
            
            # Calcular tamaño total del cache
            tamano_total = sum(f.stat().st_size for f in dir_df.glob("*.parquet")) if dir_df.exists() else 0
            stats["tamano_cache_mb"] = round(tamano_total / (1024 * 1024), 2)
        
        return stats