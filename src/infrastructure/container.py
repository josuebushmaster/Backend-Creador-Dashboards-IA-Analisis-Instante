"""
Sugerencia: Container de Dependencias
"""
from typing import Protocol
from src.core.use_cases.file_analysis import FileAnalysisUseCase
from src.infrastructure.external.groq_client import GroqClient
from src.infrastructure.persistence.in_memory_storage import InMemoryStorage

class Container:
    """Container de dependencias siguiendo principios SOLID"""
    
    def __init__(self):
        # Infrastructure
        self._storage = InMemoryStorage()
        self._ai_client = GroqClient()
        
        # Use Cases
        self._file_analysis_use_case = None
    
    @property
    def file_analysis_use_case(self) -> FileAnalysisUseCase:
        if self._file_analysis_use_case is None:
            self._file_analysis_use_case = FileAnalysisUseCase(
                ai_client=self._ai_client,
                storage=self._storage
            )
        return self._file_analysis_use_case

# Singleton global
container = Container()