import time
from typing import Dict, Optional
from jose import jwt, JWTError

# Clave secreta para la firma del JWT
SECRET_KEY: str = "tu_clave_secreta"
# Algoritmo de firma utilizado
ALGORITHM: str = "HS256"

def create_jwt(data: Dict[str, str], expires_delta: int = 3600) -> str:
    """
    Crea un token JWT (JSON Web Token) utilizando la información proporcionada.

    Args:
        data (Dict[str, str]): Datos a incluir en el token.
        expires_delta (int, optional): Duración de validez del token en segundos. 
                                       Por defecto es 3600 segundos (1 hora).

    Returns:
        str: Token JWT generado.
    """
    to_encode = data.copy()
    expire = time.time() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_jwt(token: str) -> Optional[Dict[str, str]]:
    """
    Decodifica un token JWT y devuelve la información contenida si el token es válido.

    Args:
        token (str): Token JWT a decodificar.

    Returns:
        Optional[Dict[str, str]]: Información contenida en el token si es válido, 
                                   None si el token no es válido.
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except JWTError:
        return None
