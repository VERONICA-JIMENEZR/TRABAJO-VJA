import conect 

try:
    clientes_df1 = conect.read_csv_from_s3(conect.bucket_name, 'Cliente.csv', sep=';')
    print("Archivo 'Cliente.csv' cargado correctamente.")
except Exception as e:
    print(f"Error al cargar 'Cliente.csv': {e}")

try:
    inventario_df = conect.read_csv_from_s3(conect.bucket_name, 'Inventario.csv', sep=';')
    print("Archivo 'Inventario.csv' cargado correctamente.")
except Exception as e:
    print(f"Error al cargar 'Inventario.csv': {e}")

try:
    transacciones_df = conect.read_csv_from_s3(conect.bucket_name, 'Transaccion.csv', sep=';')
    print("Archivo 'Transaccion.csv' cargado correctamente.")
except Exception as e:
    print(f"Error al cargar 'Transaccion.csv': {e}")

