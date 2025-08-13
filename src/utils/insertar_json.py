# insertar_json.py
import json
import boto3
from config import config
import os

# Inicializar el cliente de DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(config.TABLE_NAME)

def insertar_ordenes():
    try:
        # Construir la ruta absoluta al archivo ordenes.json
        ruta = os.path.join(os.path.dirname(__file__), "../../tests/ordenes.json")
        ruta = os.path.abspath(ruta)

        with open(ruta, "r", encoding="utf-8") as f:
            ordenes = json.load(f)

        # Insertar cada orden en la tabla
        for orden in ordenes:
            table.put_item(Item=orden)
            print(f"✅ Orden {orden['ID_ORDEN']} insertada correctamente.")

    except FileNotFoundError:
        print(f"❌ No se encontró el archivo en la ruta: {ruta}")
    except Exception as e:
        print(f"⚠️ Error insertando ordenes: {e}")

if __name__ == "__main__":
    insertar_ordenes()
