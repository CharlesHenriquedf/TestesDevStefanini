from pydantic import BaseModel
from datetime import date
from app.core.logger import setup_logger

# Configuração do logger para schemas
logger = setup_logger(
    logger_name="schema_logger_history",
    log_file="logs/schemas/logs_schemas_history.log"
)

class HistoryBase(BaseModel):
    user_id: str
    movie_title: str
    search_date: date

    def __init__(self, **data):
        super().__init__(**data)
        logger.info(f"Esquema HistoryBase criado: {data}")

class HistoryCreate(HistoryBase):
    pass  # Igual ao HistoryBase para criação

class HistoryResponse(HistoryBase):
    id: str

    class Config:
        orm_mode = True

    def __init__(self, **data):
        super().__init__(**data)
        logger.info(f"Esquema HistoryResponse criado: {data}")
