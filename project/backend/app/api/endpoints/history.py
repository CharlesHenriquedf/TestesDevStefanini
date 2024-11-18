from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from pymongo.database import Database
from app.api.dependencies import get_database, get_current_user
from app.models.history import History
from app.schemas.user import UserResponse
from app.core.logger import setup_logger

# Configuração do logger para a rota
logger = setup_logger(
    logger_name="history_logger",
    log_file="logs/endpoints/history_logger.log"
)

router = APIRouter()  # Certifique-se de que esta linha está presente

def serialize_history(history):
    """
    Serializa um documento do MongoDB convertendo o _id para string.
    """
    history["_id"] = str(history["_id"])
    return history

@router.post("/")
async def save_search(
    query: str, 
    db: Database = Depends(get_database), 
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Salva uma busca no histórico do usuário.
    """
    logger.info(f"Recebendo solicitação para salvar busca: query={query}, usuário={current_user.id}")
    history_entry = History(
        user_id=current_user.id,
        movie_title=query,
        search_date=datetime.utcnow()
    )
    result = await db.history.insert_one(history_entry.dict())
    if result.inserted_id:
        logger.info(f"Busca salva com sucesso: {history_entry.dict()}")
        return {"message": "Search saved successfully"}
    logger.error("Erro ao salvar a busca no banco de dados.")
    raise HTTPException(status_code=500, detail="Error saving search")

@router.get("/")
async def get_history(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Database = Depends(get_database), 
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Retorna o histórico de buscas do usuário com paginação.
    """
    logger.info(f"Recebida solicitação para obter histórico: página={page}, limite={limit}, usuário ID={current_user.id}")
    skip = (page - 1) * limit
    user_history = await db.history.find({"user_id": current_user.id}).skip(skip).limit(limit).to_list(length=limit)
    serialized_history = [serialize_history(entry) for entry in user_history]  # Serializar o histórico

    total_count = await db.history.count_documents({"user_id": current_user.id})
    response = {
        "history": serialized_history,
        "pagination": {
            "page": page,
            "limit": limit,
            "total_count": total_count,
            "total_pages": (total_count // limit) + (1 if total_count % limit > 0 else 0)
        }
    }
    logger.info(f"Histórico retornado com sucesso: {response}")
    return response
