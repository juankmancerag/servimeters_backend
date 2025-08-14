Descripción general

Este repositorio es una versión muy temprana del backend para “Servimeters”.
La mayoría de los archivos son solo andamiaje (scaffolding), pero las partes implementadas se enfocan en:

Ejecutar un flujo de orquestación de agentes por línea de comandos.

Usar servicios de AWS (Bedrock, DynamoDB, S3) para almacenar y recuperar datos.

Demostrar una habilidad de ejemplo para interpretar resultados de la prueba psicológica WISC.

servimeters_backend/
├── main.py                  # Punto de entrada CLI
├── config/                  # Constantes globales (AWS, Bedrock, nombres de tablas…)
├── src/
│   ├── agents/              # Orquestación LLM, herramientas y habilidades de dominio
│   ├── utils/               # Ayudantes para DynamoDB y S3
│   ├── handlers/            # Actualmente vacío (posible lugar para handlers de AWS Lambda)
│   └── tests/               # Datos de ejemplo y script de prueba manual
└── docs/, serverless.yml, requirements.txt  # Presentes pero vacíos

Componentes clave
1. Punto de entrada CLI

main.py lanza un bucle interactivo que envía mensajes del usuario a un agente “Servimeters” impulsado por un orquestador (src/agents/agents/agente_orquestador.py).

El orquestador construye un BedrockModel (Anthropic Haiku) y delega en herramientas para:

Obtener resúmenes de órdenes.

Asignar inspectores a órdenes (herramienta aún no implementada).

Evaluar los resultados de las asignaciones.

2. Herramientas y habilidades del agente

Herramientas (src/agents/tools/agents_tools.py):

obtener_resumen_ordenes: lee órdenes en DynamoDB y agrega totales por servicio y ciudad.

obtener_inspectores_fijos: devuelve una lista fija de inspectores.

generar_disponibilidad_tool: genera bloques de disponibilidad aleatorios para inspectores.

evaluar_asignaciones: inicia otro agente LLM para auditar las asignaciones de inspectores.

Nota: en el orquestador se hace referencia a asignar_ordenes pero no existe implementación; hay que considerar este vacío.

Habilidad (src/agents/skills/interpretar_wisc.py):

Analiza datos de evaluación psicológica (WISC) y escribe interpretaciones narrativas en DynamoDB mediante ayudantes externos (dynamo.actualizar_json).

3. Capa de utilidades

Ayudantes para DynamoDB (src/utils/consultar_ordenes.py y src/utils/insertar_json.py):

obtener_ordenes: construye filtros de búsqueda dinámica por campos como ID, ciudad o servicio.

insertar_ordenes: carga órdenes de ejemplo desde src/tests/ordenes.json en DynamoDB.

Nota: los nombres de campos en consultar_ordenes (ej. codigo_servicio, linea) no coinciden con las claves del JSON de ejemplo (Cod_servicio, Linea), lo que romperá los filtros.

Ayudante S3 (src/utils/s3_utils.py):

subir_a_s3: sube un archivo local y devuelve una URL pública.

4. Configuración

config/config.py contiene constantes del proyecto: región AWS, IDs de modelos Bedrock, nombres de tablas/buckets, etc. Es importado por varios módulos; mantenerlo actualizado para despliegues.

5. Pruebas y datos de ejemplo

src/tests/ordenes.json: datos de órdenes ficticias para pruebas locales.

src/tests/get_ordenes_test.py: script manual que demuestra cómo llamar a obtener_ordenes (no es una prueba unitaria real).

Resumen general

El repositorio es un backend prototipo para un flujo de trabajo asistido por IA que recupera órdenes de servicio, asigna inspectores y evalúa las asignaciones usando un LLM (Amazon Bedrock vía el SDK “strands”). También incluye herramientas para interactuar con DynamoDB y S3. La mayoría de los archivos son plantillas o ejemplos mínimos, por lo que el código aún está en una fase inicial.

Estructura de directorios
Ruta	Propósito
main.py	Punto de entrada por línea de comandos. Inicia el agente orquestador y abre un bucle interactivo donde los mensajes del usuario se envían al agente.
config/	Configuración central (config.py) con región AWS, ajustes de modelo Bedrock, nombre de la tabla DynamoDB y bucket S3.
src/agents/	Código y herramientas relacionadas con el agente.
• agents/agente_orquestador.py: configura el agente principal y declara herramientas disponibles.
• tools/agents_tools.py: define utilidades (resúmenes de órdenes, disponibilidad, evaluación, etc.).
• skills/: contiene habilidades de dominio; solo interpretar_wisc.py tiene contenido.
src/utils/	Scripts de utilidades.
• consultar_ordenes.py: consulta órdenes en DynamoDB con filtros.
• insertar_json.py: inserta órdenes de prueba desde JSON.
• s3_utils.py: sube archivos a S3 y devuelve la URL pública.
src/tests/	Archivos de prueba/demostración muy simples (ej. get_ordenes_test.py).
docs/, README.md, serverless.yml, requirements.txt	Marcadores de posición vacíos.
Conceptos importantes y dependencias externas

Strands: biblioteca que provee las abstracciones Agent y BedrockModel. Fundamental para entender cómo extender las capacidades del agente.

Amazon Bedrock: servicio LLM; configuración en config/config.py.

AWS Services: uso de boto3 para DynamoDB y S3; se requieren credenciales AWS configuradas.

JSON y Pandas: uso extensivo de JSON para salidas estructuradas; pandas aparece en utilidades (ej. resúmenes).

Recomendaciones para nuevos colaboradores

Estudiar el flujo del orquestador
Revisar juntos agente_orquestador.py y agents_tools.py para comprender la interacción agente-herramienta con Strands.

Implementar funciones faltantes o vacías

asignar_ordenes (referenciada pero no implementada).

Módulos de habilidades vacíos como generar_reporte.py.

Explorar la integración con AWS

Cómo se construyen los filtros en DynamoDB (consultar_ordenes.py).

Cómo cargar datos de ejemplo (insertar_json.py).

Subida de archivos con s3_utils.py.

Mejorar pruebas y documentación

Ampliar cobertura de pruebas en src/tests.

Completar README.md y docs/.

Profundizar en habilidades avanzadas

Analizar interpretar_wisc.py para entender integración compleja con DynamoDB y módulos externos.

Notas importantes

Muchos archivos son placeholders: README, docs, requirements, handlers y algunas skills/tools.

Falta importación de asignar_ordenes en agente_orquestador.

Inconsistencia en nombres de campos: unificar esquema (codigo_servicio vs Cod_servicio).

Dependencias externas:

strands y dynamo.actualizar_json no están incluidos.

pandas se importa en agents_tools.py pero no se usa.

Credenciales AWS: se asume que están configuradas; no hay gestión de autenticación en el código.verview
This repository is a very early-stage backend for “Servimeters”.
Most of the files are scaffolding, but the implemented pieces focus on:

Driving a command-line agent orchestration workflow.

Using AWS services (Bedrock, DynamoDB, S3) to store and retrieve data.

Demonstrating a sample skill for interpreting WISC psychological test results.

servimeters_backend/
├── main.py                  # CLI entrypoint
├── config/                  # Global constants (AWS, Bedrock, table names…)
├── src/
│   ├── agents/              # LLM orchestration, tools, and domain-specific skills
│   ├── utils/               # DynamoDB and S3 helpers
│   ├── handlers/            # Currently empty (placeholder for AWS Lambda handlers?)
│   └── tests/               # Sample data and a manual test script
└── docs/, serverless.yml, requirements.txt  # Present but empty
Key Components
1. CLI Entrypoint
main.py launches an interactive loop that proxies user messages to a “Servimeters” agent powered by an orchestrator (src/agents/agents/agente_orquestador.py).

The orchestrator builds a BedrockModel (Anthropic Haiku) and delegates to tools for:

Obtaining order summaries.

Assigning inspectors to orders (tool currently missing).

Evaluating the assignment results.

2. Agent Tools & Skills
Tools (src/agents/tools/agents_tools.py):

obtener_resumen_ordenes – reads DynamoDB orders and aggregates totals by service and city.

obtener_inspectores_fijos – returns a hard‑coded list of inspectors.

generar_disponibilidad_tool – produces random availability blocks for inspectors.

evaluar_asignaciones – spins up another LLM agent to audit inspector assignments.

There is a reference to asignar_ordenes in the orchestrator, but no implementation; be aware of this gap.

Skill (src/agents/skills/interpretar_wisc.py):

Parses psychological assessment data (WISC) and writes narrative interpretations back to DynamoDB via external helpers (dynamo.actualizar_json).

3. Utility Layer
DynamoDB helpers (src/utils/consultar_ordenes.py & src/utils/insertar_json.py):

obtener_ordenes builds dynamic scan filters for fields like ID, city, or service.

insertar_ordenes loads sample JSON orders from src/tests/ordenes.json into DynamoDB.

NOTE: field names in consultar_ordenes (e.g., codigo_servicio, linea) don’t match the sample JSON keys (Cod_servicio, Linea), which will break filtering.

S3 helper (src/utils/s3_utils.py):

subir_a_s3 uploads a local file and returns a public URL.

4. Configuration
config/config.py holds project constants: AWS region, Bedrock model IDs, table/bucket names, etc. It’s imported by various modules; keep it updated for deployment.

5. Tests and Sample Data
src/tests/ordenes.json contains mock order data for local experimentation.

src/tests/get_ordenes_test.py is a manual script demonstrating how to call obtener_ordenes. It is not a true unit test.


Overview
The repository is a prototype backend for an AI‑assisted workflow that retrieves service orders, assigns inspectors, and evaluates assignments using an LLM (Amazon Bedrock through the “strands” SDK). It also contains tools for interacting with DynamoDB and S3. Most files are stubs or minimal examples, so the codebase is still in an early stage.

Directory Structure
Path	Purpose
main.py	Command‑line entry point. Spins up the orchestrator agent and opens an interactive loop where user messages are forwarded to the agent.
config/	Central configuration (config.py) with AWS region, Bedrock model settings, DynamoDB table name, and S3 bucket.
src/agents/	Agent‑related code and tools.
• agents/agente_orquestador.py configures the main agent and declares available tools.
• tools/agents_tools.py defines utility tools (retrieving order summaries, generating availability, evaluating assignments, etc.).
• skills/ contains domain‑specific “skills”; only interpretar_wisc.py has content (interprets WISC test results and updates DynamoDB), while others are placeholders.
src/utils/	Utility scripts.
• consultar_ordenes.py queries DynamoDB orders with optional filters.
• insertar_json.py inserts sample orders from src/tests/ordenes.json into DynamoDB.
• s3_utils.py uploads files to S3 and returns a public URL.
src/tests/	Very lightweight test/demo files (e.g., get_ordenes_test.py prints sample results).
docs/, README.md, serverless.yml, requirements.txt	Currently empty placeholders.
Key Components
Orchestrator Agent (src/agents/agents/agente_orquestador.py)

Uses a Bedrock model via strands to follow a system prompt: fetch orders from DynamoDB, assign inspectors, and evaluate the assignments.

Lists tools it can invoke, such as retrieving order summaries (obtener_resumen_ordenes), assigning orders (expected but missing), and evaluating assignments (evaluar_asignaciones).

Agent Tools (src/agents/tools/agents_tools.py)

Provide helper functions decorated with @tool so the agent can call them.

Examples:

obtener_resumen_ordenes: aggregates orders by service and city.

obtener_inspectores_fijos & generar_disponibilidad_tool: supply inspector data and simulated availability.

evaluar_asignaciones: launches another Bedrock‑powered agent to judge the quality of assignments.

DynamoDB Utilities

consultar_ordenes.py: builds dynamic filters using boto3.dynamodb.conditions.Attr and returns a JSON list of matching records.

insertar_json.py: loads sample orders from JSON and inserts them into the DynamoDB table.

interpretar_wisc.py: (advanced) processes psychological test results and updates fields in DynamoDB via external helpers (dynamo.actualizar_json).

S3 Helper (s3_utils.py)

Uploads a local file to S3 and prints the resulting URL.

Important Concepts & External Dependencies
Strands Library: Provides Agent and BedrockModel abstractions. Understanding how to craft prompts and tools with strands is essential to extending the agent’s capabilities.

Amazon Bedrock: LLM service; configuration is set in config/config.py (model ID, temperature, etc.).

AWS Services: boto3 is used for DynamoDB and S3 interactions. Familiarity with AWS credentials and resource management is required.

JSON Handling & Pandas: Agents use JSON extensively for structured outputs; pandas appears in tool utilities (e.g., summarizing data).

Recommended Next Steps for Newcomers
Study the Orchestrator Workflow

Review agente_orquestador.py and agents_tools.py together to understand the agent‑tool interaction pattern in Strands.

Implement Missing or Placeholder Functions

asignar_ordenes (referenced but absent) and empty skill modules like generar_reporte.py are good starting points.

Explore AWS Integration

Learn how DynamoDB filters are built (consultar_ordenes.py) and how to seed data (insertar_json.py).

Practice uploading files via s3_utils.py and handling AWS credentials securely.

Enhance Testing & Documentation

Expand the minimal test coverage under src/tests and populate the empty README.md / docs to clarify project setup and usage.

Deep Dive into Advanced Skills

interpretar_wisc.py showcases a complex domain‑specific interpretation process. Investigate how it interacts with external modules and DynamoDB for richer integrations.

Important Notes for New Contributors
Many files are placeholders: README, docs, requirements, handlers, and some skills/tools are blank. Expect to flesh these out.

Missing tool import: agente_orquestador references asignar_ordenes but it’s neither defined nor imported.

Field-name consistency: DynamoDB queries assume lowercase keys (codigo_servicio), while sample data uses mixed case (Cod_servicio). Unify schema.

External dependencies:

strands (agent framework) and dynamo.actualizar_json are not included in the repo. Ensure you have access to these packages.

pandas is imported in agents_tools.py but unused—safe to remove if not needed.

AWS credentials: All DynamoDB and S3 helpers expect AWS credentials/environment to be configured; nothing here manages authentication.

Next Steps & Learning Path
Understand the “strands” library: It powers the LLM agents. Study its Agent and BedrockModel APIs.

Implement missing tools:

asignar_ordenes to assign inspectors to orders.

Any other domain-specific tools planned for agents_tools.py.

Improve tests:

Convert manual scripts into proper unit tests (pytest or similar).

Mock AWS services to run offline.

Fill in documentation: Populate README.md, docs/, and requirements.txt for easier onboarding.

Serverless deployment: serverless.yml is empty; configure functions, IAM roles, and resources to deploy to AWS Lambda or similar.

Schema cleanup: Align field naming conventions across JSON, DynamoDB, and code; consider central data models.

Explore AWS services:

Boto3 for DynamoDB & S3 operations.

AWS Bedrock for model hosting.

Robust error handling & logging: Currently minimal; add structured logs and exception tracking.