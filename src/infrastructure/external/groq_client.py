"""
Cliente para Groq AI
"""
import asyncio
from typing import List, Dict, Any

# Intentar importar Groq con manejo de errores
GROQ_AVAILABLE = False
try:
    from groq import AsyncGroq
    GROQ_AVAILABLE = True
except Exception as e:
    print(f"[!] Groq no disponible (sera sustituido por OpenAI): {type(e).__name__}")
    AsyncGroq = None  # Placeholder

from src.infrastructure.external.interfaces import AIClientInterface
from src.infrastructure.config.settings import obtener_configuracion

class ClienteGroq(AIClientInterface):
    """Cliente para interactuar con Groq AI (con fallback automático a OpenAI)"""
    
    def __init__(self):
        configuracion = obtener_configuracion()
        self.usando_groq = False
        
        if GROQ_AVAILABLE and AsyncGroq is not None:
            try:
                self.cliente = AsyncGroq(api_key=configuracion.groq_api_key)
                self.modelo = configuracion.groq_model
                self.usando_groq = True
                print("[OK] Cliente Groq inicializado correctamente")
                return
            except Exception as e:
                print(f"[!] Error al inicializar Groq: {type(e).__name__} - {str(e)[:100]}")
        
        # Fallback a OpenAI
        self._inicializar_fallback()
    
    def _inicializar_fallback(self):
        """Usa OpenAI como fallback"""
        from openai import AsyncOpenAI
        configuracion = obtener_configuracion()
        self.cliente = AsyncOpenAI(api_key=configuracion.openai_api_key)
        self.modelo = configuracion.openai_model
        self.usando_groq = False
        print("[INFO] Usando OpenAI como cliente AI principal")
    
    async def generar_analisis(self, prompt: str) -> str:
        """
        Genera análisis usando Groq.
        
        El LLM actúa como analista de datos experto que:
        1. Analiza el esquema y resumen estadístico de los datos
        2. Identifica patrones y relaciones interesantes
        3. Sugiere 3-5 visualizaciones específicas
        4. Retorna JSON estructurado con las sugerencias
        """
        try:
            respuesta = await self.cliente.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": """Eres un analista de datos senior con más de 15 años de experiencia en Business Intelligence y visualización de datos. Tu especialidad es:
    1. Identificar patrones ocultos y anomalías en grandes volúmenes de datos
    2. Transformar datos complejos en insights accionables que impulsen decisiones de negocio
    3. Diseñar visualizaciones efectivas adaptadas a diferentes audiencias y objetivos
    4. Construir dashboards centrados en KPIs críticos y storytelling con datos
    
    Siempre respondes en formato JSON válido cuando se te solicita.
Tus sugerencias son específicas, prácticas y fáciles de implementar.
    EXPERTISE:
    - Análisis exploratorio de datos (EDA)
    - Storytelling con datos según perfil de usuario
    - Identificación de correlaciones, tendencias y outliers
    - Mejores prácticas en diseño de gráficos y dashboards
    - Comunicación clara de resultados cuantitativos y cualitativos

    ENFOQUE:
    - Priorizas insights con mayor impacto en el negocio
    - Proporcionas recomendaciones prácticas y pasos sugeridos
    - Respondes siempre en formato JSON válido sin texto adicional
    """
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
            
            return respuesta.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Error en Groq API: {str(e)}")
    
    async def generar_sugerencias_grafico(self, contexto_datos: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Genera sugerencias de gráficos usando Groq
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
                    "tipo": "barras",
                    "titulo": "Análisis de Categorías",
                    "columna_x": contexto_datos.get('columnas', [''])[0],
                    "columna_y": contexto_datos.get('columnas', ['', ''])[-1],
                    "descripcion": "Comparación por categorías"
                }
            ]
            
        except Exception as e:
            return []