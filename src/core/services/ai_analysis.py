"""
Servicio de análisis con IA
"""
from typing import List, Dict, Any
import pandas as pd
import json
from src.core.domain.entities import ResultadoAnalisis
from src.core.domain.exceptions import ErrorAnalisis, ErrorServicioIA
from src.infrastructure.external.interfaces import AIClientInterface

class ServicioAnalisisIA:
    """Servicio para análisis de datos usando IA"""
    
    def __init__(self, cliente_ia: AIClientInterface):
        self.cliente_ia = cliente_ia
    
    async def analizar_datos(self, data: pd.DataFrame, tipo_analisis: str = "general") -> ResultadoAnalisis:
        """
        Analiza datos usando IA y retorna insights
        """
        try:
            # Preparar contexto de los datos
            contexto_datos = self._preparar_contexto_datos(data)
            
            # Generar prompt según tipo de análisis
            prompt = self._generar_prompt_analisis(contexto_datos, tipo_analisis)
            
            # Obtener análisis de IA
            respuesta_ia = await self.cliente_ia.generar_analisis(prompt)
            
            # Procesar respuesta
            datos_analisis = self._procesar_respuesta_ia(respuesta_ia)
            
            # Generar sugerencias de gráficos
            sugerencias_graficos = await self._generar_sugerencias_graficos(data, datos_analisis)
            
            return ResultadoAnalisis.crear(
                id_archivo="",  # Se asignará en el use case
                resumen=datos_analisis["resumen"],
                insights=datos_analisis["insights"],
                sugerencias_graficos=sugerencias_graficos
            )
            
        except Exception as e:
            raise ErrorAnalisis(f"Error en análisis IA: {str(e)}")
    
    def _preparar_contexto_datos(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Prepara contexto de los datos para IA"""
        return {
            "forma": data.shape,
            "columnas": list(data.columns),
            "tipos_datos": data.dtypes.to_dict(),
            "muestra": data.head().to_dict(),
            "estadisticas": data.describe().to_dict() if len(data.select_dtypes(include='number').columns) > 0 else {},
            "conteo_nulos": data.isnull().sum().to_dict()
        }
    
    def _generar_prompt_analisis(self, contexto_datos: Dict[str, Any], tipo_analisis: str) -> str:
        """Genera prompt para análisis según tipo"""
        prompt_base = f"""
        Analiza los siguientes datos y proporciona insights valiosos:
        
        Forma de los datos: {contexto_datos['forma'][0]} filas, {contexto_datos['forma'][1]} columnas
        Columnas: {', '.join(contexto_datos['columnas'])}
        Tipos de datos: {contexto_datos['tipos_datos']}
        Muestra de datos: {contexto_datos['muestra']}
        """
        
        if tipo_analisis == "estadistico":
            prompt_base += f"\\nEstadísticas: {contexto_datos['estadisticas']}"
        
        prompt_base += """
        
        Proporciona:
        1. Un resumen ejecutivo de los datos
        2. 3-5 insights clave encontrados
        3. Patrones o tendencias identificados
        4. Recomendaciones basadas en los datos
        
        Responde en formato JSON con las claves: resumen, insights, patrones, recomendaciones
        """
        
        return prompt_base
    
    def _procesar_respuesta_ia(self, respuesta_ia: str) -> Dict[str, Any]:
        """Procesa respuesta de IA"""
        try:
            # Intentar parsear como JSON
            if respuesta_ia.strip().startswith('{'):
                return json.loads(respuesta_ia)
            
            # Si no es JSON, procesar como texto
            return {
                "resumen": respuesta_ia[:500] + "..." if len(respuesta_ia) > 500 else respuesta_ia,
                "insights": [respuesta_ia],
                "patrones": [],
                "recomendaciones": []
            }
            
        except json.JSONDecodeError:
            return {
                "resumen": "Análisis completado",
                "insights": [respuesta_ia],
                "patrones": [],
                "recomendaciones": []
            }
    
    async def _generar_sugerencias_graficos(self, data: pd.DataFrame, analisis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Genera sugerencias de gráficos basado en los datos usando IA"""
        try:
            # Preparar contexto de datos para IA
            contexto_datos = self._preparar_contexto_datos(data)
            
            # Crear prompt para sugerencias de gráficos
            prompt = self._crear_prompt_sugerencia_graficos(contexto_datos, data)
            
            # Obtener sugerencias de IA
            respuesta_ia = await self.cliente_ia.generar_analisis(prompt)
            
            # Parsear respuesta JSON
            sugerencias = self._parsear_sugerencias_graficos(respuesta_ia, data)
            
            return sugerencias[:5]  # Máximo 5 sugerencias
            
        except Exception as e:
            # Fallback a sugerencias básicas si falla la IA
            return self._generar_sugerencias_graficos_basicas(data)
    
    def _crear_prompt_sugerencia_graficos(self, contexto_datos: Dict[str, Any], data: pd.DataFrame) -> str:
        """Crea prompt para que la IA sugiera gráficos"""
        cols_numericas = data.select_dtypes(include=['number']).columns.tolist()
        cols_categoricas = data.select_dtypes(include=['object', 'category']).columns.tolist()
        cols_fecha = data.select_dtypes(include=['datetime']).columns.tolist()
        
        prompt = f"""
        Actúa como un analista de datos experto. Analiza la siguiente estructura de datos y sugiere de 3 a 5 visualizaciones específicas que destaquen los patrones o relaciones más interesantes.

        INFORMACIÓN DEL DATASET:
        - Dimensiones: {contexto_datos['forma'][0]} filas, {contexto_datos['forma'][1]} columnas
        - Columnas numéricas: {', '.join(cols_numericas) if cols_numericas else 'Ninguna'}
        - Columnas categóricas: {', '.join(cols_categoricas) if cols_categoricas else 'Ninguna'}
        - Columnas de fecha/hora: {', '.join(cols_fecha) if cols_fecha else 'Ninguna'}
        
        ESTADÍSTICAS:
        {json.dumps(contexto_datos.get('estadisticas', {}), indent=2)}
        
        MUESTRA DE DATOS:
        {json.dumps(contexto_datos.get('muestra', {}), indent=2)[:500]}
        
        INSTRUCCIONES:
        1. Identifica los patrones, tendencias o relaciones más interesantes en los datos
        2. Sugiere 3-5 visualizaciones específicas que mejor muestren estos insights
        3. Para cada visualización, especifica:
           - titulo: Título descriptivo del gráfico
           - tipo_grafico: Tipo de gráfico (barras, lineas, pastel, dispersion, area)
           - parametros: Objeto con eje_x (nombre de columna para eje X) e eje_y (nombre de columna para eje Y)
           - insight: Breve análisis de qué revelará este gráfico (1-2 oraciones)
        
        RESPONDE ÚNICAMENTE CON UN ARRAY JSON en este formato exacto:
        [
          {{
            "titulo": "Título del gráfico",
            "tipo_grafico": "barras",
            "parametros": {{
              "eje_x": "nombre_columna_x",
              "eje_y": "nombre_columna_y"
            }},
            "insight": "Este gráfico revela..."
          }}
        ]
        
        IMPORTANTE: 
        - Usa SOLO columnas que existen en el dataset
        - Elige tipo_grafico apropiado para el tipo de datos
        - NO incluyas texto adicional, solo el array JSON
        """
        
        return prompt
    
    def _parsear_sugerencias_graficos(self, respuesta_ia: str, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Parsea las sugerencias de gráficos de la respuesta de IA"""
        try:
            # Limpiar respuesta y extraer JSON
            respuesta_limpia = respuesta_ia.strip()
            
            # Buscar el array JSON en la respuesta
            indice_inicio = respuesta_limpia.find('[')
            indice_fin = respuesta_limpia.rfind(']') + 1
            
            if indice_inicio != -1 and indice_fin > indice_inicio:
                json_str = respuesta_limpia[indice_inicio:indice_fin]
                sugerencias = json.loads(json_str)
                
                # Validar que las columnas existan
                sugerencias_validas = []
                for sugerencia in sugerencias:
                    if self._validar_sugerencia_grafico(sugerencia, data):
                        sugerencias_validas.append(sugerencia)
                
                return sugerencias_validas if sugerencias_validas else self._generar_sugerencias_graficos_basicas(data)
            else:
                return self._generar_sugerencias_graficos_basicas(data)
                
        except json.JSONDecodeError:
            return self._generar_sugerencias_graficos_basicas(data)
    
    def _validar_sugerencia_grafico(self, sugerencia: Dict[str, Any], data: pd.DataFrame) -> bool:
        """Valida que una sugerencia de gráfico sea válida"""
        try:
            params = sugerencia.get('parametros', {})
            eje_x = params.get('eje_x')
            eje_y = params.get('eje_y')
            
            # Verificar que las columnas existan
            if eje_x and eje_x not in data.columns:
                return False
            if eje_y and eje_y not in data.columns:
                return False
            
            # Verificar que tenga los campos requeridos
            campos_requeridos = ['titulo', 'tipo_grafico', 'parametros', 'insight']
            return all(campo in sugerencia for campo in campos_requeridos)
            
        except Exception:
            return False
    
    def _generar_sugerencias_graficos_basicas(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Genera sugerencias básicas de gráficos como fallback"""
        sugerencias = []
        
        columnas_numericas = data.select_dtypes(include=['number']).columns.tolist()
        columnas_categoricas = data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Sugerir gráficos basados en tipos de columnas
        if len(columnas_numericas) >= 2:
            sugerencias.append({
                "titulo": f"Relación entre {columnas_numericas[0]} y {columnas_numericas[1]}",
                "tipo_grafico": "dispersion",
                "parametros": {
                    "eje_x": columnas_numericas[0],
                    "eje_y": columnas_numericas[1]
                },
                "insight": "Este gráfico de dispersión permite visualizar la correlación entre estas dos variables numéricas."
            })
        
        if len(columnas_numericas) >= 1 and len(columnas_categoricas) >= 1:
            sugerencias.append({
                "titulo": f"{columnas_numericas[0]} por {columnas_categoricas[0]}",
                "tipo_grafico": "barras",
                "parametros": {
                    "eje_x": columnas_categoricas[0],
                    "eje_y": columnas_numericas[0]
                },
                "insight": "Este gráfico de barras compara valores numéricos entre diferentes categorías."
            })
        
        if len(columnas_numericas) >= 1:
            col_x = data.columns[0] if len(data.columns) > 0 else 'indice'
            sugerencias.append({
                "titulo": f"Tendencia de {columnas_numericas[0]}",
                "tipo_grafico": "lineas",
                "parametros": {
                    "eje_x": col_x,
                    "eje_y": columnas_numericas[0]
                },
                "insight": "Este gráfico de líneas muestra la evolución de los valores a lo largo del conjunto de datos."
            })
        
        if len(columnas_categoricas) >= 1 and len(data) < 20:
            sugerencias.append({
                "titulo": f"Distribución por {columnas_categoricas[0]}",
                "tipo_grafico": "pastel",
                "parametros": {
                    "eje_x": columnas_categoricas[0],
                    "eje_y": "conteo"
                },
                "insight": "Este gráfico circular muestra la proporción de cada categoría en el total."
            })
        
        return sugerencias[:3]  # Máximo 3 sugerencias básicas