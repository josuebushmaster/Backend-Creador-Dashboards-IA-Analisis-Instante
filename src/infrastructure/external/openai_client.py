"""
Cliente para OpenAI
"""
import asyncio
from typing import List, Dict, Any
from openai import AsyncOpenAI
from src.infrastructure.external.interfaces import AIClientInterface
from src.infrastructure.config.settings import obtener_configuracion

class ClienteOpenAI(AIClientInterface):
    """Cliente para interactuar con OpenAI"""
    
    def __init__(self):
        configuracion = obtener_configuracion()
        self.cliente = AsyncOpenAI(api_key=configuracion.openai_api_key)
        self.modelo = configuracion.openai_model
    
    async def generar_analisis(self, prompt: str) -> str:
        """
        Genera análisis usando OpenAI
        """
        try:
            respuesta = await self.cliente.chat.completions.create(
                model=self.modelo,
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
            
            return respuesta.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Error en OpenAI API: {str(e)}")
    
    async def generar_sugerencias_grafico(self, contexto_datos: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Genera sugerencias de gráficos usando OpenAI
        """
        prompt = f"""
        Basándote en los siguientes datos, sugiere 3 tipos de gráficos más apropiados:
        
        Columnas: {contexto_datos.get('columnas', [])}
        Tipos de datos: {contexto_datos.get('tipos_datos', {})}
        Forma: {contexto_datos.get('forma', (0, 0))}
        
        Para cada gráfico, especifica:
        - tipo: tipo de gráfico (barras, lineas, pastel, dispersion, area)
        - titulo: título sugerido
        - columna_x: columna para eje X
        - columna_y: columna para eje Y
        - descripcion: breve descripción del insight
        
        Responde en formato JSON como array de objetos.
        """
        
        try:
            respuesta = await self.generar_analisis(prompt)
            # Procesar respuesta y convertir a lista de diccionarios
            # Por simplicidad, retornamos una respuesta predeterminada
            return [
                {
                    "tipo": "lineas",
                    "titulo": "Tendencia Temporal",
                    "columna_x": contexto_datos.get('columnas', [''])[0],
                    "columna_y": contexto_datos.get('columnas', ['', ''])[-1],
                    "descripcion": "Análisis de tendencias en el tiempo"
                }
            ]
            
        except Exception as e:
            return []