from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import pandas as pd
import matplotlib.pyplot as plt
import io
from typing import Optional

app = FastAPI()

# Security
fake_users_db = {
    "user": {
        "username": "user",
        "full_name": "Usuario Normal",
        "email": "user@example.com",
        "hashed_password": "fakehashedpassword",
        "disabled": False,
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Load the database
clientes_df = pd.read_csv("clientes_segmentados.csv", index_col="ID cliente")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


def fake_hash_password(password: str):
    return "fakehashed" + password


def verify_password(plain_password, hashed_password):
    return fake_hash_password(plain_password) == hashed_password


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict):
    return {"access_token": "fake-token", "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return User(username="user")


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return access_token


@app.get("/clientes/{segmento}")
async def obtener_clientes(segmento: str, current_user: User = Depends(get_current_user)):
    if segmento.lower() not in ["oro", "plata", "bronce"]:
        raise HTTPException(status_code=404, detail="Segmento no válido")

    clientes_segmento = clientes_df[clientes_df["Cliente"] == segmento.capitalize()]
    clientes = clientes_segmento["Nombre"].tolist()
    cantidad = len(clientes)
    total = len(clientes_df)
    porcentaje = cantidad / total * 100

    return {
        "segmento": segmento.capitalize(),
        "clientes": clientes,
        "cantidad": cantidad,
        "porcentaje": f"{porcentaje:.2f}%"
    }


@app.get("/grafica")
async def obtener_grafica(current_user: User = Depends(get_current_user)):
    counts = clientes_df["Cliente"].value_counts()
    counts.plot(kind="bar")
    plt.xlabel("Segmento")
    plt.ylabel("Cantidad de clientes")
    plt.title("Cantidad de clientes por segmento")
    plt.xticks(rotation=45)
    
    # Convertir la gráfica en un archivo de imagen
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    
    return img


# CRUD operations
@app.get("/clientes/")
async def read_clientes(current_user: User = Depends(get_current_user)):
    return clientes_df.to_dict(orient="index")


@app.post("/clientes/")
async def create_cliente(cliente: dict, current_user: User = Depends(get_current_user)):
    # You might want to validate the input before directly appending it to the DataFrame
    clientes_df = clientes_df.append(pd.DataFrame(cliente, index=[0]))
    return {"detail": "Cliente creado con éxito"}


@app.put("/clientes/{cliente_id}")
async def update_cliente(cliente_id: str, cliente: dict, current_user: User = Depends(get_current_user)):
    if cliente_id not in clientes_df.index:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Update the cliente data
    clientes_df.loc[cliente_id] = cliente
    return {"detail": "Cliente actualizado con éxito"}


@app.delete("/clientes/{cliente_id}")
async def delete_cliente(cliente_id: str, current_user: User = Depends(get_current_user)):
    if cliente_id not in clientes_df.index:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Delete the cliente
    clientes_df.drop(index=cliente_id, inplace=True)
    return {"detail": "Cliente eliminado con éxito"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
