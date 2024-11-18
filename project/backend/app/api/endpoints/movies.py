from fastapi import APIRouter, HTTPException, Depends, Query
from app.utils.external_api import fetch_movies
from app.api.dependencies import get_database, get_current_user
from app.schemas.user import UserResponse
from app.api.endpoints.history import save_search  # Corrigido o caminho da importação
from app.core.logger import setup_logger

# Configuração do logger para filmes
logger = setup_logger(
    logger_name="movies_logger",
    log_file="logs/endpoints/movies_logger.log"
)

router = APIRouter()

@router.get("/")
async def search_movies(
    query: str = Query(..., description="Termo para buscar filmes."),
    db=Depends(get_database),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Endpoint para buscar filmes usando a API externa.
    """
    logger.info(f"Recebendo requisição para /search com query='{query}'")
    logger.info(f"Usuário autenticado: {current_user.id}")

    try:
        # Busca os filmes da API externa
        movies = await fetch_movies(query)
        if not movies:
            logger.info("Nenhum filme encontrado para a query fornecida.")
            raise HTTPException(status_code=404, detail="No movies found")
        
        # Salvar busca no histórico
        await save_search(query=query, db=db, current_user=current_user)
        logger.info(f"Busca salva no histórico para a query='{query}'")

        return {"results": movies}
    except HTTPException as e:
        logger.warning(f"Erro HTTP na busca de filmes: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Erro ao buscar filmes: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
