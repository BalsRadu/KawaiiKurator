from fastapi import FastAPI, HTTPException, Depends
from recommendations.anime_based import find_similar_animes
from recommendations.user_based import find_similar_users, get_user_preferences, get_recommended_animes, lookup_user_id
from dependencies import get_anime_recommendation_dependencies, get_user_recommendation_dependencies
from schemas.anime_schema import AnimeRecommendationRequest
from schemas.user_schema import UserRecommendationRequest
from init import init_app

app = FastAPI()

# Call init_app to perform initial setup
init_app()

@app.get("/recommendations/anime")
def get_anime_recommendations(request: AnimeRecommendationRequest, dependencies: dict = Depends(get_anime_recommendation_dependencies)):
    anime_name = request.anime_name
    try:
        recommendations = find_similar_animes(anime_name, dependencies['df_anime'], dependencies['anime_encoder'], dependencies['anime_weights'])
        return recommendations
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.get("/recommendations/user")
def get_user_recommendations(request: UserRecommendationRequest, dependencies: dict = Depends(get_user_recommendation_dependencies)):
    username = request.username
    try:
        # Lookup user ID from username.
        user_id = lookup_user_id(username, dependencies['df_score'])
        # Find similar users
        similar_users = find_similar_users(username, dependencies['user_encoder'], dependencies['user_weights'], n=10)
        similar_users = similar_users[similar_users.similarity > 0.4]
        similar_users = similar_users[similar_users.similar_users != user_id]
        # Get user preferences
        user_pref = get_user_preferences(user_id, dependencies['df_score'], dependencies['df_anime'])
        # Get recommended animes based on similar users' preferences
        recommended_animes = get_recommended_animes(similar_users, user_pref, dependencies['df_score'], dependencies['df_anime'], n=5)
        return recommended_animes
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")