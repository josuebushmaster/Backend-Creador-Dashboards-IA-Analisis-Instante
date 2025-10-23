"""
Generador de datos para gráficos
"""
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from src.core.domain.entities import ChartData
from src.core.domain.exceptions import ChartGenerationError

class ChartDataGenerator:
    """Servicio para generar datos de gráficos"""
    
    def __init__(self, storage=None):
        self.storage = storage
    
    async def generate_from_dataframe(
        self,
        dataframe: pd.DataFrame,
        chart_type: str,
        x_axis: str,
        y_axis: str,
        title: str = None,
        aggregation: str = "sum"
    ) -> ChartData:
        """
        Genera datos de gráfico desde un DataFrame.
        
        Los datos son agregados y formateados según el tipo de gráfico,
        evitando enviar datos crudos completos al cliente.
        """
        try:
            # Validar columnas
            if x_axis not in dataframe.columns:
                raise ChartGenerationError(f"Columna {x_axis} no encontrada en los datos")
            
            if y_axis not in dataframe.columns and y_axis != "count":
                raise ChartGenerationError(f"Columna {y_axis} no encontrada en los datos")
            
            # Procesar datos según tipo de gráfico y agregación
            processed_data = self._process_data_by_chart_type(
                dataframe, 
                chart_type, 
                x_axis, 
                y_axis,
                aggregation
            )
            
            # Generar configuración del gráfico
            config = self._generate_chart_config(chart_type, x_axis, y_axis, title)
            
            # Metadata
            metadata = {
                "total_records": len(dataframe),
                "processed_records": len(processed_data),
                "x_axis": x_axis,
                "y_axis": y_axis,
                "chart_type": chart_type,
                "aggregation": aggregation
            }
            
            return ChartData.create(
                chart_type=chart_type,
                data=processed_data,
                config=config,
                metadata=metadata
            )
            
        except Exception as e:
            raise ChartGenerationError(f"Error generando gráfico: {str(e)}")
    
    async def generate_chart_data(
        self, 
        data: List[Dict[str, Any]], 
        chart_type: str,
        x_column: str,
        y_column: str,
        title: str = None
    ) -> ChartData:
        """
        Genera datos procesados para gráfico desde lista de diccionarios
        """
        try:
            df = pd.DataFrame(data)
            
            # Validar columnas
            if x_column not in df.columns or y_column not in df.columns:
                raise ChartGenerationError(f"Columnas {x_column} o {y_column} no encontradas")
            
            # Procesar datos según tipo de gráfico
            processed_data = self._process_data_by_chart_type(
                df, 
                chart_type, 
                x_column, 
                y_column,
                "sum"
            )
            
            # Generar configuración del gráfico
            config = self._generate_chart_config(chart_type, x_column, y_column, title)
            
            # Metadata
            metadata = {
                "total_records": len(df),
                "x_column": x_column,
                "y_column": y_column,
                "chart_type": chart_type
            }
            
            return ChartData.create(
                chart_type=chart_type,
                data=processed_data,
                config=config,
                metadata=metadata
            )
            
        except Exception as e:
            raise ChartGenerationError(f"Error generando gráfico: {str(e)}")
    
    def _process_data_by_chart_type(
        self, 
        df: pd.DataFrame, 
        chart_type: str, 
        x_column: str, 
        y_column: str,
        aggregation: str = "sum"
    ) -> List[Dict[str, Any]]:
        """Procesa datos según el tipo de gráfico"""
        
        if chart_type == "bar":
            return self._process_bar_chart(df, x_column, y_column, aggregation)
        elif chart_type == "line":
            return self._process_line_chart(df, x_column, y_column, aggregation)
        elif chart_type == "pie":
            return self._process_pie_chart(df, x_column, y_column, aggregation)
        elif chart_type == "scatter":
            return self._process_scatter_chart(df, x_column, y_column)
        elif chart_type == "area":
            return self._process_area_chart(df, x_column, y_column, aggregation)
        else:
            raise ChartGenerationError(f"Tipo de gráfico no soportado: {chart_type}")
    
    def _aggregate_data(self, df: pd.DataFrame, x_column: str, y_column: str, aggregation: str) -> pd.DataFrame:
        """Agrega datos según el tipo de agregación especificado"""
        if y_column == "count":
            return df.groupby(x_column).size().reset_index(name='count')
        
        if aggregation == "sum":
            return df.groupby(x_column)[y_column].sum().reset_index()
        elif aggregation == "avg" or aggregation == "mean":
            return df.groupby(x_column)[y_column].mean().reset_index()
        elif aggregation == "count":
            return df.groupby(x_column)[y_column].count().reset_index()
        elif aggregation == "min":
            return df.groupby(x_column)[y_column].min().reset_index()
        elif aggregation == "max":
            return df.groupby(x_column)[y_column].max().reset_index()
        else:
            return df.groupby(x_column)[y_column].sum().reset_index()
    
    def _process_bar_chart(
        self, 
        df: pd.DataFrame, 
        x_column: str, 
        y_column: str,
        aggregation: str
    ) -> List[Dict[str, Any]]:
        """Procesa datos para gráfico de barras con agregación"""
        grouped = self._aggregate_data(df, x_column, y_column, aggregation)
        # Limitar a top 20 para evitar sobrecarga visual
        if len(grouped) > 20:
            grouped = grouped.nlargest(20, grouped.columns[-1])
        return grouped.to_dict('records')
    
    def _process_line_chart(
        self, 
        df: pd.DataFrame, 
        x_column: str, 
        y_column: str,
        aggregation: str
    ) -> List[Dict[str, Any]]:
        """Procesa datos para gráfico de líneas"""
        grouped = self._aggregate_data(df, x_column, y_column, aggregation)
        sorted_df = grouped.sort_values(x_column)
        return sorted_df.to_dict('records')
    
    def _process_pie_chart(
        self, 
        df: pd.DataFrame, 
        x_column: str, 
        y_column: str,
        aggregation: str
    ) -> List[Dict[str, Any]]:
        """Procesa datos para gráfico circular"""
        grouped = self._aggregate_data(df, x_column, y_column, aggregation)
        
        # Limitar a top 10 para gráficos circulares
        if len(grouped) > 10:
            grouped = grouped.nlargest(10, grouped.columns[-1])
        
        total = grouped[grouped.columns[-1]].sum()
        grouped['percentage'] = (grouped[grouped.columns[-1]] / total * 100).round(2)
        return grouped.to_dict('records')
    
    def _process_scatter_chart(
        self, 
        df: pd.DataFrame, 
        x_column: str, 
        y_column: str
    ) -> List[Dict[str, Any]]:
        """Procesa datos para gráfico de dispersión"""
        # Para scatter no agregamos, mostramos puntos individuales
        # Pero limitamos a 1000 puntos para performance
        scatter_df = df[[x_column, y_column]].dropna()
        if len(scatter_df) > 1000:
            scatter_df = scatter_df.sample(n=1000, random_state=42)
        return scatter_df.to_dict('records')
    
    def _process_area_chart(
        self, 
        df: pd.DataFrame, 
        x_column: str, 
        y_column: str,
        aggregation: str
    ) -> List[Dict[str, Any]]:
        """Procesa datos para gráfico de área"""
        grouped = self._aggregate_data(df, x_column, y_column, aggregation)
        sorted_df = grouped.sort_values(x_column)
        return sorted_df.to_dict('records')
    
    def _generate_chart_config(
        self, 
        chart_type: str, 
        x_column: str, 
        y_column: str, 
        title: str = None
    ) -> Dict[str, Any]:
        """Genera configuración del gráfico"""
        config = {
            "type": chart_type,
            "title": title or f"{y_column} por {x_column}",
            "xAxis": {
                "label": x_column,
                "type": "category" if chart_type in ["bar", "pie"] else "linear"
            },
            "yAxis": {
                "label": y_column,
                "type": "linear"
            },
            "responsive": True,
            "maintainAspectRatio": False,
            "animation": True
        }
        
        # Configuraciones específicas por tipo
        if chart_type == "pie":
            config["legend"] = {"position": "right"}
            config["showLabels"] = True
        elif chart_type == "line" or chart_type == "area":
            config["smooth"] = True
            config["fill"] = chart_type == "area"
        elif chart_type == "scatter":
            config["showLine"] = False
            config["pointRadius"] = 4
        elif chart_type == "bar":
            config["horizontal"] = False
            config["stacked"] = False
        
        return config