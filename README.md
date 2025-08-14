Overview
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