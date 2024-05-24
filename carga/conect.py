import os
import boto3
import pandas as pd
import io

# Reemplaza 'my-access-key' y 'my-secret-key' con las credenciales de AWS
s3 = boto3.client(
    's3',
     aws_access_key_id=os.environ['CONTRASENA1'],
    aws_secret_access_key=os.environ['CONTRASENA2']
)

# Nombre de tu bucket
bucket_name = 'rawdata1243'

# Función para leer un archivo CSV de S3 a un DataFrame de pandas
def read_csv_from_s3(bucket_name, file_key, sep=','):
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    return pd.read_csv(io.BytesIO(obj['Body'].read()), sep=sep, on_bad_lines='skip')  # Usar on_bad_lines='skip' para ignorar líneas problemáticas


