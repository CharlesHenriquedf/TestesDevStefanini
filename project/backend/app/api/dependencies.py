from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.settings import settings
from motor.motor_asyncio import AsyncIOMotorClient
from app.schemas.user import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_database():
    """
    Dependência para obter o banco de dados.
    """
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    return client["consulta_filmes"]

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependência para autenticar o usuário via token JWT.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return UserResponse(id=user_id, username="TestUser", email="test@example.com")  # Substituir com consulta ao banco
    except JWTError:
        raise credentials_exception
