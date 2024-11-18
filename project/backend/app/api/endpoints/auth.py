from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.api.dependencies import get_database
from pymongo.database import Database
from app.core.settings import settings
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Database = Depends(get_database)):
    """
    Função para validar o usuário atual baseado no token JWT.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_data = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user_data:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Mapear o retorno para UserResponse
        return UserResponse(
            id=str(user_data["_id"]),
            username=user_data["username"],
            email=user_data["email"]
        )
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Database = Depends(get_database)):
    """
    Endpoint para registrar um novo usuário.
    """
    user_data = await db.users.find_one({"email": user.email})
    if user_data:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    user_id = await db.users.insert_one({"username": user.username, "email": user.email, "password": hashed_password})
    return UserResponse(id=str(user_id.inserted_id), username=user.username, email=user.email)

@router.post("/login")
async def login_user(user: UserLogin, db: Database = Depends(get_database)):
    """
    Endpoint para login.
    """
    user_data = await db.users.find_one({"email": user.email})
    if not user_data or not verify_password(user.password, user_data["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token({"sub": str(user_data["_id"])})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/protected")
async def protected_route(current_user: UserResponse = Depends(get_current_user)):
    """
    Rota protegida que retorna uma mensagem personalizada para o usuário autenticado.
    """
    return {"message": f"Welcome {current_user.username}, this is a protected route!"}

