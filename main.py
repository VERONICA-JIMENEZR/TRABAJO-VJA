from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
import pandas as pd
import matplotlib.pyplot as plt
import io

app = FastAPI()
security = HTTPBasic()

# Token de seguridad
fake_users_db = {
    "user": "password"
}

# Cargar la base de datos de clientes segmentados
clientes_df = pd.read_csv("clientes_segmentados.csv", index_col="ID cliente")

# Cargar la base de datos de productos más vendidos y menos vendidos
productos_mas_vendidos_df = pd.read_csv("productos_mas_vendidos.csv")
productos_menos_vendidos_df = pd.read_csv("productos_menos_vendidos.csv")

# Cargar la base de datos de resultados de cohorte
resultados_cohorte_df = pd.read_csv("resultados_cohorte.csv", parse_dates=["Año", "Mes"], index_col=["Año", "Mes"])


def obtener_porcentaje_clientes(segmento: str) -> float:
    total = len(clientes_df)
    clientes_segmento = clientes_df[clientes_df["Cliente"] == segmento.capitalize()]
    cantidad = len(clientes_segmento)
    porcentaje = cantidad / total * 100
    return porcentaje


@app.get("/clientes/{segmento}")
async def obtener_clientes(segmento: str, credentials: HTTPBasicCredentials = Depends(security)):
    """
    Obtener clientes por segmento.
    """
    if segmento.lower() not in ["oro", "plata", "bronce"]:
        raise HTTPException(status_code=404, detail="Segmento no válido")

    clientes_segmento = clientes_df[clientes_df["Cliente"] == segmento.capitalize()]
    clientes = clientes_segmento["Nombre"].tolist()
    cantidad = len(clientes)
    porcentaje = obtener_porcentaje_clientes(segmento)

    return {
        "segmento": segmento.capitalize(),
        "clientes": clientes,
        "cantidad": cantidad,
        "porcentaje": f"{porcentaje:.2f}%"
    }


@app.get("/grafica")
async def obtener_grafica():
    """
    Obtener gráfica de la proporción de clientes por segmento.
    """
    fig, ax = plt.subplots()
    counts = clientes_df["Cliente"].value_counts()
    counts.plot(kind="bar", ax=ax)
    ax.set_xlabel("Segmento")
    ax.set_ylabel("Cantidad de clientes")
    ax.set_title("Cantidad de clientes por segmento")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    # Convertir la gráfica en un archivo de imagen
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)

    return img


@app.get("/token")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Obtener token de autenticación.
    """
    correct_username = fake_users_db.get(credentials.username)
    correct_password = fake_users_db.get(credentials.password)
    if not (correct_username and correct_password and
            correct_username == credentials.username and
            correct_password == credentials.password):
        return JSONResponse(status_code=401, content={"message": "Incorrect email or password"})
    return {"token": "fake_token"}


# CRUD - Create
@app.post("/clientes/agregar")
async def agregar_cliente(nombre: str, cliente: str, credentials: HTTPBasicCredentials = Depends(security)):
    """
    Agregar un nuevo cliente.
    """
    if cliente.lower() not in ["oro", "plata", "bronce"]:
        raise HTTPException(status_code=404, detail="Segmento no válido")

    nuevos_datos = pd.DataFrame({"Nombre": [nombre], "Cliente": [cliente.capitalize()]})
    global clientes_df
    clientes_df = pd.concat([clientes_df, nuevos_datos])
    clientes_df.to_csv("clientes_segmentados.csv")
    return {"message": "Cliente agregado exitosamente"}


# CRUD - Update
@app.put("/clientes/{id_cliente}")
async def actualizar_cliente(id_cliente: str, nombre: str, cliente: str,
                             credentials: HTTPBasicCredentials = Depends(security)):
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
async def eliminar_cliente(id_cliente: str, credentials: HTTPBasicCredentials = Depends(security)):
    """
    Eliminar un cliente.
    """
    if id_cliente not in clientes_df.index:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    clientes_df = clientes_df.drop(id_cliente)
    clientes_df.to_csv("clientes_segmentados.csv")
    return {"message": "Cliente eliminado exitosamente"}


@app.get("/producto-del-mes/{año}/{mes}")
async def obtener_producto_del_mes(año: int, mes: int):
    """
    Obtener el producto más consumido del mes.
    """
    try:
        producto_del_mes = resultados_cohorte_df.loc[(año, mes), "Consumido"]
    except KeyError:
        raise HTTPException(status_code=404, detail="No se encontraron datos para el año y mes especificados")

    return {"mensaje": "Producto más consumido del mes", "año": año, "mes": mes, "producto": producto_del_mes}


@app.get("/productos-mas-vendidos")
async def obtener_productos_mas_vendidos():
    """
    Obtener lista de productos más vendidos.
    """
    return productos_mas_vendidos_df.to_dict(orient="records")


@app.get("/productos-menosvendidos")
async def obtener_productos_menos_vendidos():
    """
    Obtener lista de productos menos vendidos.
"""
    return productos_menos_vendidos_df.to_dict(orient="records")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
