# src/utils/consultar_ordenes.py

import boto3
import json
from config import config
from boto3.dynamodb.conditions import Attr

# Inicializar recurso DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(config.TABLE_NAME)

def obtener_ordenes(
    id_orden=None,
    ciudad=None,
    cliente=None,
    codigo_servicio=None,
    contacto_cliente=None,
    linea=None,
    mail_cliente=None
):
    """
    Consulta órdenes en DynamoDB filtrando por los parámetros especificados.
    Si un parámetro es None, no se filtra por ese campo.
    Devuelve un objeto JSON con las órdenes encontradas.
    """
    try:
        # Construir filtros dinámicamente
        filtro = None
        if id_orden:
            filtro = Attr("ID_ORDEN").eq(id_orden)
        if ciudad:
            filtro = filtro & Attr("ciudad").eq(ciudad) if filtro else Attr("ciudad").eq(ciudad)
        if cliente:
            filtro = filtro & Attr("cliente").eq(cliente) if filtro else Attr("cliente").eq(cliente)
        if codigo_servicio:
            filtro = filtro & Attr("codigo_servicio").eq(codigo_servicio) if filtro else Attr("codigo_servicio").eq(codigo_servicio)
        if contacto_cliente:
            filtro = filtro & Attr("contacto_cliente").eq(contacto_cliente) if filtro else Attr("contacto_cliente").eq(contacto_cliente)
        if linea:
            filtro = filtro & Attr("linea").eq(linea) if filtro else Attr("linea").eq(linea)
        if mail_cliente:
            filtro = filtro & Attr("mail_cliente").eq(mail_cliente) if filtro else Attr("mail_cliente").eq(mail_cliente)

        # Ejecutar consulta
        if filtro:
            response = table.scan(FilterExpression=filtro)
        else:
            response = table.scan()

        # Devolver resultados como JSON
        return json.dumps(response.get("Items", []), ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)

