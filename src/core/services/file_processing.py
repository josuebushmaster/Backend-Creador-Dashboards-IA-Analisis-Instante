"""
Servicio de procesamiento de archivos
"""
import pandas as pd
import io
from typing import Dict, Any
from src.core.domain.entities import DatosArchivo
from src.core.domain.exceptions import ErrorProcesarArchivo, ErrorTipoArchivoNoSoportado

class ServicioProcesarArchivo:
    """Servicio para procesamiento de archivos"""
    
    def __init__(self):
        self.tipos_soportados = ['csv', 'xlsx', 'xls', 'json']
    
    def procesar_archivo(self, datos_archivo: DatosArchivo) -> Dict[str, Any]:
        """Procesa archivo y extrae información"""
        try:
            # Convertir a DataFrame
            df = self._contenido_a_dataframe(datos_archivo.contenido, datos_archivo.tipo_archivo)
            
            # Generar información del archivo
            info = {
                "forma": df.shape,
                "columnas": list(df.columns),
                "tipos_datos": df.dtypes.to_dict(),
                "conteo_nulos": df.isnull().sum().to_dict(),
                "datos_muestra": df.head(5).to_dict('records'),
                "uso_memoria": df.memory_usage(deep=True).sum()
            }
            
            # Estadísticas numéricas si las hay
            columnas_numericas = df.select_dtypes(include=['number']).columns
            if len(columnas_numericas) > 0:
                info["estadisticas"] = df[columnas_numericas].describe().to_dict()
            
            return info
            
        except Exception as e:
            raise ErrorProcesarArchivo(f"Error procesando archivo: {str(e)}")
    
    def _contenido_a_dataframe(self, contenido: bytes, tipo_archivo: str) -> pd.DataFrame:
        """Convierte contenido a DataFrame"""
        try:
            if tipo_archivo == 'csv':
                return pd.read_csv(io.BytesIO(contenido))
            elif tipo_archivo in ['xlsx', 'xls']:
                return pd.read_excel(io.BytesIO(contenido))
            elif tipo_archivo == 'json':
                return pd.read_json(io.BytesIO(contenido))
            else:
                raise ErrorTipoArchivoNoSoportado(f"Tipo no soportado: {tipo_archivo}")
                
        except Exception as e:
            raise ErrorProcesarArchivo(f"Error leyendo archivo: {str(e)}")
    
    def validar_tipo_archivo(self, nombre_archivo: str) -> str:
        """Valida y retorna tipo de archivo"""
        extension = nombre_archivo.lower().split('.')[-1]
        
        if extension not in self.tipos_soportados:
            raise ErrorTipoArchivoNoSoportado(
                f"Tipo de archivo no soportado: {extension}. "
                f"Tipos soportados: {', '.join(self.tipos_soportados)}"
            )
        
        return extension