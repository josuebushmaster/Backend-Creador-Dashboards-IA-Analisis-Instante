"""
Servicio de procesamiento de archivos
"""
import pandas as pd
import io
from typing import Dict, Any
from src.core.domain.entities import FileData
from src.core.domain.exceptions import FileProcessingError, UnsupportedFileTypeError

class FileProcessingService:
    """Servicio para procesamiento de archivos"""
    
    def __init__(self):
        self.supported_types = ['csv', 'xlsx', 'xls', 'json']
    
    def process_file(self, file_data: FileData) -> Dict[str, Any]:
        """Procesa archivo y extrae información"""
        try:
            # Convertir a DataFrame
            df = self._content_to_dataframe(file_data.content, file_data.file_type)
            
            # Generar información del archivo
            info = {
                "shape": df.shape,
                "columns": list(df.columns),
                "dtypes": df.dtypes.to_dict(),
                "null_counts": df.isnull().sum().to_dict(),
                "sample_data": df.head(5).to_dict('records'),
                "memory_usage": df.memory_usage(deep=True).sum()
            }
            
            # Estadísticas numéricas si las hay
            numeric_columns = df.select_dtypes(include=['number']).columns
            if len(numeric_columns) > 0:
                info["statistics"] = df[numeric_columns].describe().to_dict()
            
            return info
            
        except Exception as e:
            raise FileProcessingError(f"Error procesando archivo: {str(e)}")
    
    def _content_to_dataframe(self, content: bytes, file_type: str) -> pd.DataFrame:
        """Convierte contenido a DataFrame"""
        try:
            if file_type == 'csv':
                return pd.read_csv(io.BytesIO(content))
            elif file_type in ['xlsx', 'xls']:
                return pd.read_excel(io.BytesIO(content))
            elif file_type == 'json':
                return pd.read_json(io.BytesIO(content))
            else:
                raise UnsupportedFileTypeError(f"Tipo no soportado: {file_type}")
                
        except Exception as e:
            raise FileProcessingError(f"Error leyendo archivo: {str(e)}")
    
    def validate_file_type(self, filename: str) -> str:
        """Valida y retorna tipo de archivo"""
        extension = filename.lower().split('.')[-1]
        
        if extension not in self.supported_types:
            raise UnsupportedFileTypeError(
                f"Tipo de archivo no soportado: {extension}. "
                f"Tipos soportados: {', '.join(self.supported_types)}"
            )
        
        return extension