"""
Caso de uso para datos de gráficos
"""
from typing import List, Dict, Any, Optional
from src.core.domain.entities import ChartData
from src.core.services.chart_data_generator import ChartDataGenerator
from src.infrastructure.persistence.in_memory_storage import InMemoryStorage

class ChartDataUseCase:
    """Caso de uso para generar datos de gráficos"""
    
    def __init__(
        self, 
        chart_generator: ChartDataGenerator,
        storage: Optional[InMemoryStorage] = None
    ):
        self.chart_generator = chart_generator
        self.storage = storage or InMemoryStorage()
    
    async def generate_chart_data_from_file(
        self,
        file_id: str,
        chart_type: str,
        x_axis: str,
        y_axis: str,
        title: str = None,
        aggregation: str = "sum"
    ) -> ChartData:
        """
        Genera datos de gráfico desde un archivo almacenado.
        
        Este método recibe los parámetros del gráfico sugerido por la IA
        y retorna los datos ya agregados y formateados, listos para visualizar.
        Evita enviar todo el conjunto de datos crudos al cliente.
        """
        # Recuperar DataFrame del storage
        df = self.storage.get_dataframe(file_id)
        
        if df is None:
            raise ValueError(f"Archivo con ID {file_id} no encontrado")
        
        # Generar datos del gráfico
        chart_data = await self.chart_generator.generate_from_dataframe(
            dataframe=df,
            chart_type=chart_type,
            x_axis=x_axis,
            y_axis=y_axis,
            title=title,
            aggregation=aggregation
        )
        
        # Guardar en storage
        self.storage.save_chart(chart_data.chart_id, chart_data)
        
        return chart_data
    
    async def generate_chart_data(
        self,
        data: List[Dict[str, Any]],
        chart_type: str,
        x_column: str,
        y_column: str,
        title: str = None
    ) -> ChartData:
        """Genera datos para gráfico desde datos raw"""
        return await self.chart_generator.generate_chart_data(
            data=data,
            chart_type=chart_type,
            x_column=x_column,
            y_column=y_column,
            title=title
        )
    
    async def get_chart_data(self, chart_id: str) -> Optional[ChartData]:
        """Obtiene datos de gráfico por ID"""
        return self.storage.get_chart(chart_id)