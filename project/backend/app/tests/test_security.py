from app.core.logger import setup_logger
from app.core.security import encrypt_password, verify_password
from httpx import AsyncClient
from app.main import app


# Configuração do logger para os testes
logger = setup_logger(
    logger_name="test_security_logger",
    log_file="logs/tests/logs_tests.log"
)

def test_encrypt_password():
    """
    Testa a função encrypt_password.
    """
    try:
        logger.info("Iniciando teste para encrypt_password.")
        password = "my_password"
        encrypted = encrypt_password(password)
        assert encrypted == f"encrypted_{password}"
        logger.info("Teste encrypt_password concluído com sucesso.")
    except AssertionError as e:
        logger.error(f"Erro no teste encrypt_password: {e}")
        raise

def test_verify_password():
    """
    Testa a função verify_password.
    """
    try:
        logger.info("Iniciando teste para verify_password.")
        password = "my_password"
        encrypted = encrypt_password(password)
        is_valid = verify_password(encrypted, password)
        assert is_valid is True

        is_invalid = verify_password(encrypted, "wrong_password")
        assert is_invalid is False
        logger.info("Teste verify_password concluído com sucesso.")
    except AssertionError as e:
        logger.error(f"Erro no teste verify_password: {e}")
        raise
