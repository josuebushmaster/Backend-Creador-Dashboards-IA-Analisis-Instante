"""
Rutas para generación de gráficos
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from src.core.use_cases.chart_data import ChartDataUseCase
from src.core.services.chart_data_generator import ChartDataGenerator
from src.infrastructure.persistence.in_memory_storage import InMemoryStorage

router = APIRouter()

# Instanciar dependencias (singleton compartido)
storage = InMemoryStorage()
chart_generator = ChartDataGenerator(storage)
chart_data_use_case = ChartDataUseCase(chart_generator, storage)

class ChartParametersRequest(BaseModel):
    """Modelo para request de parámetros de gráfico"""
    file_id: str
    chart_type: str
    x_axis: str
    y_axis: str
    title: Optional[str] = None
    aggregation: str = "sum"  # sum, avg, count, min, max

@router.post("/chart-data")
async def get_chart_data_post(request: ChartParametersRequest):
    """
    🎯 SEGUNDO ENDPOINT (POST): Generación de datos agregados para gráficos
    
    Recibe los parámetros de una sugerencia del análisis de IA en el body JSON
    y retorna los datos ya procesados, agregados y optimizados para visualización.
    """
    return await _process_chart_request(
        file_id=request.file_id,
        chart_type=request.chart_type,
        x_axis=request.x_axis,
        y_axis=request.y_axis,
        title=request.title,
        aggregation=request.aggregation
    )

async def _process_chart_request(
    file_id: str,
    chart_type: str,
    x_axis: str,
    y_axis: str,
    title: Optional[str] = None,
    aggregation: str = "sum"
):
    """
    Función común para procesar requests de gráficos (POST y GET)
    
    Input (viene de chart_suggestions del endpoint /upload):
    - file_id: ID del archivo analizado
    - chart_type: bar, line, pie, scatter, area
    - x_axis: Columna para eje X
    - y_axis: Columna para eje Y  
    - aggregation: sum, avg, count, min, max
    - title: Título del gráfico (opcional)
    
    Output (listo para biblioteca de gráficos frontend):
    - data: Array de datos agregados y optimizados
      * Bar: Top 20 categorías más relevantes
      * Pie: Top 10 categorías
      * Scatter: Máximo 1000 puntos
      * Line/Area: Series completas ordenadas por X
    - config: Configuración sugerida del gráfico
    - metadata: Información adicional (total_points, aggregation_type, etc)
    
    ❌ NO envía datos crudos completos
    ✅ Solo envía datos necesarios y agregados
    """
    try:
        # Generar datos del gráfico con agregación y optimización
        result = await chart_data_use_case.generate_chart_data_from_file(
            file_id=file_id,
            chart_type=chart_type,
            x_axis=x_axis,
            y_axis=y_axis,
            title=title,
            aggregation=aggregation
        )
        
        return {
            "chart_id": result.chart_id,
            "chart_type": result.chart_type,
            "title": title or f"{y_axis} por {x_axis}",
            "data": result.data,
            "config": result.config,
            "metadata": result.metadata
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando datos del gráfico: {str(e)}")