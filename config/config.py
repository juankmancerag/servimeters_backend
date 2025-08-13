# config/config.py

#pip install -r requirements.txt --platform manylinux2014_x86_64 --implementation cp --python-version 3.12 --only-binary=:all: --target ./python --upgrade --no-deps

## #######################################################################################################
##
##
## Account ID 480238144518943892995551
## AstraTec
## #######################################################################################################

## #######################################################################################################
## @section Variables del proyecto
## #######################################################################################################


# Región AWS
REGION_NAME = "us-east-1"

# Parametros de Bedrock para configuracion del agente strands
MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
MODEL_TEMPERATURE = 0.3
MODEL_TOP_P = 0.9
MODEL_MAX_TOKENS = 2048
MODEL_REGION_NAME = "us-east-1"


# Nombre del agente (opcional, por si quieres personalizar mensajes)
AGENTE_NOMBRE = "Agente Programador Servimeters"

#Nombre del proyecto
CONF_NOMBRE_PROYECTO = "servimeters"


#Nombre de tabla de dynamoDB para almacenar las ordenes de servicio
TABLE_NAME = 'servimeters-ordenes-servicio'

# Nombre del bucket S3 para almacenar  informes finales
REPORTS_BUCKET_NAME = "servimeters-files"


