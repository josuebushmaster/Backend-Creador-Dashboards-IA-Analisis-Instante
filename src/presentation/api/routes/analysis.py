"""
Rutas para análisis de archivos
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict, Any
import pandas as pd
import io
import traceback
from src.core.use_cases.file_analysis import CasoUsoAnalisisArchivo
from src.presentation.api.dependencies import almacenamiento_compartido
from src.presentation.api.utils import sanitize_for_json

router = APIRouter()

# Los clientes AI se inicializan bajo demanda (lazy)
caso_uso_analisis_archivo = None

@router.post("/upload")
async def subir_y_analizar_archivo(file: UploadFile = File(...)):
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
    - id_archivo: Para usar en el siguiente endpoint
    - vista_previa: Primeras 10 filas de datos
    - metadatos: Información del archivo (filas, columnas, tipos)
    - sugerencias_graficos: Array con sugerencias de la IA
      - titulo: Título del gráfico
      - tipo_grafico: barras, lineas, pastel, dispersion, area
      - parametros: {eje_x, eje_y, agregacion}
      - insight: Análisis del patrón detectado
    """
    global caso_uso_analisis_archivo
    
    # Inicialización lazy de dependencias
    if caso_uso_analisis_archivo is None:
        from src.presentation.api.dependencies import obtener_cliente_groq, obtener_cliente_openai
        caso_uso_analisis_archivo = CasoUsoAnalisisArchivo(
            obtener_cliente_groq(),
            obtener_cliente_openai(),
            almacenamiento_compartido
        )
    
    try:
        # Leer contenido del archivo
        contenido = await file.read()
        
        # Validar tipo de archivo
        if not file.filename.endswith(('.csv', '.xlsx', '.xls', '.json')):
            raise HTTPException(
                status_code=400, 
                detail="Tipo de archivo no soportado. Use CSV, Excel o JSON."
            )
        
        # Validar tamaño (máximo 10MB)
        if len(contenido) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="Archivo demasiado grande. Máximo 10MB permitido."
            )
        
        # Procesar archivo con pandas
        try:
            if file.filename.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(contenido))
            elif file.filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(io.BytesIO(contenido))
            elif file.filename.endswith('.json'):
                df = pd.read_json(io.BytesIO(contenido))
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al leer archivo: {str(e)}"
            )
        
        # Procesar archivo y guardar en storage
        resultado = await caso_uso_analisis_archivo.procesar_y_almacenar_archivo(
            nombre_archivo=file.filename,
            contenido=contenido,
            dataframe=df
        )
        
        id_archivo = resultado["id_archivo"]
        
        # 🤖 ANÁLISIS CON IA - Automático después de subir
        resultado_analisis = await caso_uso_analisis_archivo.analizar_archivo_con_ia(id_archivo)
        
        # Combinar información del archivo + análisis de IA
        respuesta = {
            "id_archivo": id_archivo,
            "nombre_archivo": file.filename,
            "estado": "analizado",
            "metadatos": {
                "filas": len(df),
                "columnas": len(df.columns),
                "nombres_columnas": list(df.columns),
                "tipos_columnas": df.dtypes.astype(str).to_dict(),
                "conteo_nulos": df.isnull().sum().to_dict(),
                "uso_memoria_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
            },
            "vista_previa": df.head(10).to_dict('records'),
            "estadisticas_resumen": df.describe().to_dict() if len(df.select_dtypes(include='number').columns) > 0 else {},
            "analisis": {
                "resumen": resultado_analisis.resumen,
                "insights": resultado_analisis.insights,
                "sugerencias_graficos": resultado_analisis.sugerencias_graficos
            }
        }

        # Sanitizar la respuesta (convertir NaN/Inf y tipos numpy/pandas)
        respuesta = sanitize_for_json(respuesta)
        return respuesta

    except HTTPException:
        raise
    except Exception as e:
        # Imprimir traceback completo para debugging
        print("\n" + "="*80)
        print("ERROR EN ENDPOINT /upload:")
        print("="*80)
        traceback.print_exc()
        print("="*80 + "\n")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")