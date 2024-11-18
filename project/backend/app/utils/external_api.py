import httpx
from app.core.settings import settings
from app.core.logger import setup_logger

# Configuração do logger para a API externa
logger = setup_logger(
    logger_name="external_api_logger",
    log_file="logs/utils/external_api_logger.log"
)

async def fetch_movies(query: str):
    """
    Faz uma requisição para a API externa para buscar filmes.
    """
    url = f"https://the-one-api.dev/v2/movie"

    # Máscara do token para logs
    headers = {"Authorization": f"Bearer {settings.THE_ONE_API_KEY[:4]}****"}
    logger.info(f"Enviando requisição para {url} com headers {headers} e query '{query}'")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers={"Authorization": f"Bearer {settings.THE_ONE_API_KEY}"})

            logger.info(f"Resposta recebida com status {response.status_code}")

            if response.status_code == 200:
                movies = response.json().get("docs", [])
                logger.info(f"Filmes retornados pela API: {movies}")
                # Filtrar por query no título do filme
                filtered_movies = [
                    movie for movie in movies if query.lower() in movie["name"].lower()
                ]
                logger.info(f"Filmes filtrados com base na query '{query}': {filtered_movies}")
                return filtered_movies
            else:
                logger.warning(f"Erro na API externa: {response.text}")
                response.raise_for_status()
    except Exception as e:
        logger.error(f"Erro ao se comunicar com a API externa: {str(e)}")
        raise
