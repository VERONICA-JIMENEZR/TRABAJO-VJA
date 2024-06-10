from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO


app: FastAPI = FastAPI()

security: HTTPBasic = HTTPBasic()

# Credenciales de acceso
fake_users_db: dict = {
    "Vero": "1234"  # Usuario: Vero, Contraseña: 1234
}

clientes_df: pd.DataFrame = pd.read_csv("clientes_segmentados.csv", index_col="ID cliente")
productos_mas_vendidos_df: pd.DataFrame = pd.read_csv("productos_mas_vendidos.csv")
productos_menos_vendidos_df: pd.DataFrame = pd.read_csv("productos_menos_vendidos.csv")
resultados_cohorte_df: pd.DataFrame = pd.read_csv("resultados_cohorte.csv")

@app.get("/")
async def obtener_mensaje() -> dict:
    """
    Mensaje de bienvenida para la API de Eureka.
    """
    return {"message": "¡Bienvenido a la API de Eureka! Esta API proporciona información sobre productos más y menos vendidos, así como el producto más consumido por mes."}


@app.get("/token")
async def login(credentials: HTTPBasicCredentials = Depends(security)) -> dict:
    """
    Obtener token de autenticación.
    """
    correct_username: str = fake_users_db.get(credentials.username)
    correct_password: str = fake_users_db.get(credentials.password)
    if not (correct_username and correct_password and
            correct_username == credentials.username and
            correct_password == credentials.password):
        return JSONResponse(status_code=401, content={"message": "Nombre de usuario o contraseña incorrectos"})
    return {"token": "token_de_eureka"}



@app.get("/clientes/{segmento}")
async def obtener_clientes(segmento: str) -> dict:
    """
    Obtener clientes por segmento.
    """
    if segmento.lower() not in ["oro", "plata", "bronce"]:
        raise HTTPException(status_code=404, detail="Segmento no válido")

    clientes_segmento: pd.DataFrame = clientes_df[clientes_df["Cliente"] == segmento.capitalize()]
    clientes: list = clientes_segmento["Nombre"].tolist()
    cantidad: int = len(clientes)
    porcentaje: float = (cantidad / len(clientes_df)) * 100

    return {
        "segmento": segmento.capitalize(),
        "clientes": clientes,
        "cantidad": cantidad,
        "porcentaje": f"{porcentaje:.2f}%"
    }

# CRUD - Create
@app.post("/clientes")
async def agregar_cliente(nombre: str, cliente: str) -> dict:
    """
    Agregar un nuevo cliente.
    """
    if cliente.lower() not in ["oro", "plata", "bronce"]:
        raise HTTPException(status_code=404, detail="Segmento no válido")

    nuevos_datos: pd.DataFrame = pd.DataFrame({"Nombre": [nombre], "Cliente": [cliente.capitalize()]})
    global clientes_df
    clientes_df = pd.concat([clientes_df, nuevos_datos])
    clientes_df.to_csv("clientes_segmentados.csv")
    return {"message": "Cliente agregado exitosamente"}

# CRUD - Read
@app.get("/clientes")
async def obtener_todos_los_clientes():
    """
    Obtener todos los clientes segmentados.
    """
    return clientes_df.to_dict(orient="index")


# CRUD - Update
@app.put("/clientes/{id_cliente}")
async def actualizar_cliente(id_cliente: str, nombre: str, cliente: str):
    """
    Actualizar información de un cliente.
    """
    if id_cliente not in clientes_df.index:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    if cliente.lower() not in ["oro", "plata", "bronce"]:
        raise HTTPException(status_code=404, detail="Segmento no válido")

    clientes_df.loc[id_cliente] = [nombre, cliente.capitalize()]
    clientes_df.to_csv("clientes_segmentados.csv")
    return {"message": "Cliente actualizado exitosamente"}


# CRUD - Delete
@app.delete("/clientes/{id_cliente}")
async def eliminar_cliente(id_cliente: str) -> dict:
    """
    Eliminar un cliente.

    Parameters:
        id_cliente (str): Identificador del cliente a eliminar.

    Returns:
        dict: Mensaje de éxito en la eliminación del cliente.
    """
    if id_cliente not in clientes_df.index:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    clientes_df = clientes_df.drop(id_cliente)
    clientes_df.to_csv("clientes_segmentados.csv")
    return {"message": "Cliente eliminado exitosamente"}


@app.get("/grafica", response_class=StreamingResponse)
async def obtener_grafica() -> StreamingResponse:
    """
    Obtener gráfica de la proporción de clientes por segmento.
    """
    oro_customers_count = len(clientes_df[clientes_df["Cliente"] == "Oro"])
    plata_customers_count = len(clientes_df[clientes_df["Cliente"] == "Plata"])
    bronce_customers_count = len(clientes_df[clientes_df["Cliente"] == "Bronce"])

    classes = ["Oro", "Plata", "Bronce"]
    counts = [oro_customers_count, plata_customers_count, bronce_customers_count]

    fig, ax = plt.subplots()
    ax.bar(classes, counts, color=['gold', 'silver', 'brown'])
    ax.set_xlabel('Segmento')
    ax.set_ylabel('Cantidad de Clientes')
    ax.set_title('Segmentación de Clientes por RFM')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    
    return StreamingResponse(buf, media_type="image/png")



@app.get("/producto-más-consumido")
async def obtener_producto_mas_consumido(año: int, mes: int) -> dict:
    """
    Obtener el producto más consumido del mes.

    Parameters:
        año (int): Año de la consulta.
        mes (int): Mes de la consulta.

    Returns:
        dict: Información sobre el producto más consumido.
    """
    try:
        producto_mas_consumido = resultados_cohorte_df.loc[(resultados_cohorte_df["Año"] == año) &
                                                           (resultados_cohorte_df["Mes"] == mes),
                                                           "Consumido"].iloc[0]
    except IndexError:
        raise HTTPException(status_code=404, detail="No se encontraron datos para el año y mes especificados")

    return {"año": año, "mes": mes, "producto_mas_consumido": producto_mas_consumido}


@app.get("/productos-más-vendidos")
async def obtener_productos_mas_vendidos() -> dict:
    """
    Obtener lista de productos más vendidos.

    Returns:
        dict: Lista de productos más vendidos.
    """
    return productos_mas_vendidos_df.to_dict(orient="records")


@app.get("/productos-menos-vendidos")
async def obtener_productos_menos_vendidos() -> dict:
    """
    Obtener lista de productos menos vendidos.

    Returns:
        dict: Lista de productos menos vendidos.
    """
    return productos_menos_vendidos_df.to_dict(orient="records")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)