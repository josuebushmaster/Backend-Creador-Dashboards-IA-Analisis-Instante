"""
Cliente para OpenAI
"""
import asyncio
from typing import List, Dict, Any
from openai import AsyncOpenAI
from src.infrastructure.external.interfaces import AIClientInterface
from src.infrastructure.config.settings import get_settings

class OpenAIClient(AIClientInterface):
    """Cliente para interactuar con OpenAI"""
    
    def __init__(self):
        settings = get_settings()
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model or "gpt-3.5-turbo"
    
    async def generate_analysis(self, prompt: str) -> str:
        """
        Genera análisis usando OpenAI
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un analista de datos experto. Proporciona análisis claros, insights valiosos y recomendaciones prácticas basadas en los datos."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Error en OpenAI API: {str(e)}")
    
    async def generate_chart_suggestions(self, data_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Genera sugerencias de gráficos usando OpenAI
        """
        prompt = f"""
        Basándote en los siguientes datos, sugiere 3 tipos de gráficos más apropiados:
        
        Columnas: {data_context.get('columns', [])}
        Tipos de datos: {data_context.get('dtypes', {})}
        Forma: {data_context.get('shape', (0, 0))}
        
        Para cada gráfico, especifica:
        - type: tipo de gráfico (bar, line, pie, scatter, area)
        - title: título sugerido
        - x_column: columna para eje X
        - y_column: columna para eje Y
        - description: breve descripción del insight
        
        Responde en formato JSON como array de objetos.
        """
        
        try:
            response = await self.generate_analysis(prompt)
            # Procesar respuesta y convertir a lista de diccionarios
            # Por simplicidad, retornamos una respuesta predeterminada
            return [
                {
                    "type": "line",
                    "title": "Tendencia Temporal",
                    "x_column": data_context.get('columns', [''])[0],
                    "y_column": data_context.get('columns', ['', ''])[-1],
                    "description": "Análisis de tendencias en el tiempo"
                }
            ]
            
        except Exception as e:
            return []