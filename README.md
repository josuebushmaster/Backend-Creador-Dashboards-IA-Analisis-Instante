# Backend — dashboard_IA

Este es el backend del proyecto de dashboards con análisis asistido por IA. Está construido en Python con FastAPI y una arquitectura por capas sencilla de mantener.

## Empieza en 1 minuto (para quien llega nuevo)

## Estructura rápida

- `main.py` — Punto de entrada para levantar la API.
- `src/` — Código de la app:
  - `presentation/fastapi_app.py` y `presentation/api/routes/` — App y rutas FastAPI.
  - `core/` — Dominio y casos de uso (servicios, entidades, value objects).
  - `infrastructure/` — Adaptadores externos (OpenAI/Groq), configuración y persistencia en memoria.
- `scripts/` — Utilidades (p. ej. limpieza de `__pycache__`).
- `.env.example` — Plantilla de variables de entorno (no contiene secretos).

## Requisitos

- Python 3.10 o superior.
- Pip y un entorno virtual (recomendado).

## Configuración local

1. Moverse a la carpeta del proyecto:

```powershell
cd "d:\PRUEBAS Tecnicas\dashboard_IA\Backend"
```

1. Crear y activar un entorno virtual (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

1. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

1. Configurar variables de entorno (parte desde la plantilla):

```powershell
copy .env.example .env
# Abre .env y completa tus claves si vas a usar LLMs
# GROQ_API_KEY=...
# OPENAI_API_KEY=...
```

> Consejo: `.env` está ignorado por Git. La plantilla `.env.example` sí se versiona.

## Ejecutar el servidor

Opción simple (usa `main.py`):

```powershell
python main.py
```

También puedes lanzar con uvicorn directamente si lo prefieres:

```powershell
uvicorn src.presentation.fastapi_app:app --host 0.0.0.0 --port 8000 --reload
```

Rutas principales: revisa `src/presentation/api/routes/` para ver endpoints como `analysis`, `charts` y `sistema`.

## Tests y utilidades

- Ejecutar pruebas (si tienes pytest instalado):

  ```powershell
  pytest -q
  ```

- Limpiar carpetas `__pycache__` (dry‑run):

  ```powershell
  .\scripts\clean_pycache.ps1 -WhatIf
  # ó
  python .\scripts\clean_pycache.py --path .
  ```

- Limpiar de verdad:

  ```powershell
  .\scripts\clean_pycache.ps1
  # ó
  python .\scripts\clean_pycache.py --path . --delete
  ```

## Documentación de la API

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

Explora ahí los endpoints disponibles (por ejemplo, los definidos en `src/presentation/api/routes/analysis.py`, `charts.py` y `sistema.py`).

## Decisiones técnicas (detalladas)

Abajo detallo las decisiones técnicas que tomé, por qué las escogí, dónde están implementadas y recomendaciones/próximos pasos.

1) Framework web: FastAPI
 - Por qué: rendimiento, tipado (type hints), documentación automática (Swagger / ReDoc) y buena ergonomía para APIs modernas.
 - Dónde: `src/presentation/fastapi_app.py`, rutas en `src/presentation/api/routes/`.
 - Trade-offs: más adecuado para APIs que para páginas server-side complejas. Si el proyecto requiere features típicas de un CMS/admin, considerar Django.
 - Recomendación: documentar ejemplos de request/response en los modelos Pydantic.

2) Validación y modelos: Pydantic
 - Por qué: validación declarativa, parsing y generación automática de esquemas OpenAPI.
 - Dónde: `src/presentation/api/models/requests.py` y usos en los routers.
 - Recomendación: mantener los modelos pequeños y composables; añadir ejemplos con `schema_extra` si hace falta.

3) Arquitectura por capas / separación de responsabilidades
 - Por qué: aislar lógica de negocio (core) de detalles de infraestructura y presentación para facilitar tests y cambios futuros.
 - Capas:
   - Presentation: `src/presentation/` (FastAPI, modelos, routers, middleware).
   - Core/Domain: `src/core/` (entidades, value objects, servicios/casos de uso).
   - Infrastructure: `src/infrastructure/` (container, config, adaptadores externos, persistencia).
 - Recomendación: mantener el core libre de imports de FastAPI o librerías de infra.

4) Inyección de dependencias / Container
 - Por qué: centralizar creación de clientes/adapters, facilitar mocks en tests y cambiar implementaciones sin tocar la lógica.
 - Dónde: `src/infrastructure/container.py` y `src/presentation/api/dependencies.py`.
 - Recomendación: exponer factories simples y evitar singletons globales complejos.

5) Adaptadores para LLMs y contratos
 - Por qué: desacoplar proveedores (Groq, OpenAI) mediante contratos para poder cambiar proveedor o mockearlo en tests.
 - Dónde: `src/infrastructure/external/interfaces.py`, `groq_client.py`, `openai_client.py`.
 - Recomendación: implementar timeouts, retries y manejo de errores en los adaptadores; no propagar excepciones crudas al cliente HTTP.

6) Persistencia: in-memory storage (temporal)
 - Por qué: arranque rápido y facilidad para tests locales sin infra adicional.
 - Dónde: `src/infrastructure/persistence/in_memory_storage.py`.
 - Trade-offs: no persistente ni distribuible; planificar migración a una BD (Postgres, SQLite, Redis) si se requiere durabilidad/escala.

7) Configuración y seguridad de entorno
 - Por qué: evitar subir secretos y centralizar configuración.
 - Dónde: `.env.example` (plantilla) y `src/infrastructure/config/settings.py` (carga/validación).
 - Recomendación: para producción usar secret manager (Vault, AWS Secrets Manager) y no confiar en `.env` con claves sensibles.

8) Documentación de la API
 - Por qué: facilita coordinación con frontend y pruebas manuales.
 - Dónde: FastAPI expone `/docs` (Swagger) y `/redoc` (ReDoc) automáticamente.
 - Recomendación: añadir ejemplos y modelos de respuesta en los schemas Pydantic.

9) Tests y estrategia
 - Por qué: permitir cambios seguros y regresiones controladas.
 - Recomendación: usar `pytest`, mocks para adaptadores externos y `TestClient` de FastAPI para tests de integración. Mantener `in_memory_storage` para tests unitarios y añadir tests que cubran fallos de adaptadores externos.

10) Dev tooling y tareas
 - Inclusiones: `scripts/clean_pycache.*` y `.vscode/tasks.json` para acelerar tareas de desarrollo.
 - Recomendación: añadir CI (GitHub Actions) para ejecutar lint + tests en PRs.

11) Logs, timeouts y robustez
 - Recomendación crítica: implementar timeouts en llamadas externas (por ejemplo `httpx` con timeout), retries (tenacity) y límites de concurrencia si el LLM es punto caliente.

12) Manejo de errores
 - Dónde: `src/core/domain/exceptions.py` para excepciones de dominio; traducirlas a respuestas HTTP en routers o middleware.
 - Recomendación: centralizar handlers para mapear excepciones a códigos HTTP claros y mensajes seguros.

Si quieres, inserto una versión resumida de estas decisiones en la parte superior del README para que sea visible en la vista rápida. También puedo generar un snippet de ejemplo (router + servicio + test) que implemente estas prácticas.

## Notas

- `.gitignore` permite subir `.env.example` pero bloquea `.env` y otros archivos sensibles.
- Si algo no levanta, revisa que el entorno esté activado y las variables de `.env` estén definidas.

## Solución de problemas frecuentes

- PowerShell no permite activar el entorno virtual:

  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```

- Error instalando dependencias: prueba a actualizar pip e instalar de nuevo.

  ```powershell
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  ```

- Puerto 8000 ocupado: cambia el puerto en `.env` (PORT) o al lanzar uvicorn con `--port 8001`.

---

## Arquitectura del proyecto (árbol)

Aquí tienes un diagrama en forma de árbol con las carpetas y los archivos más relevantes, seguido de una breve explicación de cada elemento para que cualquier desarrollador nuevo entienda dónde está cada cosa.

```text
.
├─ .env.example                    — Plantilla de variables de entorno (no contiene secretos).
├─ main.py                         — Punto de entrada: inicializa configuración y arranca la app.
├─ requirements.txt                — Lista de dependencias Python del proyecto.
├─ scripts/                        — Scripts de utilidades del repositorio.
│  ├─ clean_pycache.py             — Python: busca y lista/borra `__pycache__` (--delete para borrar).
│  └─ clean_pycache.ps1            — PowerShell: versión para Windows con opciones -WhatIf/-Confirm.
├─ src/                            — Código fuente principal.
│  ├─ __init__.py                  — Marca el paquete `src`.
│  ├─ presentation/                — Capa de presentación (FastAPI).
│  │  ├─ __init__.py
│  │  ├─ fastapi_app.py            — Crea y configura la app FastAPI, monta routers y middlewares.
│  │  └─ api/
│  │     ├─ __init__.py
│  │     ├─ dependencies.py        — Dependencias de endpoints (inyección del container, etc.).
│  │     ├─ middleware/
│  │     │  └─ cors.py             — Configuración CORS para la API.
│  │     ├─ models/
│  │     │  └─ requests.py         — Modelos Pydantic para validar solicitudes entrantes.
│  │     └─ routes/
│  │        ├─ __init__.py
│  │        ├─ analysis.py         — Endpoints para análisis de datos (AI-driven).
│  │        ├─ charts.py           — Endpoints para generación/consulta de datos de gráficos.
│  │        └─ sistema.py          — Endpoints de sistema/health checks.
│  ├─ core/                        — Lógica de negocio y casos de uso.
│  │  ├─ __init__.py
│  │  ├─ domain/
│  │  │  ├─ __init__.py
│  │  │  ├─ entities.py            — Entidades del dominio (modelos de negocio).
│  │  │  ├─ exceptions.py          — Excepciones específicas del dominio.
│  │  │  ├─ repositories.py        — Interfaces/contratos para repositorios.
│  │  │  └─ value_objects.py       — Objetos de valor del dominio.
│  │  └─ services/
│  │     ├─ __init__.py
│  │     ├─ ai_analysis.py         — Lógica que orquesta llamadas a LLMs y procesa respuestas.
│  │     ├─ chart_data_generator.py— Genera la estructura de datos para los charts.
│  │     └─ file_processing.py     — Procesamiento/validación de archivos de entrada (CSV, etc.).
│  └─ infrastructure/               — Adaptadores externos, configuración y persistencia.
│     ├─ __init__.py
│     ├─ container.py              — Registro/ensamblaje de dependencias (IoC container).
│     ├─ config/
│     │  ├─ __init__.py
│     │  └─ settings.py            — Carga y validación de variables de entorno (.env).
│     ├─ external/
│     │  ├─ __init__.py
│     │  ├─ groq_client.py         — Cliente/adapter para Groq (consulta LLM/API).
│     │  ├─ openai_client.py       — Cliente/adapter para OpenAI.
│     │  └─ interfaces.py          — Contratos comunes que deben cumplir los clientes externos.
│     └─ persistence/
│        ├─ __init__.py
│        └─ in_memory_storage.py   — Implementación simple de almacenamiento en memoria (tests/prototipos).
└─ .vscode/
  └─ tasks.json                    — Tareas de VS Code (start, tests, limpiar pycache).
```

Explicación por carpeta/archivo

- `.env.example`: plantilla con las variables de entorno necesarias (no contiene secretos). Usa `copy .env.example .env` y rellena tus claves.
- `main.py`: punto de entrada que arranca la aplicación (carga configuración, container y servidor).
- `requirements.txt`: dependencias del proyecto.

- `scripts/`: utilidades para mantenimiento del repo.
  - `clean_pycache.py`, `clean_pycache.ps1`: scripts para borrar carpetas `__pycache__` (dry-run y delete).

- `src/`: código fuente principal.
  - `presentation/`: capa que expone la API (FastAPI).
    - `fastapi_app.py`: crea la app FastAPI y monta rutas y middlewares.
    - `api/routes/`: definición de endpoints por responsabilidad (analysis, charts, sistema).
    - `api/models/requests.py`: modelos Pydantic que representan las solicitudes entrantes.
    - `api/dependencies.py`: dependencias de FastAPI (por ejemplo, inyección de servicios desde el container).
    - `api/middleware/cors.py`: configuración CORS.

  - `core/`: lógica de negocio y casos de uso.
    - `domain/`: entidades del dominio, objetos de valor, repositorios y excepciones.
    - `services/`: implementaciones de casos de uso y coordinación entre componentes (AI analysis, generación de chart data, procesamiento de archivos).

  - `infrastructure/`: adaptadores y configuración.
    - `container.py`: registro de dependencias e instanciación de clientes y repositorios.
    - `config/settings.py`: carga y valida variables de entorno.
    - `external/`: adaptadores a servicios externos (Groq, OpenAI). `interfaces.py` define contratos para los clientes.
    - `persistence/in_memory_storage.py`: implementación simple de almacenamiento para pruebas y prototipos.

- `.vscode/tasks.json`: tareas predefinidas para VS Code (iniciar servidor, tests, limpiar pycache).
- creado por Josue Pastil, desarrollador full stack
- www.linkedin.com/in/josué-pastil-b98753196
