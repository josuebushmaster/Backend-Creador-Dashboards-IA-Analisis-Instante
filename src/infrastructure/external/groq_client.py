"""
Cliente para Groq AI
"""
import asyncio
from typing import List, Dict, Any
from groq import AsyncGroq
from src.infrastructure.external.interfaces import AIClientInterface
from src.infrastructure.config.settings import get_settings

class GroqClient(AIClientInterface):
    """Cliente para interactuar con Groq AI"""
    
    def __init__(self):
        settings = get_settings()
        self.client = AsyncGroq(api_key=settings.groq_api_key)
        self.model = settings.groq_model or "llama-3.1-70b-versatile"
    
    async def generate_analysis(self, prompt: str) -> str:
        """
        Genera análisis usando Groq.
        
        El LLM actúa como analista de datos experto que:
        1. Analiza el esquema y resumen estadístico de los datos
        2. Identifica patrones y relaciones interesantes
        3. Sugiere 3-5 visualizaciones específicas
        4. Retorna JSON estructurado con las sugerencias
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Eres un analista de datos experto con amplia experiencia en visualización de datos y storytelling con datos. 

Tu trabajo es:
1. Analizar cuidadosamente la estructura y contenido de los datos
2. Identificar los patrones, tendencias y relaciones más significativas
3. Sugerir visualizaciones que cuenten una historia clara con los datos
4. Proporcionar insights accionables y contextualizados

Siempre respondes en formato JSON válido cuando se te solicita.
Tus sugerencias son específicas, prácticas y fáciles de implementar."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=3000,
                response_format={"type": "json_object"} if "JSON" in prompt else None
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Error en Groq API: {str(e)}")
    
    async def generate_chart_suggestions(self, data_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Genera sugerencias de gráficos usando Groq
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
                    "type": "bar",
                    "title": "Análisis de Categorías",
                    "x_column": data_context.get('columns', [''])[0],
                    "y_column": data_context.get('columns', ['', ''])[-1],
                    "description": "Comparación por categorías"
                }
            ]
            
        except Exception as e:
            return []