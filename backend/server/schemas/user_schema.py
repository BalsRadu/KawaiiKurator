from pydantic import BaseModel

class UserRecommendationRequest(BaseModel):
    username: str  # Changed from user_id to username