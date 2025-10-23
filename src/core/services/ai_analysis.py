"""
Servicio de análisis con IA
"""
from typing import List, Dict, Any
import pandas as pd
import json
from src.core.domain.entities import AnalysisResult
from src.core.domain.exceptions import AnalysisError, AIServiceError
from src.infrastructure.external.interfaces import AIClientInterface

class AIAnalysisService:
    """Servicio para análisis de datos usando IA"""
    
    def __init__(self, ai_client: AIClientInterface):
        self.ai_client = ai_client
    
    async def analyze_data(self, data: pd.DataFrame, analysis_type: str = "general") -> AnalysisResult:
        """
        Analiza datos usando IA y retorna insights
        """
        try:
            # Preparar contexto de los datos
            data_context = self._prepare_data_context(data)
            
            # Generar prompt según tipo de análisis
            prompt = self._generate_analysis_prompt(data_context, analysis_type)
            
            # Obtener análisis de IA
            ai_response = await self.ai_client.generate_analysis(prompt)
            
            # Procesar respuesta
            analysis_data = self._process_ai_response(ai_response)
            
            # Generar sugerencias de gráficos
            chart_suggestions = await self._generate_chart_suggestions(data, analysis_data)
            
            return AnalysisResult.create(
                file_id="",  # Se asignará en el use case
                summary=analysis_data["summary"],
                insights=analysis_data["insights"],
                chart_suggestions=chart_suggestions
            )
            
        except Exception as e:
            raise AnalysisError(f"Error en análisis IA: {str(e)}")
    
    def _prepare_data_context(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Prepara contexto de los datos para IA"""
        return {
            "shape": data.shape,
            "columns": list(data.columns),
            "dtypes": data.dtypes.to_dict(),
            "sample": data.head().to_dict(),
            "stats": data.describe().to_dict() if len(data.select_dtypes(include='number').columns) > 0 else {},
            "null_counts": data.isnull().sum().to_dict()
        }
    
    def _generate_analysis_prompt(self, data_context: Dict[str, Any], analysis_type: str) -> str:
        """Genera prompt para análisis según tipo"""
        base_prompt = f"""
        Analiza los siguientes datos y proporciona insights valiosos:
        
        Forma de los datos: {data_context['shape'][0]} filas, {data_context['shape'][1]} columnas
        Columnas: {', '.join(data_context['columns'])}
        Tipos de datos: {data_context['dtypes']}
        Muestra de datos: {data_context['sample']}
        """
        
        if analysis_type == "statistical":
            base_prompt += f"\\nEstadísticas: {data_context['stats']}"
        
        base_prompt += """
        
        Proporciona:
        1. Un resumen ejecutivo de los datos
        2. 3-5 insights clave encontrados
        3. Patrones o tendencias identificados
        4. Recomendaciones basadas en los datos
        
        Responde en formato JSON con las claves: summary, insights, patterns, recommendations
        """
        
        return base_prompt
    
    def _process_ai_response(self, ai_response: str) -> Dict[str, Any]:
        """Procesa respuesta de IA"""
        try:
            # Intentar parsear como JSON
            if ai_response.strip().startswith('{'):
                return json.loads(ai_response)
            
            # Si no es JSON, procesar como texto
            return {
                "summary": ai_response[:500] + "..." if len(ai_response) > 500 else ai_response,
                "insights": [ai_response],
                "patterns": [],
                "recommendations": []
            }
            
        except json.JSONDecodeError:
            return {
                "summary": "Análisis completado",
                "insights": [ai_response],
                "patterns": [],
                "recommendations": []
            }
    
    async def _generate_chart_suggestions(self, data: pd.DataFrame, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Genera sugerencias de gráficos basado en los datos usando IA"""
        try:
            # Preparar contexto de datos para IA
            data_context = self._prepare_data_context(data)
            
            # Crear prompt para sugerencias de gráficos
            prompt = self._create_chart_suggestion_prompt(data_context, data)
            
            # Obtener sugerencias de IA
            ai_response = await self.ai_client.generate_analysis(prompt)
            
            # Parsear respuesta JSON
            suggestions = self._parse_chart_suggestions(ai_response, data)
            
            return suggestions[:5]  # Máximo 5 sugerencias
            
        except Exception as e:
            # Fallback a sugerencias básicas si falla la IA
            return self._generate_basic_chart_suggestions(data)
    
    def _create_chart_suggestion_prompt(self, data_context: Dict[str, Any], data: pd.DataFrame) -> str:
        """Crea prompt para que la IA sugiera gráficos"""
        numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = data.select_dtypes(include=['datetime']).columns.tolist()
        
        prompt = f"""
        Actúa como un analista de datos experto. Analiza la siguiente estructura de datos y sugiere de 3 a 5 visualizaciones específicas que destaquen los patrones o relaciones más interesantes.

        INFORMACIÓN DEL DATASET:
        - Dimensiones: {data_context['shape'][0]} filas, {data_context['shape'][1]} columnas
        - Columnas numéricas: {', '.join(numeric_cols) if numeric_cols else 'Ninguna'}
        - Columnas categóricas: {', '.join(categorical_cols) if categorical_cols else 'Ninguna'}
        - Columnas de fecha/hora: {', '.join(datetime_cols) if datetime_cols else 'Ninguna'}
        
        ESTADÍSTICAS:
        {json.dumps(data_context.get('stats', {}), indent=2)}
        
        MUESTRA DE DATOS:
        {json.dumps(data_context.get('sample', {}), indent=2)[:500]}
        
        INSTRUCCIONES:
        1. Identifica los patrones, tendencias o relaciones más interesantes en los datos
        2. Sugiere 3-5 visualizaciones específicas que mejor muestren estos insights
        3. Para cada visualización, especifica:
           - title: Título descriptivo del gráfico
           - chart_type: Tipo de gráfico (bar, line, pie, scatter, area)
           - parameters: Objeto con x_axis (nombre de columna para eje X) e y_axis (nombre de columna para eje Y)
           - insight: Breve análisis de qué revelará este gráfico (1-2 oraciones)
        
        RESPONDE ÚNICAMENTE CON UN ARRAY JSON en este formato exacto:
        [
          {{
            "title": "Título del gráfico",
            "chart_type": "bar",
            "parameters": {{
              "x_axis": "nombre_columna_x",
              "y_axis": "nombre_columna_y"
            }},
            "insight": "Este gráfico revela..."
          }}
        ]
        
        IMPORTANTE: 
        - Usa SOLO columnas que existen en el dataset
        - Elige chart_type apropiado para el tipo de datos
        - NO incluyas texto adicional, solo el array JSON
        """
        
        return prompt
    
    def _parse_chart_suggestions(self, ai_response: str, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Parsea las sugerencias de gráficos de la respuesta de IA"""
        try:
            # Limpiar respuesta y extraer JSON
            response_clean = ai_response.strip()
            
            # Buscar el array JSON en la respuesta
            start_idx = response_clean.find('[')
            end_idx = response_clean.rfind(']') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_clean[start_idx:end_idx]
                suggestions = json.loads(json_str)
                
                # Validar que las columnas existan
                valid_suggestions = []
                for suggestion in suggestions:
                    if self._validate_chart_suggestion(suggestion, data):
                        valid_suggestions.append(suggestion)
                
                return valid_suggestions if valid_suggestions else self._generate_basic_chart_suggestions(data)
            else:
                return self._generate_basic_chart_suggestions(data)
                
        except json.JSONDecodeError:
            return self._generate_basic_chart_suggestions(data)
    
    def _validate_chart_suggestion(self, suggestion: Dict[str, Any], data: pd.DataFrame) -> bool:
        """Valida que una sugerencia de gráfico sea válida"""
        try:
            params = suggestion.get('parameters', {})
            x_axis = params.get('x_axis')
            y_axis = params.get('y_axis')
            
            # Verificar que las columnas existan
            if x_axis and x_axis not in data.columns:
                return False
            if y_axis and y_axis not in data.columns:
                return False
            
            # Verificar que tenga los campos requeridos
            required_fields = ['title', 'chart_type', 'parameters', 'insight']
            return all(field in suggestion for field in required_fields)
            
        except Exception:
            return False
    
    def _generate_basic_chart_suggestions(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Genera sugerencias básicas de gráficos como fallback"""
        suggestions = []
        
        numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
        categorical_columns = data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Sugerir gráficos basados en tipos de columnas
        if len(numeric_columns) >= 2:
            suggestions.append({
                "title": f"Relación entre {numeric_columns[0]} y {numeric_columns[1]}",
                "chart_type": "scatter",
                "parameters": {
                    "x_axis": numeric_columns[0],
                    "y_axis": numeric_columns[1]
                },
                "insight": "Este gráfico de dispersión permite visualizar la correlación entre estas dos variables numéricas."
            })
        
        if len(numeric_columns) >= 1 and len(categorical_columns) >= 1:
            suggestions.append({
                "title": f"{numeric_columns[0]} por {categorical_columns[0]}",
                "chart_type": "bar",
                "parameters": {
                    "x_axis": categorical_columns[0],
                    "y_axis": numeric_columns[0]
                },
                "insight": "Este gráfico de barras compara valores numéricos entre diferentes categorías."
            })
        
        if len(numeric_columns) >= 1:
            x_col = data.columns[0] if len(data.columns) > 0 else 'index'
            suggestions.append({
                "title": f"Tendencia de {numeric_columns[0]}",
                "chart_type": "line",
                "parameters": {
                    "x_axis": x_col,
                    "y_axis": numeric_columns[0]
                },
                "insight": "Este gráfico de líneas muestra la evolución de los valores a lo largo del conjunto de datos."
            })
        
        if len(categorical_columns) >= 1 and len(data) < 20:
            suggestions.append({
                "title": f"Distribución por {categorical_columns[0]}",
                "chart_type": "pie",
                "parameters": {
                    "x_axis": categorical_columns[0],
                    "y_axis": "count"
                },
                "insight": "Este gráfico circular muestra la proporción de cada categoría en el total."
            })
        
        return suggestions[:3]  # Máximo 3 sugerencias básicas