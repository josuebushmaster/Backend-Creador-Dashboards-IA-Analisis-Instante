"""
Entidades de dominio para el dashboard IA
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

@dataclass
class FileData:
    """Entidad para datos de archivo"""
    file_id: str
    filename: str
    file_type: str
    content: bytes
    uploaded_at: datetime
    size: int
    
    @classmethod
    def create(cls, filename: str, content: bytes, file_type: str) -> 'FileData':
        return cls(
            file_id=str(uuid.uuid4()),
            filename=filename,
            file_type=file_type,
            content=content,
            uploaded_at=datetime.now(),
            size=len(content)
        )

@dataclass
class AnalysisResult:
    """Entidad para resultado de análisis"""
    analysis_id: str
    file_id: str
    summary: str
    insights: List[str]
    chart_suggestions: List[Dict[str, Any]]
    created_at: datetime
    status: str
    
    @classmethod
    def create(cls, file_id: str, summary: str, insights: List[str], 
               chart_suggestions: List[Dict[str, Any]]) -> 'AnalysisResult':
        return cls(
            analysis_id=str(uuid.uuid4()),
            file_id=file_id,
            summary=summary,
            insights=insights,
            chart_suggestions=chart_suggestions,
            created_at=datetime.now(),
            status="completed"
        )

@dataclass
class ChartData:
    """Entidad para datos de gráfico"""
    chart_id: str
    chart_type: str
    data: List[Dict[str, Any]]
    config: Dict[str, Any]
    metadata: Dict[str, Any]
    created_at: datetime
    
    @classmethod
    def create(cls, chart_type: str, data: List[Dict[str, Any]], 
               config: Dict[str, Any], metadata: Dict[str, Any]) -> 'ChartData':
        return cls(
            chart_id=str(uuid.uuid4()),
            chart_type=chart_type,
            data=data,
            config=config,
            metadata=metadata,
            created_at=datetime.now()
        )