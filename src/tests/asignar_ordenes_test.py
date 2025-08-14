import sys
import types
import json


def setup_strands_stub():
    """Create minimal ``strands`` modules so imports succeed during tests."""
    strands = types.ModuleType("strands")

    class Agent:
        def __init__(self, model=None, system_prompt=None, tools=None, callback_handler=None):
            self.tools = tools or []

        def __call__(self, *args, **kwargs):
            return ""

    class BedrockModel:
        def __init__(self, *args, **kwargs):
            pass

    tools_module = types.ModuleType("strands.tools")
    def tool(func):
        return func
    tools_module.tool = tool

    models_module = types.ModuleType("strands.models")
    models_module.BedrockModel = BedrockModel

    strands.Agent = Agent
    strands.tools = tools_module
    strands.models = models_module

    sys.modules.setdefault("strands", strands)
    sys.modules.setdefault("strands.tools", tools_module)
    sys.modules.setdefault("strands.models", models_module)


def test_asignar_ordenes_assigns_inspectors():
    setup_strands_stub()
    from src.agents.tools.agents_tools import asignar_ordenes

    ordenes = [
        {"ID_ORDEN": "1", "Linea": "RETIE"},
        {"ID_ORDEN": "2", "Linea": "RETILAB"},
        {"ID_ORDEN": "3", "Linea": "TV"},
    ]

    resultado = json.loads(asignar_ordenes(json.dumps(ordenes)))

    assert resultado == [
        {"ID_ORDEN": "1", "Inspector": "Juan Pérez"},
        {"ID_ORDEN": "2", "Inspector": "Ana Gómez"},
        {"ID_ORDEN": "3", "Inspector": "Juan Pérez"},
    ]


def test_agente_orquestador_uses_asignar_ordenes():
    setup_strands_stub()
    from src.agents.agents.agente_orquestador import agente_orquestador

    agente = agente_orquestador()
    tool_names = [t.__name__ for t in agente.agent.tools]

    assert "asignar_ordenes" in tool_names

