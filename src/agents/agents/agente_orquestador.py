# src/agents/agents/agente_orquestador.py
from strands import Agent
from strands.models import BedrockModel
from config.config import (
    MODEL_TOP_P,
    MODEL_TEMPERATURE,
    MODEL_ID,
    MODEL_MAX_TOKENS,
    MODEL_REGION_NAME
)

# Tools centralizados
from src.agents.tools.agents_tools import (
    obtener_resumen_ordenes,
    asignar_ordenes,        # <-- Tool para asignación inicial
    evaluar_asignaciones    # <-- Tool evaluador
)

class agente_orquestador:
    def __init__(self):
        self.model = BedrockModel(
            model_id=MODEL_ID,
            temperature=MODEL_TEMPERATURE,
            top_p=MODEL_TOP_P,
            max_tokens=MODEL_MAX_TOKENS,
            region_name=MODEL_REGION_NAME
        )

        prompt_template = """
        Eres un analista de planeación operativa con la siguiente misión:
        1. Recuperar órdenes desde DynamoDB.
        2. Asignar cada orden a un inspector disponible usando el tool correspondiente.
        3. Enviar la lista de asignaciones al tool evaluador para obtener un veredicto de precisión.

        📋 Criterios de asignación:
        - Certificación requerida para el servicio.
        - Disponibilidad en el horario solicitado.
        - Preferencia por la misma ciudad o cercana.
        - Menor costo y menor desplazamiento.

        ✅ Devuélveme un JSON final con:
        {
          "asignaciones": [...],
          "evaluacion": {...}
        }
        """

        self.agent = Agent(
            model=self.model,
            system_prompt=prompt_template,
            tools=[obtener_resumen_ordenes, asignar_ordenes, evaluar_asignaciones],
            callback_handler=None
        )

    def responder(self, mensaje: str) -> str:
        return self.agent(mensaje)
