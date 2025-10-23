"""
Rutas para análisis de archivos
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict, Any
import pandas as pd
import io
from src.core.use_cases.file_analysis import FileAnalysisUseCase
from src.infrastructure.external.groq_client import GroqClient
from src.infrastructure.external.openai_client import OpenAIClient
from src.infrastructure.persistence.in_memory_storage import InMemoryStorage

router = APIRouter()

# Instanciar dependencias (singleton compartido)
groq_client = GroqClient()
openai_client = OpenAIClient()
storage = InMemoryStorage()
file_analysis_use_case = FileAnalysisUseCase(groq_client, openai_client, storage)

@router.post("/upload")
async def upload_and_analyze_file(file: UploadFile = File(...)):
    """
    🎯 ENDPOINT PRINCIPAL: Carga de archivo + Análisis con IA
    
    Este es el ÚNICO endpoint necesario para el flujo completo de análisis.
    
    Funcionalidad:
    1. Recibe archivo (CSV, Excel, JSON)
    2. Valida tipo y tamaño (máx 10MB)
    3. Procesa con pandas
    4. Extrae schema: columnas, tipos de datos, describe(), info()
    5. Envía contexto al LLM (Groq) que actúa como analista de datos experto
    6. Retorna 3-5 sugerencias de visualización en JSON estructurado
    
    Response incluye:
    - file_id: Para usar en el siguiente endpoint
    - preview: Primeras 10 filas de datos
    - metadata: Información del archivo (filas, columnas, tipos)
    - chart_suggestions: Array con sugerencias de la IA
      - title: Título del gráfico
      - chart_type: bar, line, pie, scatter, area
      - parameters: {x_axis, y_axis, aggregation}
      - insight: Análisis del patrón detectado
    """
    try:
        # Leer contenido del archivo
        content = await file.read()
        
        # Validar tipo de archivo
        if not file.filename.endswith(('.csv', '.xlsx', '.xls', '.json')):
            raise HTTPException(
                status_code=400, 
                detail="Tipo de archivo no soportado. Use CSV, Excel o JSON."
            )
        
        # Validar tamaño (máximo 10MB)
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="Archivo demasiado grande. Máximo 10MB permitido."
            )
        
        # Procesar archivo con pandas
        try:
            if file.filename.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(content))
            elif file.filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(io.BytesIO(content))
            elif file.filename.endswith('.json'):
                df = pd.read_json(io.BytesIO(content))
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al leer archivo: {str(e)}"
            )
        
        # Procesar archivo y guardar en storage
        result = await file_analysis_use_case.process_and_store_file(
            filename=file.filename,
            content=content,
            dataframe=df
        )
        
        file_id = result["file_id"]
        
        # 🤖 ANÁLISIS CON IA - Automático después de subir
        analysis_result = await file_analysis_use_case.analyze_file_with_ai(file_id)
        
        # Combinar información del archivo + análisis de IA
        response = {
            "file_id": file_id,
            "filename": file.filename,
            "status": "analyzed",
            "metadata": {
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": list(df.columns),
                "column_types": df.dtypes.astype(str).to_dict(),
                "null_counts": df.isnull().sum().to_dict(),
                "memory_usage_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
            },
            "preview": df.head(10).to_dict('records'),
            "summary_stats": df.describe().to_dict() if len(df.select_dtypes(include='number').columns) > 0 else {},
            "analysis": {
                "summary": analysis_result.summary,
                "insights": analysis_result.insights,
                "chart_suggestions": analysis_result.chart_suggestions
            }
        }
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")