"""
Caso de uso para análisis de archivos
"""
from typing import Optional, Dict, Any
import pandas as pd
import io
from src.core.domain.entities import DatosArchivo, ResultadoAnalisis
from src.core.domain.exceptions import ErrorProcesarArchivo, ErrorTipoArchivoNoSoportado
from src.core.services.ai_analysis import ServicioAnalisisIA
from src.infrastructure.external.interfaces import AIClientInterface
from src.infrastructure.persistence.in_memory_storage import AlmacenamientoMemoria

class CasoUsoAnalisisArchivo:
    """Caso de uso para análisis de archivos con IA"""
    
    def __init__(
        self, 
        cliente_ia: AIClientInterface, 
        cliente_openai: Optional[AIClientInterface] = None,
        almacenamiento: Optional[AlmacenamientoMemoria] = None
    ):
        self.servicio_analisis_ia = ServicioAnalisisIA(cliente_ia)
        self.cliente_openai = cliente_openai
        self.almacenamiento = almacenamiento or AlmacenamientoMemoria()
    
    async def procesar_y_almacenar_archivo(
        self, 
        nombre_archivo: str, 
        contenido: bytes,
        dataframe: pd.DataFrame
    ) -> Dict[str, Any]:
        """Procesa archivo subido y lo almacena"""
        try:
            # Crear entidad de archivo
            datos_archivo = DatosArchivo.crear(
                nombre_archivo=nombre_archivo,
                contenido=contenido,
                tipo_archivo=self._obtener_tipo_archivo(nombre_archivo)
            )
            
            # Guardar archivo en storage
            self.almacenamiento.guardar_archivo(datos_archivo.id_archivo, datos_archivo)
            
            # Guardar DataFrame en storage
            self.almacenamiento.guardar_dataframe(datos_archivo.id_archivo, dataframe)
            
            return {
                "id_archivo": datos_archivo.id_archivo,
                "nombre_archivo": nombre_archivo,
                "tipo_archivo": datos_archivo.tipo_archivo
            }
            
        except Exception as e:
            raise ErrorProcesarArchivo(f"Error procesando archivo: {str(e)}")
    
    async def procesar_archivo(self, nombre_archivo: str, contenido: bytes):
        """Procesa archivo subido (método legacy para compatibilidad)"""
        try:
            # Crear entidad de archivo
            datos_archivo = DatosArchivo.crear(
                nombre_archivo=nombre_archivo,
                contenido=contenido,
                tipo_archivo=self._obtener_tipo_archivo(nombre_archivo)
            )
            
            # Convertir a DataFrame
            df = self._contenido_a_dataframe(contenido, datos_archivo.tipo_archivo)
            
            # Guardar en storage
            self.almacenamiento.guardar_archivo(datos_archivo.id_archivo, datos_archivo)
            self.almacenamiento.guardar_dataframe(datos_archivo.id_archivo, df)
            
            # Generar preview
            datos_vista_previa = df.head(10).to_dict('records')
            
            return {
                "id_archivo": datos_archivo.id_archivo,
                "datos_vista_previa": datos_vista_previa,
                "columnas": list(df.columns),
                "forma": df.shape
            }
            
        except Exception as e:
            raise ErrorProcesarArchivo(f"Error procesando archivo: {str(e)}")
    
    async def analizar_archivo_con_ia(self, id_archivo: str) -> ResultadoAnalisis:
        """
        Analiza archivo usando IA.
        
        Proceso:
        1. Recupera el DataFrame del storage
        2. Extrae nombres de columnas, tipos de datos
        3. Genera resumen estadístico con describe() y info()
        4. Envía esquema y resumen al LLM
        5. El LLM actúa como analista de datos experto
        6. Identifica patrones y relaciones interesantes
        7. Sugiere 3-5 visualizaciones específicas
        8. Retorna JSON estructurado con sugerencias
        """
        try:
            # Recuperar DataFrame del storage
            df = self.almacenamiento.obtener_dataframe(id_archivo)
            
            if df is None:
                raise ValueError(f"Archivo con ID {id_archivo} no encontrado")
            
            # Realizar análisis con IA
            resultado_analisis = await self.servicio_analisis_ia.analizar_datos(df, "general")
            
            # Actualizar id_archivo en el resultado
            resultado_analisis.id_archivo = id_archivo
            
            # Guardar análisis en storage
            self.almacenamiento.guardar_analisis(resultado_analisis.id_analisis, resultado_analisis)
            
            return resultado_analisis
            
        except ValueError:
            raise
        except Exception as e:
            raise ErrorProcesarArchivo(f"Error en análisis: {str(e)}")
    
    async def analizar_archivo(self, ruta_archivo: str, tipo_analisis: str = "general", incluir_graficos: bool = True):
        """Analiza archivo y genera insights (método legacy)"""
        try:
            # Por simplicidad, simularemos cargar el archivo
            # En una implementación real, cargaríamos desde storage
            
            # Simular datos para el ejemplo
            datos_muestra = {
                'ventas': [100, 150, 200, 175, 300],
                'mes': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo'],
                'region': ['Norte', 'Sur', 'Norte', 'Este', 'Oeste']
            }
            df = pd.DataFrame(datos_muestra)
            
            # Realizar análisis con IA
            resultado_analisis = await self.servicio_analisis_ia.analizar_datos(df, tipo_analisis)
            
            return resultado_analisis
            
        except Exception as e:
            raise ErrorProcesarArchivo(f"Error en análisis: {str(e)}")
    
    async def obtener_resultado_analisis(self, id_analisis: str) -> Optional[ResultadoAnalisis]:
        """Obtiene resultado de análisis por ID"""
        return self.almacenamiento.obtener_analisis(id_analisis)
    
    def _obtener_tipo_archivo(self, nombre_archivo: str) -> str:
        """Obtiene tipo de archivo basado en extensión"""
        extension = nombre_archivo.lower().split('.')[-1]
        
        if extension == 'csv':
            return 'csv'
        elif extension in ['xlsx', 'xls']:
            return 'excel'
        elif extension == 'json':
            return 'json'
        else:
            raise ErrorTipoArchivoNoSoportado(f"Tipo de archivo no soportado: {extension}")
    
    def _contenido_a_dataframe(self, contenido: bytes, tipo_archivo: str) -> pd.DataFrame:
        """Convierte contenido de archivo a DataFrame"""
        try:
            if tipo_archivo == 'csv':
                return pd.read_csv(io.BytesIO(contenido))
            elif tipo_archivo == 'excel':
                return pd.read_excel(io.BytesIO(contenido))
            elif tipo_archivo == 'json':
                return pd.read_json(io.BytesIO(contenido))
            else:
                raise ErrorTipoArchivoNoSoportado(f"Tipo de archivo no soportado: {tipo_archivo}")
                
        except Exception as e:
            raise ErrorProcesarArchivo(f"Error leyendo archivo: {str(e)}")