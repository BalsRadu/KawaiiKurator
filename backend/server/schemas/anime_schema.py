from pydantic import BaseModel

class AnimeRecommendationRequest(BaseModel):
    anime_name: str