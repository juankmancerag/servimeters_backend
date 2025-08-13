# src/agents/tools/agents_tools.py
import random
from datetime import datetime, timedelta
import pandas as pd
from strands.tools import tool
import json
from src.utils.consultar_ordenes import obtener_ordenes
from strands.models import BedrockModel
from strands import Agent

from config.config import (
    MODEL_TOP_P,
    MODEL_TEMPERATURE,
    MODEL_ID,
    MODEL_MAX_TOKENS,
    MODEL_REGION_NAME
)


@tool
def obtener_resumen_ordenes() -> str:
    """
    Recupera todas las órdenes desde DynamoDB y calcula:
    1. Total de órdenes
    2. Total por servicio
    3. Total por ciudad
    """
    try:
        data_json = obtener_ordenes()  # sin filtros
        data = json.loads(data_json)

        total_ordenes = len(data)

        ordenes_por_servicio = {}
        ordenes_por_ciudad = {}

        for orden in data:
            # Servicio
            servicio = orden.get("Linea", "Desconocido")
            ordenes_por_servicio[servicio] = ordenes_por_servicio.get(servicio, 0) + 1

            # Ciudad
            ciudad = orden.get("ciudad", "Desconocida")
            ordenes_por_ciudad[ciudad] = ordenes_por_ciudad.get(ciudad, 0) + 1

        return json.dumps({
            "total_ordenes": total_ordenes,
            "ordenes_por_servicio": ordenes_por_servicio,
            "ordenes_por_ciudad": ordenes_por_ciudad
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)

# Lista fija de inspectores (puedes cargarla desde un JSON o DynamoDB)
INSPECTORES_FIJOS = [
    {
        'id': 1,
        'nombre': "Juan Pérez",
        'ciudad_origen': "Bogotá",
        'direccion_origen': "Calle 100 #45-50",
        'costo': 120,
        'certificaciones': ["RETIE", "Ascensores"]
    },
    {
        'id': 2,
        'nombre': "Ana Gómez",
        'ciudad_origen': "Medellín",
        'direccion_origen': "Carrera 15 #85-10",
        'costo': 110,
        'certificaciones': ["RETILAB", "RETIE"]
    },
    {
        'id': 3,
        'nombre': "Carlos Ruiz",
        'ciudad_origen': "Cali",
        'direccion_origen': "Av. Suba #120-30",
        'costo': 130,
        'certificaciones': ["Ascensores"]
    }
]


@tool
def obtener_inspectores_fijos() -> str:
    """
    Devuelve la lista fija de inspectores en formato JSON.
    """
    return json.dumps(INSPECTORES_FIJOS, ensure_ascii=False, indent=2)


@tool
def generar_disponibilidad_tool(dia: str = "2025-07-10") -> str:
    """
    Genera disponibilidad aleatoria para un día específico.
    Parámetros:
    - dia: fecha en formato YYYY-MM-DD (default: 2025-07-10)
    """
    franjas = []
    base_hora = datetime.strptime(f"{dia} 08:00", "%Y-%m-%d %H:%M")
    for _ in range(random.randint(2, 4)):
        inicio = base_hora + timedelta(hours=random.randint(0, 7))
        duracion = random.choice([1, 2])
        fin = inicio + timedelta(hours=duracion)
        franjas.append(f"{inicio.strftime('%Y-%m-%d %H:%M')}-{fin.strftime('%H:%M')}")

    return json.dumps(franjas, ensure_ascii=False, indent=2)


@tool
def evaluar_asignaciones(asignaciones_json: str) -> str:
    """
    Analiza la asignación inicial hecha por el primer agente usando un agente evaluador LLM.
    Emite un veredicto sobre la precisión de las asignaciones basándose en criterios operativos.
    """
    try:
        # Validar formato JSON
        try:
            asignaciones = json.loads(asignaciones_json)
        except json.JSONDecodeError:
            return json.dumps({"error": "El formato del JSON de asignaciones no es válido."}, ensure_ascii=False, indent=2)

        # Inicializar modelo y agente evaluador
        model = BedrockModel(
            model_id=MODEL_ID,
            temperature=MODEL_TEMPERATURE,
            top_p=MODEL_TOP_P,
            max_tokens=MODEL_MAX_TOKENS,
            region_name=MODEL_REGION_NAME
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
            callback_handler=None
        )

        # Ejecutar evaluación con el JSON de asignaciones como entrada
        resultado = agente_eval(asignaciones_json)
        return resultado

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)