"""
Generador de datos para gráficos
"""
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from src.core.domain.entities import DatosGrafico
from src.core.domain.exceptions import ErrorGeneracionGrafico

class GeneradorDatosGrafico:
    """Servicio para generar datos de gráficos"""
    
    def __init__(self, almacenamiento=None):
        self.almacenamiento = almacenamiento
    
    async def generar_desde_dataframe(
        self,
        dataframe: pd.DataFrame,
        tipo_grafico: str,
        eje_x: str,
        eje_y: str,
        titulo: str = None,
        agregacion: str = "suma"
    ) -> DatosGrafico:
        """
        Genera datos de gráfico desde un DataFrame.
        
        Los datos son agregados y formateados según el tipo de gráfico,
        evitando enviar datos crudos completos al cliente.
        """
        try:
            # Validar columnas
            if eje_x not in dataframe.columns:
                raise ErrorGeneracionGrafico(f"Columna {eje_x} no encontrada en los datos")
            
            if eje_y not in dataframe.columns and eje_y != "conteo":
                raise ErrorGeneracionGrafico(f"Columna {eje_y} no encontrada en los datos")
            
            # Crear copia del dataframe para no modificar el original
            df_trabajo = dataframe.copy()
            
            # Procesar datos según tipo de gráfico y agregación
            datos_procesados = self._procesar_datos_por_tipo_grafico(
                df_trabajo, 
                tipo_grafico, 
                eje_x, 
                eje_y,
                agregacion
            )
            
            # Generar configuración del gráfico
            configuracion = self._generar_configuracion_grafico(tipo_grafico, eje_x, eje_y, titulo)
            
            # Metadata
            metadatos = {
                "total_registros": len(dataframe),
                "registros_procesados": len(datos_procesados),
                "eje_x": eje_x,
                "eje_y": eje_y,
                "tipo_grafico": tipo_grafico,
                "agregacion": agregacion
            }
            
            return DatosGrafico.crear(
                tipo_grafico=tipo_grafico,
                datos=datos_procesados,
                configuracion=configuracion,
                metadatos=metadatos
            )
            
        except Exception as e:
            raise ErrorGeneracionGrafico(f"Error generando gráfico: {str(e)}")
    
    async def generar_datos_grafico(
        self, 
        datos: List[Dict[str, Any]], 
        tipo_grafico: str,
        columna_x: str,
        columna_y: str,
        titulo: str = None
    ) -> DatosGrafico:
        """
        Genera datos procesados para gráfico desde lista de diccionarios
        """
        try:
            df = pd.DataFrame(datos)
            
            # Validar columnas
            if columna_x not in df.columns or columna_y not in df.columns:
                raise ErrorGeneracionGrafico(f"Columnas {columna_x} o {columna_y} no encontradas")
            
            # Procesar datos según tipo de gráfico
            datos_procesados = self._procesar_datos_por_tipo_grafico(
                df, 
                tipo_grafico, 
                columna_x, 
                columna_y,
                "suma"
            )
            
            # Generar configuración del gráfico
            configuracion = self._generar_configuracion_grafico(tipo_grafico, columna_x, columna_y, titulo)
            
            # Metadata
            metadatos = {
                "total_registros": len(df),
                "columna_x": columna_x,
                "columna_y": columna_y,
                "tipo_grafico": tipo_grafico
            }
            
            return DatosGrafico.crear(
                tipo_grafico=tipo_grafico,
                datos=datos_procesados,
                configuracion=configuracion,
                metadatos=metadatos
            )
            
        except Exception as e:
            raise ErrorGeneracionGrafico(f"Error generando gráfico: {str(e)}")
    
    def _procesar_datos_por_tipo_grafico(
        self, 
        df: pd.DataFrame, 
        tipo_grafico: str, 
        columna_x: str, 
        columna_y: str,
        agregacion: str = "suma"
    ) -> List[Dict[str, Any]]:
        """Procesa datos según el tipo de gráfico"""
        
        if tipo_grafico == "barras":
            return self._procesar_grafico_barras(df, columna_x, columna_y, agregacion)
        elif tipo_grafico == "lineas":
            return self._procesar_grafico_lineas(df, columna_x, columna_y, agregacion)
        elif tipo_grafico == "pastel":
            return self._procesar_grafico_pastel(df, columna_x, columna_y, agregacion)
        elif tipo_grafico == "dispersion":
            return self._procesar_grafico_dispersion(df, columna_x, columna_y)
        elif tipo_grafico == "area":
            return self._procesar_grafico_area(df, columna_x, columna_y, agregacion)
        else:
            raise ErrorGeneracionGrafico(f"Tipo de gráfico no soportado: {tipo_grafico}")
    
    def _agregar_datos(self, df: pd.DataFrame, columna_x: str, columna_y: str, agregacion: str) -> pd.DataFrame:
        """Agrega datos según el tipo de agregación especificado"""
        if columna_y == "conteo":
            return df.groupby(columna_x).size().reset_index(name='conteo')
        
        # Validar que la columna Y sea numérica (excepto para conteo)
        if agregacion != "conteo":
            # Intentar convertir a numérico, si falla usar conteo
            try:
                df[columna_y] = pd.to_numeric(df[columna_y], errors='coerce')
            except Exception:
                pass
            
            # Si la columna no es numérica o tiene muchos valores no numéricos, usar conteo
            if df[columna_y].dtype == 'object' or df[columna_y].isna().sum() > len(df) * 0.5:
                return df.groupby(columna_x).size().reset_index(name='conteo')
        
        if agregacion == "suma":
            return df.groupby(columna_x)[columna_y].sum().reset_index()
        elif agregacion == "promedio" or agregacion == "media":
            return df.groupby(columna_x)[columna_y].mean().reset_index()
        elif agregacion == "conteo":
            return df.groupby(columna_x)[columna_y].count().reset_index()
        elif agregacion == "minimo":
            return df.groupby(columna_x)[columna_y].min().reset_index()
        elif agregacion == "maximo":
            return df.groupby(columna_x)[columna_y].max().reset_index()
        else:
            return df.groupby(columna_x)[columna_y].sum().reset_index()
    
    def _procesar_grafico_barras(
        self, 
        df: pd.DataFrame, 
        columna_x: str, 
        columna_y: str,
        agregacion: str
    ) -> List[Dict[str, Any]]:
        """Procesa datos para gráfico de barras con agregación"""
        agrupado = self._agregar_datos(df, columna_x, columna_y, agregacion)
        
        # Limitar a top 20 para evitar sobrecarga visual
        if len(agrupado) > 20:
            columna_valor = agrupado.columns[-1]
            # Asegurar que la columna es numérica antes de usar nlargest
            try:
                agrupado[columna_valor] = pd.to_numeric(agrupado[columna_valor], errors='coerce').fillna(0)
                agrupado = agrupado.nlargest(20, columna_valor)
            except Exception:
                # Si falla, tomar las primeras 20
                agrupado = agrupado.head(20)
        
        return agrupado.to_dict('records')
    
    def _procesar_grafico_lineas(
        self, 
        df: pd.DataFrame, 
        columna_x: str, 
        columna_y: str,
        agregacion: str
    ) -> List[Dict[str, Any]]:
        """Procesa datos para gráfico de líneas"""
        agrupado = self._agregar_datos(df, columna_x, columna_y, agregacion)
        df_ordenado = agrupado.sort_values(columna_x)
        return df_ordenado.to_dict('records')
    
    def _procesar_grafico_pastel(
        self, 
        df: pd.DataFrame, 
        columna_x: str, 
        columna_y: str,
        agregacion: str
    ) -> List[Dict[str, Any]]:
        """Procesa datos para gráfico circular"""
        agrupado = self._agregar_datos(df, columna_x, columna_y, agregacion)
        
        # Limitar a top 10 para gráficos circulares
        if len(agrupado) > 10:
            agrupado = agrupado.nlargest(10, agrupado.columns[-1])
        
        # Calcular total y porcentajes (asegurar tipo numérico)
        columna_valor = agrupado.columns[-1]
        try:
            # Convertir a numérico si no lo es
            agrupado[columna_valor] = pd.to_numeric(agrupado[columna_valor], errors='coerce').fillna(0)
            total = agrupado[columna_valor].sum()
            
            if total > 0:
                agrupado['porcentaje'] = (agrupado[columna_valor] / total * 100).round(2)
            else:
                agrupado['porcentaje'] = 0
        except Exception as e:
            # Si falla el cálculo de porcentaje, usar valores absolutos
            agrupado['porcentaje'] = 0
        
        return agrupado.to_dict('records')
    
    def _procesar_grafico_dispersion(
        self, 
        df: pd.DataFrame, 
        columna_x: str, 
        columna_y: str
    ) -> List[Dict[str, Any]]:
        """Procesa datos para gráfico de dispersión"""
        # Para scatter no agregamos, mostramos puntos individuales
        # Pero limitamos a 1000 puntos para performance
        df_dispersion = df[[columna_x, columna_y]].dropna()
        if len(df_dispersion) > 1000:
            df_dispersion = df_dispersion.sample(n=1000, random_state=42)
        return df_dispersion.to_dict('records')
    
    def _procesar_grafico_area(
        self, 
        df: pd.DataFrame, 
        columna_x: str, 
        columna_y: str,
        agregacion: str
    ) -> List[Dict[str, Any]]:
        """Procesa datos para gráfico de área"""
        agrupado = self._agregar_datos(df, columna_x, columna_y, agregacion)
        df_ordenado = agrupado.sort_values(columna_x)
        return df_ordenado.to_dict('records')
    
    def _generar_configuracion_grafico(
        self, 
        tipo_grafico: str, 
        columna_x: str, 
        columna_y: str, 
        titulo: str = None
    ) -> Dict[str, Any]:
        """Genera configuración del gráfico"""
        configuracion = {
            "tipo": tipo_grafico,
            "titulo": titulo or f"{columna_y} por {columna_x}",
            "ejeX": {
                "etiqueta": columna_x,
                "tipo": "categoria" if tipo_grafico in ["barras", "pastel"] else "lineal"
            },
            "ejeY": {
                "etiqueta": columna_y,
                "tipo": "lineal"
            },
            "responsivo": True,
            "mantenerRelacionAspecto": False,
            "animacion": True
        }
        
        # Configuraciones específicas por tipo
        if tipo_grafico == "pastel":
            configuracion["leyenda"] = {"posicion": "derecha"}
            configuracion["mostrarEtiquetas"] = True
        elif tipo_grafico == "lineas" or tipo_grafico == "area":
            configuracion["suave"] = True
            configuracion["relleno"] = tipo_grafico == "area"
        elif tipo_grafico == "dispersion":
            configuracion["mostrarLinea"] = False
            configuracion["radioP unto"] = 4
        elif tipo_grafico == "barras":
            configuracion["horizontal"] = False
            configuracion["apilado"] = False
        
        return configuracion