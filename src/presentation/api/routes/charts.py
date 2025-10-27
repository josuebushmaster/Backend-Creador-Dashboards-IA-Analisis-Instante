"""
Rutas para generación de gráficos
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import traceback
from src.core.use_cases.chart_data import CasoUsoDatosGrafico
from src.core.services.chart_data_generator import GeneradorDatosGrafico
from src.presentation.api.dependencies import almacenamiento_compartido
from src.presentation.api.utils import sanitize_for_json

router = APIRouter()

# Usar lazy initialization para evitar errores en import time
caso_uso_datos_grafico = None

class SolicitudParametrosGrafico(BaseModel):
    """Modelo para request de parámetros de gráfico"""
    id_archivo: str
    tipo_grafico: str
    eje_x: str
    eje_y: str
    titulo: Optional[str] = None
    agregacion: str = "suma"  # suma, promedio, conteo, minimo, maximo

@router.post("/chart-data")
async def obtener_datos_grafico_post(solicitud: SolicitudParametrosGrafico):
    """
    🎯 SEGUNDO ENDPOINT (POST): Generación de datos agregados para gráficos
    
    Recibe los parámetros de una sugerencia del análisis de IA en el body JSON
    y retorna los datos ya procesados, agregados y optimizados para visualización.
    """
    global caso_uso_datos_grafico
    
    # Inicialización lazy
    if caso_uso_datos_grafico is None:
        generador_graficos = GeneradorDatosGrafico(almacenamiento_compartido)
        caso_uso_datos_grafico = CasoUsoDatosGrafico(generador_graficos, almacenamiento_compartido)
    
    return await _procesar_solicitud_grafico(
        id_archivo=solicitud.id_archivo,
        tipo_grafico=solicitud.tipo_grafico,
        eje_x=solicitud.eje_x,
        eje_y=solicitud.eje_y,
        titulo=solicitud.titulo,
        agregacion=solicitud.agregacion
    )

async def _procesar_solicitud_grafico(
    id_archivo: str,
    tipo_grafico: str,
    eje_x: str,
    eje_y: str,
    titulo: Optional[str] = None,
    agregacion: str = "suma"
):
    """
    Función común para procesar requests de gráficos (POST y GET)
    
    Input (viene de sugerencias_graficos del endpoint /upload):
    - id_archivo: ID del archivo analizado
    - tipo_grafico: barras, lineas, pastel, dispersion, area
    - eje_x: Columna para eje X
    - eje_y: Columna para eje Y  
    - agregacion: suma, promedio, conteo, minimo, maximo
    - titulo: Título del gráfico (opcional)
    
    Output (listo para biblioteca de gráficos frontend):
    - datos: Array de datos agregados y optimizados
      * Barras: Top 20 categorías más relevantes
      * Pastel: Top 10 categorías
      * Dispersión: Máximo 1000 puntos
      * Líneas/Area: Series completas ordenadas por X
    - configuracion: Configuración sugerida del gráfico
    - metadatos: Información adicional (total_puntos, tipo_agregacion, etc)
    
    ❌ NO envía datos crudos completos
    ✅ Solo envía datos necesarios y agregados
    """
    try:
        # Generar datos del gráfico con agregación y optimización
        resultado = await caso_uso_datos_grafico.generar_datos_grafico_desde_archivo(
            id_archivo=id_archivo,
            tipo_grafico=tipo_grafico,
            eje_x=eje_x,
            eje_y=eje_y,
            titulo=titulo,
            agregacion=agregacion
        )
        
        respuesta = {
            "id_grafico": resultado.id_grafico,
            "tipo_grafico": resultado.tipo_grafico,
            "titulo": titulo or f"{eje_y} por {eje_x}",
            "datos": resultado.datos,
            "configuracion": resultado.configuracion,
            "metadatos": resultado.metadatos
        }

        # Sanitizar respuesta para evitar NaN/Inf en la serialización JSON
        return sanitize_for_json(respuesta)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Imprimir traceback completo para debugging
        print("\n" + "="*80)
        print("ERROR EN ENDPOINT /chart-data:")
        print("="*80)
        traceback.print_exc()
        print("="*80 + "\n")
        raise HTTPException(status_code=500, detail=f"Error generando datos del gráfico: {str(e)}")