
from src.utils.consultar_ordenes import obtener_ordenes

# python -m src.tests.get_ordenes_test


# Caso 1: Buscar por ID específico
# print(obtener_ordenes(id_orden="ORD-001"))

# Caso 2: Buscar por ciudad y cliente
#print(obtener_ordenes(ciudad="Bogota"))

# Caso 3: Buscar por servicio y contacto
#print(obtener_ordenes(codigo_servicio="SV-123", contacto_cliente="3001234567"))

# Caso 4: Sin filtros (traer todas las órdenes) 
print(obtener_ordenes())
