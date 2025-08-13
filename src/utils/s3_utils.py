import boto3
import os


def subir_a_s3(filepath: str, bucket: str, key: str) -> str:
    """
    Sube un archivo local a un bucket S3 y devuelve la URL pública (si aplica).
    """
    s3 = boto3.client("s3")

    try:
        s3.upload_file(filepath, bucket, key)
        region = s3.get_bucket_location(Bucket=bucket)["LocationConstraint"]

        if region:
            url = f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
        else:  # us-east-1 (no región en la URL)
            url = f"https://{bucket}.s3.amazonaws.com/{key}"

        print(f"✅ Archivo subido correctamente a: {url}")
        return url

    except Exception as e:
        print(f"❌ Error al subir archivo a S3: {e}")
        return f"❌ Error: {e}"
