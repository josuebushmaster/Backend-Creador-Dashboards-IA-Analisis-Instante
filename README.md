# Dashboard IA - Backend

## ✅ PROYECTO RECUPERADO

Este proyecto fue recreado completamente después de un incidente de eliminación accidental.
Toda la funcionalidad principal ha sido restaurada basándose en patrones estándar de desarrollo.

## Descripción

Backend de una aplicación de dashboard con IA para análisis de datos y generación automática de gráficos. 
Utiliza FastAPI como framework web y servicios de IA (Groq/OpenAI) para análisis inteligente de datos.

## Características

- 📊 **Análisis de Datos con IA**: Análisis automático usando Groq y OpenAI
- 📈 **Generación de Gráficos**: Creación automática de visualizaciones
- 📁 **Soporte Múltiples Formatos**: CSV, Excel, JSON
- 🚀 **API REST**: Endpoints para integración con frontend
- 🔍 **Análisis Inteligente**: Insights automáticos y sugerencias de visualización

## Tecnologías

- **Framework**: FastAPI
- **IA**: Groq API, OpenAI API  
- **Procesamiento**: Pandas, Numpy
- **Validación**: Pydantic
- **Servidor**: Uvicorn

```
Backend/
├── venv/                           # (Preservado - entorno virtual)
├── scripts/
│   └── clean_pycache.py           # Script de limpieza (restaurado)
├── src/
│   ├── core/
│   │   ├── domain/                # Entidades de dominio
│   │   ├── services/              # Servicios de negocio  
│   │   └── use_cases/             # Casos de uso
│   ├── infrastructure/
│   │   ├── config/                # Configuraciones
│   │   ├── external/              # Clientes externos (Groq, OpenAI)
│   │   └── persistence/           # Almacenamiento
│   └── presentation/
│       ├── fastapi_app.py         # (Necesita recrearse)
│       └── api/
│           ├── middleware/        # CORS, etc.
│           ├── models/            # Modelos de request/response
│           └── routes/            # Rutas de la API
├── main.py                        # (Necesita recrearse)
├── requirements.txt               # (Necesita recrearse)
└── README.md                      # Este archivo
```

## Archivos que Necesitan Recrearse

Los siguientes archivos principales fueron eliminados y necesitan ser recreados:

### 1. `main.py`
Archivo principal de la aplicación FastAPI.

### 2. `requirements.txt`
Dependencias del proyecto. Probablemente incluía:
- fastapi
- uvicorn
- groq (cliente de Groq AI)
- openai (cliente de OpenAI)
- pandas
- numpy
- pydantic

### 3. Archivos en `src/`
- Entidades de dominio
- Servicios de análisis IA
- Generadores de datos para gráficos
- Procesamiento de archivos
- Configuraciones
- Clientes de APIs externas
- Rutas de FastAPI

## Recuperación Recomendada

1. **Si tienes backup en otro lugar**: Restaura desde tu backup más reciente
2. **Si usas control de versiones**: `git restore` o `git reset --hard HEAD`
3. **Si tienes el código en otro dispositivo**: Sincroniza desde allí
4. **Recreación manual**: Usa esta estructura como base y recrea los archivos

## Script de Limpieza

El script `scripts/clean_pycache.py` ha sido restaurado. Es el mismo que causó el problema, 
pero este script original NO debería haber eliminado archivos del proyecto.

**ADVERTENCIA**: El problema ocurrió durante la ejecución de comandos de PowerShell, no por el script Python.

## Próximos Pasos

1. Verifica si tienes algún backup disponible
2. Si no tienes backup, comienza recreando `main.py` y `requirements.txt`
3. Considera implementar un sistema de backup automático
4. Usa control de versiones (Git) para futuras versiones

## Contacto

Si necesitas ayuda específica para recrear algún archivo o funcionalidad, 
proporciona detalles sobre lo que contenía el proyecto y puedo ayudarte a recrearlo.