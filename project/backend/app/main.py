from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import settings
from app.api.endpoints import auth, movies, history
from app.core.logger import setup_logger

# Configurar logger global para gravar em arquivo e terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app/main_logger.log"),
        logging.StreamHandler(),  # Mantém logs no terminal (Docker logs)
    ],
)

# Logger específico para depuração
debug_logger = setup_logger("debug_logger", "logs/debug.log")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciador de ciclo de vida para conectar e desconectar do MongoDB."""
    max_retries = 5
    wait_seconds = 5

    for attempt in range(1, max_retries + 1):
        try:
            app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URI)
            app.database = app.mongodb_client["movie_database"]

            # Testar a conexão
            await app.mongodb_client.admin.command('ping')
            logging.info("Conectado ao MongoDB com sucesso.")
            break
        except Exception as e:
            logging.error(f"Tentativa {attempt} de {max_retries}: Falha ao conectar ao MongoDB.")
            logging.exception(e)

            if attempt == max_retries:
                logging.critical("Número máximo de tentativas alcançado. Encerrando a aplicação.")
                raise e

            logging.info(f"Aguardando {wait_seconds} segundos antes de tentar novamente...")
            await asyncio.sleep(wait_seconds)

    yield  # Ponto onde o FastAPI inicia o app

    app.mongodb_client.close()
    logging.info("Conexão com o MongoDB encerrada.")

# Inicializar a aplicação FastAPI com o lifespan
app = FastAPI(lifespan=lifespan)

# Configuração de CORS
origins = [
    "http://localhost:3000",  # Origem do frontend em desenvolvimento
    # Adicione outras origens permitidas se necessário
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão dos roteadores
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(movies.router, prefix="/search", tags=["search"])
app.include_router(history.router, prefix="/history", tags=["history"])




logging.info("Roteadores carregados: /auth, /search, /history")

