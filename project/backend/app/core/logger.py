import logging
import os

def setup_logger(logger_name, log_file, level=logging.INFO):

    
    """
    Configurações dos Logs.

    :param logger_name: Nome do logger.
    :param log_file: Caminho do arquivo de log.
    :param level: Nível do log.
    :return: Logger configurado.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Cria o diretório se não existir
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Configuração do manipulador de arquivos
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    # Formato de log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)

    # Evitar múltiplos manipuladores no mesmo logger
    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger
