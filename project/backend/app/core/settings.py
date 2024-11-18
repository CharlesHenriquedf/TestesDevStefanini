from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """
    Configurações globais da aplicação, utilizando Pydantic para validação.
    """
    MONGODB_URI: str = Field(..., env="MONGODB_URI", description="URI de conexão com o MongoDB")
    SECRET_KEY: str = Field(..., env="SECRET_KEY", description="Chave secreta para geração de tokens JWT")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM", description="Algoritmo para assinatura de tokens JWT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES", description="Tempo de expiração dos tokens de acesso")
    THE_ONE_API_KEY: str = Field(..., env="THE_ONE_API_KEY", description="Chave para acessar a API externa")

    class Config:
        """
        Configurações adicionais para integração com variáveis de ambiente.
        """
        env_file = ".env"  # Arquivo de variáveis de ambiente
        env_file_encoding = "utf-8"  # Codificação do arquivo .env
        case_sensitive = True  # Variáveis de ambiente são case-sensitive

# Instância global de configurações
settings = Settings()

