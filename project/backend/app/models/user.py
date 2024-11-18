from app.core.logger import setup_logger

# Configuração do logger para a pasta models
logger = setup_logger(
    logger_name="model_logger_user",
    log_file="logs/models/logs_models_user.log"
)

class User:
    def __init__(self, username: str, email: str, user_id: str = None):
        self.username = username
        self.email = email
        self.user_id = user_id  # Adicionado para refletir o campo "id" esperado no schema
        logger.info(f"Usuário criado: {self.__dict__}")

    def update_email(self, new_email: str):
        try:
            logger.info(f"Atualizando e-mail para: {new_email}")
            self.email = new_email
            logger.info("E-mail atualizado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao atualizar e-mail: {e}")
            raise
