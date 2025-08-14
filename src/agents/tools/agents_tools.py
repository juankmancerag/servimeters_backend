# src/agents/tools/agents_tools.py
"""Herramientas utilizadas por el agente orquestador.

El proyecto depende de librerías externas como ``boto3`` y ``strands`` que no
siempre están disponibles en los entornos de prueba.  Este módulo incluye
implementaciones de respaldo para que pueda importarse sin dichos paquetes,
permitiendo probar la lógica interna de las herramientas.
"""

import random
from datetime import datetime, timedelta
import json

# ---------------------------------------------------------------------------
# Optional dependencies
# ---------------------------------------------------------------------------
try:  # pragma: no cover - solo se usa si la dependencia está instalada
    import pandas as pd  # noqa: F401
except ModuleNotFoundError:  # pragma: no cover
    pd = None

try:  # pragma: no cover - solo se usa con la librería real
    from strands.tools import tool
    from strands.models import BedrockModel
    from strands import Agent
except ModuleNotFoundError:  # pragma: no cover
    def tool(func):  # type: ignore
        """Decorador de respaldo que devuelve la función sin modificar."""
        return func

    class BedrockModel:  # pragma: no cover
        def __init__(self, *args, **kwargs):
            pass

    class Agent:  # pragma: no cover
        def __init__(self, *args, **kwargs):
            self.tools = kwargs.get("tools", [])

        def __call__(self, *args, **kwargs):
            return ""

try:  # pragma: no cover - boto3 no siempre está disponible
    from src.utils.consultar_ordenes import obtener_ordenes
except Exception:  # pragma: no cover
    def obtener_ordenes(*args, **kwargs) -> str:
        """Versión de respaldo que devuelve una lista vacía."""
        return json.dumps([])

from config.config import (
    MODEL_TOP_P,
    MODEL_TEMPERATURE,
    MODEL_ID,
    MODEL_MAX_TOKENS,
    MODEL_REGION_NAME,
)


@tool
def obtener_resumen_ordenes() -> str:
    """Obtiene un resumen estadístico de las órdenes registradas."""
    try:
        data_json = obtener_ordenes()  # sin filtros
        data = json.loads(data_json)

        total_ordenes = len(data)

        ordenes_por_servicio = {}
        ordenes_por_ciudad = {}

        for orden in data:
            servicio = orden.get("Linea", "Desconocido")
            ordenes_por_servicio[servicio] = (
                ordenes_por_servicio.get(servicio, 0) + 1
            )

            ciudad = orden.get("ciudad", "Desconocida")
            ordenes_por_ciudad[ciudad] = (
                ordenes_por_ciudad.get(ciudad, 0) + 1
            )

        return json.dumps(
            {
                "total_ordenes": total_ordenes,
                "ordenes_por_servicio": ordenes_por_servicio,
                "ordenes_por_ciudad": ordenes_por_ciudad,
            },
            ensure_ascii=False,
            indent=2,
        )

    except Exception as e:  # pragma: no cover - depende de AWS
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)


# Lista fija de inspectores (puede almacenarse en JSON o en DynamoDB)
INSPECTORES_FIJOS = [
    {
        "id": 1,
        "nombre": "Juan Pérez",
        "ciudad_origen": "Bogotá",
        "direccion_origen": "Calle 100 #45-50",
        "costo": 120,
        "certificaciones": ["RETIE", "Ascensores"],
    },
    {
        "id": 2,
        "nombre": "Ana Gómez",
        "ciudad_origen": "Medellín",
        "direccion_origen": "Carrera 15 #85-10",
        "costo": 110,
        "certificaciones": ["RETILAB", "RETIE"],
    },
    {
        "id": 3,
        "nombre": "Carlos Ruiz",
        "ciudad_origen": "Cali",
        "direccion_origen": "Av. Suba #120-30",
        "costo": 130,
        "certificaciones": ["Ascensores"],
    },
]


@tool
def obtener_inspectores_fijos() -> str:
    """Devuelve la lista fija de inspectores en formato JSON."""
    return json.dumps(INSPECTORES_FIJOS, ensure_ascii=False, indent=2)


@tool
def asignar_ordenes(ordenes_json: str) -> str:
    """Asigna cada orden al primer inspector que cumpla la certificación.

    Si ninguna certificación coincide, se asigna el primer inspector
    disponible. El resultado se devuelve en formato JSON.
    """

    try:
        ordenes = json.loads(ordenes_json)
    except json.JSONDecodeError:
        return json.dumps(
            {"error": "El formato del JSON de órdenes no es válido."},
            ensure_ascii=False,
            indent=2,
        )

    asignaciones = []
    for orden in ordenes:
        linea = orden.get("Linea")
        inspector = None
        for candidato in INSPECTORES_FIJOS:
            if linea in candidato.get("certificaciones", []):
                inspector = candidato["nombre"]
                break
        if inspector is None and INSPECTORES_FIJOS:
            inspector = INSPECTORES_FIJOS[0]["nombre"]

        asignaciones.append(
            {"ID_ORDEN": orden.get("ID_ORDEN"), "Inspector": inspector}
        )

    return json.dumps(asignaciones, ensure_ascii=False, indent=2)


@tool
def generar_disponibilidad_tool(dia: str = "2025-07-10") -> str:
    """Genera disponibilidad aleatoria para un día específico."""
    franjas = []
    base_hora = datetime.strptime(f"{dia} 08:00", "%Y-%m-%d %H:%M")
    for _ in range(random.randint(2, 4)):
        inicio = base_hora + timedelta(hours=random.randint(0, 7))
        duracion = random.choice([1, 2])
        fin = inicio + timedelta(hours=duracion)
        franjas.append(
            f"{inicio.strftime('%Y-%m-%d %H:%M')}-{fin.strftime('%H:%M')}"
        )

    return json.dumps(franjas, ensure_ascii=False, indent=2)


@tool
def evaluar_asignaciones(asignaciones_json: str) -> str:
    """Evalúa la precisión de las asignaciones realizadas por el agente."""
    try:  # pragma: no cover - requiere servicios externos
        try:
            json.loads(asignaciones_json)
        except json.JSONDecodeError:
            return json.dumps(
                {"error": "El formato del JSON de asignaciones no es válido."},
                ensure_ascii=False,
                indent=2,
            )

        model = BedrockModel(
            model_id=MODEL_ID,
            temperature=MODEL_TEMPERATURE,
            top_p=MODEL_TOP_P,
            max_tokens=MODEL_MAX_TOKENS,
            region_name=MODEL_REGION_NAME,
        )

        prompt_template = """
        Eres un evaluador experto en asignación de inspectores a órdenes de servicio.
        Debes analizar la asignación propuesta por otro agente y determinar si cumple con estos criterios:

        1. El inspector debe tener la certificación necesaria para el servicio asignado.
        2. Debe tener disponibilidad en el horario solicitado.
        3. Idealmente debe vivir en la misma ciudad o cerca de la ubicación del servicio.
        4. Se debe considerar el menor costo y menor desplazamiento.

        Instrucciones de salida:
        - Evalúa cada asignación individualmente y clasifícala como "Correcta" o "Incorrecta".
        - Justifica cada veredicto en una o dos líneas.
        - Devuelve un JSON con:
          {
            "total_asignaciones": N,
            "correctas": X,
            "precision_%": Y,
            "detalle": [
              {"ID_ORDEN": ..., "Inspector": ..., "resultado": ..., "motivo": ...}
            ]
          }
        """

        agente_eval = Agent(
            model=model,
            system_prompt=prompt_template,
            tools=[],
            callback_handler=None,
        )

        resultado = agente_eval(asignaciones_json)
        return resultado

    except Exception as e:  # pragma: no cover
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)

