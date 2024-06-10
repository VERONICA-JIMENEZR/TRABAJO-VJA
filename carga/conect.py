import os
import boto3
import pandas as pd
import io
from typing import Union

# Reemplaza 'my-access-key' y 'my-secret-key' con las credenciales de AWS
s3 = boto3.client(
    's3',
    aws_access_key_id='',  # os.environ['COgiNTRASENA1']
    aws_secret_access_key=''  # os.environ['CONTRASENA2']
)

# Nombre de tu bucket
bucket_name = 'rawdata12435'

def read_csv_from_s3(bucket_name: str, file_key: str, sep: str = ',') -> pd.DataFrame:
    """
    Lee un archivo CSV desde un bucket de S3 y lo carga en un DataFrame de pandas.

    Args:
        bucket_name (str): El nombre del bucket de S3.
        file_key (str): La clave del archivo en el bucket de S3.
        sep (str, optional): El delimitador del archivo CSV. Por defecto es ','.

    Returns:
        pd.DataFrame: Un DataFrame de pandas con los datos del archivo CSV.

    """
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    return pd.read_csv(io.BytesIO(obj['Body'].read()), sep=sep, on_bad_lines='skip')



