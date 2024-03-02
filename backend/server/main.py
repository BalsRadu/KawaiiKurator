from fastapi import FastAPI, HTTPException, Depends
from .recommendations.anime_based import find_similar_animes
from .dependencies import get_anime_recommendation_dependencies
from .schemas.anime_schema import AnimeRecommendationRequest
from .init import init_app

app = FastAPI()

# Call init_app to perform initial setup
init_app()

@app.post("/recommendations/anime")
def get_anime_recommendations(request: AnimeRecommendationRequest, dependencies: dict = Depends(get_anime_recommendation_dependencies)):
    anime_name = request.anime_name
    try:
        recommendations = find_similar_animes(anime_name, dependencies['df_anime'], dependencies['anime_encoder'], dependencies['anime_weights'])
        return recommendations
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}