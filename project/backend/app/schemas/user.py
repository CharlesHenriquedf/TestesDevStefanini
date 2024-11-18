from pydantic import BaseModel, EmailStr
from app.core.logger import setup_logger

# Configuração do logger para schemas
logger = setup_logger(
    logger_name="schema_logger_user",
    log_file="logs/schemas/logs_schemas_user.log"
)

class UserBase(BaseModel):
    username: str
    email: EmailStr

    def __init__(self, **data):
        super().__init__(**data)
        logger.info(f"Esquema UserBase criado: {data}")

class UserCreate(UserBase):
    password: str

    def __init__(self, **data):
        super().__init__(**data)
        logger.info(f"Esquema UserCreate criado: {data}")

class UserResponse(UserBase):
    id: str

    class Config:
        orm_mode = True

    def __init__(self, **data):
        super().__init__(**data)
        logger.info(f"Esquema UserResponse criado: {data}")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    def __init__(self, **data):
        super().__init__(**data)
        logger.info(f"Esquema UserLogin criado: {data}")

