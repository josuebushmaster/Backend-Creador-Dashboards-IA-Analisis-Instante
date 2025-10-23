"""
Caso de uso para análisis de archivos
"""
from typing import Optional, Dict, Any
import pandas as pd
import io
from src.core.domain.entities import FileData, AnalysisResult
from src.core.domain.exceptions import FileProcessingError, UnsupportedFileTypeError
from src.core.services.ai_analysis import AIAnalysisService
from src.infrastructure.external.interfaces import AIClientInterface
from src.infrastructure.persistence.in_memory_storage import InMemoryStorage

class FileAnalysisUseCase:
    """Caso de uso para análisis de archivos con IA"""
    
    def __init__(
        self, 
        ai_client: AIClientInterface, 
        openai_client: Optional[AIClientInterface] = None,
        storage: Optional[InMemoryStorage] = None
    ):
        self.ai_analysis_service = AIAnalysisService(ai_client)
        self.openai_client = openai_client
        self.storage = storage or InMemoryStorage()
    
    async def process_and_store_file(
        self, 
        filename: str, 
        content: bytes,
        dataframe: pd.DataFrame
    ) -> Dict[str, Any]:
        """Procesa archivo subido y lo almacena"""
        try:
            # Crear entidad de archivo
            file_data = FileData.create(
                filename=filename,
                content=content,
                file_type=self._get_file_type(filename)
            )
            
            # Guardar archivo en storage
            self.storage.save_file(file_data.file_id, file_data)
            
            # Guardar DataFrame en storage
            self.storage.save_dataframe(file_data.file_id, dataframe)
            
            return {
                "file_id": file_data.file_id,
                "filename": filename,
                "file_type": file_data.file_type
            }
            
        except Exception as e:
            raise FileProcessingError(f"Error procesando archivo: {str(e)}")
    
    async def process_file(self, filename: str, content: bytes):
        """Procesa archivo subido (método legacy para compatibilidad)"""
        try:
            # Crear entidad de archivo
            file_data = FileData.create(
                filename=filename,
                content=content,
                file_type=self._get_file_type(filename)
            )
            
            # Convertir a DataFrame
            df = self._content_to_dataframe(content, file_data.file_type)
            
            # Guardar en storage
            self.storage.save_file(file_data.file_id, file_data)
            self.storage.save_dataframe(file_data.file_id, df)
            
            # Generar preview
            preview_data = df.head(10).to_dict('records')
            
            return {
                "file_id": file_data.file_id,
                "preview_data": preview_data,
                "columns": list(df.columns),
                "shape": df.shape
            }
            
        except Exception as e:
            raise FileProcessingError(f"Error procesando archivo: {str(e)}")
    
    async def analyze_file_with_ai(self, file_id: str) -> AnalysisResult:
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
            df = self.storage.get_dataframe(file_id)
            
            if df is None:
                raise ValueError(f"Archivo con ID {file_id} no encontrado")
            
            # Realizar análisis con IA
            analysis_result = await self.ai_analysis_service.analyze_data(df, "general")
            
            # Actualizar file_id en el resultado
            analysis_result.file_id = file_id
            
            # Guardar análisis en storage
            self.storage.save_analysis(analysis_result.analysis_id, analysis_result)
            
            return analysis_result
            
        except ValueError:
            raise
        except Exception as e:
            raise FileProcessingError(f"Error en análisis: {str(e)}")
    
    async def analyze_file(self, file_path: str, analysis_type: str = "general", include_charts: bool = True):
        """Analiza archivo y genera insights (método legacy)"""
        try:
            # Por simplicidad, simularemos cargar el archivo
            # En una implementación real, cargaríamos desde storage
            
            # Simular datos para el ejemplo
            sample_data = {
                'ventas': [100, 150, 200, 175, 300],
                'mes': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo'],
                'region': ['Norte', 'Sur', 'Norte', 'Este', 'Oeste']
            }
            df = pd.DataFrame(sample_data)
            
            # Realizar análisis con IA
            analysis_result = await self.ai_analysis_service.analyze_data(df, analysis_type)
            
            return analysis_result
            
        except Exception as e:
            raise FileProcessingError(f"Error en análisis: {str(e)}")
    
    async def get_analysis_result(self, analysis_id: str) -> Optional[AnalysisResult]:
        """Obtiene resultado de análisis por ID"""
        return self.storage.get_analysis(analysis_id)
    
    def _get_file_type(self, filename: str) -> str:
        """Obtiene tipo de archivo basado en extensión"""
        extension = filename.lower().split('.')[-1]
        
        if extension == 'csv':
            return 'csv'
        elif extension in ['xlsx', 'xls']:
            return 'excel'
        elif extension == 'json':
            return 'json'
        else:
            raise UnsupportedFileTypeError(f"Tipo de archivo no soportado: {extension}")
    
    def _content_to_dataframe(self, content: bytes, file_type: str) -> pd.DataFrame:
        """Convierte contenido de archivo a DataFrame"""
        try:
            if file_type == 'csv':
                return pd.read_csv(io.BytesIO(content))
            elif file_type == 'excel':
                return pd.read_excel(io.BytesIO(content))
            elif file_type == 'json':
                return pd.read_json(io.BytesIO(content))
            else:
                raise UnsupportedFileTypeError(f"Tipo de archivo no soportado: {file_type}")
                
        except Exception as e:
            raise FileProcessingError(f"Error leyendo archivo: {str(e)}")