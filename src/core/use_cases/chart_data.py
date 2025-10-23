"""
Caso de uso para datos de gráficos
"""
from typing import List, Dict, Any, Optional
from src.core.domain.entities import DatosGrafico
from src.core.services.chart_data_generator import GeneradorDatosGrafico
from src.infrastructure.persistence.in_memory_storage import AlmacenamientoMemoria

class CasoUsoDatosGrafico:
    """Caso de uso para generar datos de gráficos"""
    
    def __init__(
        self, 
        generador_graficos: GeneradorDatosGrafico,
        almacenamiento: Optional[AlmacenamientoMemoria] = None
    ):
        self.generador_graficos = generador_graficos
        self.almacenamiento = almacenamiento or AlmacenamientoMemoria()
    
    async def generar_datos_grafico_desde_archivo(
        self,
        id_archivo: str,
        tipo_grafico: str,
        eje_x: str,
        eje_y: str,
        titulo: str = None,
        agregacion: str = "suma"
    ) -> DatosGrafico:
        """
        Genera datos de gráfico desde un archivo almacenado.
        
        Este método recibe los parámetros del gráfico sugerido por la IA
        y retorna los datos ya agregados y formateados, listos para visualizar.
        Evita enviar todo el conjunto de datos crudos al cliente.
        """
        # Recuperar DataFrame del storage
        df = self.almacenamiento.obtener_dataframe(id_archivo)
        
        if df is None:
            raise ValueError(f"Archivo con ID {id_archivo} no encontrado")
        
        # Generar datos del gráfico
        datos_grafico = await self.generador_graficos.generar_desde_dataframe(
            dataframe=df,
            tipo_grafico=tipo_grafico,
            eje_x=eje_x,
            eje_y=eje_y,
            titulo=titulo,
            agregacion=agregacion
        )
        
        # Guardar en storage
        self.almacenamiento.guardar_grafico(datos_grafico.id_grafico, datos_grafico)
        
        return datos_grafico
    
    async def generar_datos_grafico(
        self,
        datos: List[Dict[str, Any]],
        tipo_grafico: str,
        columna_x: str,
        columna_y: str,
        titulo: str = None
    ) -> DatosGrafico:
        """Genera datos para gráfico desde datos raw"""
        return await self.generador_graficos.generar_datos_grafico(
            datos=datos,
            tipo_grafico=tipo_grafico,
            columna_x=columna_x,
            columna_y=columna_y,
            titulo=titulo
        )
    
    async def obtener_datos_grafico(self, id_grafico: str) -> Optional[DatosGrafico]:
        """Obtiene datos de gráfico por ID"""
        return self.almacenamiento.obtener_grafico(id_grafico)