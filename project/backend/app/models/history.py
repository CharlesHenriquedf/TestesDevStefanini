from pydantic import BaseModel
from datetime import datetime

class History(BaseModel):
    user_id: str
    movie_title: str
    search_date: datetime

    def dict(self):
        """
        Retorna o objeto em formato de dicionário, necessário para salvar no MongoDB.
        """
        return {
            "user_id": self.user_id,
            "movie_title": self.movie_title,
            "search_date": self.search_date.isoformat()
        }
