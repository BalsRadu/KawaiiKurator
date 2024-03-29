# FastAPI application entry point
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

# Recommendation functions
from recommendations.anime_based import find_similar_animes
from recommendations.user_based import (
    find_similar_users,
    get_user_preferences,
    get_recommended_animes,
    lookup_user_id,
)
from recommendations.content_based import (
    get_content_recommendations,
)

# Dependencies
from dependencies import (
    get_anime_recommendation_dependencies,
    get_user_recommendation_dependencies,
    get_content_based_dependencies,
)

# Initialization script
from init import init_app

app = FastAPI()

# Add CORSMiddleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Allowed methods
    allow_headers=["*"],  # Allowed all headers
)

# Call init_app to perform initial setup
init_app()


@app.get("/recommendations/anime")
def get_anime_recommendations(
    anime_name: str,
    popularity: int = None,
    score: float = None,
    episodes: int = None,
    genre: str = None,
    dependencies: dict = Depends(get_anime_recommendation_dependencies),
):
    try:

        filters = {
            "popularity": popularity,
            "score": score,
            "episodes": episodes,
            "genre": genre,
        }

        recommendations = find_similar_animes(
            anime_name,
            filters,
            dependencies["df_anime"],
            dependencies["anime_encoder"],
            dependencies["anime_weights"],
        )
        return recommendations
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


@app.get("/recommendations/user")
def get_user_recommendations(
    username: str,
    popularity: int = None,
    score: float = None,
    episodes: int = None,
    genre: str = None,
    dependencies: dict = Depends(get_user_recommendation_dependencies),
):
    try:
        filters = {
            "popularity": popularity,
            "score": score,
            "episodes": episodes,
            "genre": genre,
        }

        # Lookup user ID from username.
        user_id = lookup_user_id(username, dependencies["df_score"])

        # Find similar users
        similar_users = find_similar_users(
            int(user_id),
            dependencies["user_encoder"],
            dependencies["user_weights"],
            n=10,
        )

        # get top 5 similar users
        similar_users = similar_users[similar_users.similar_users != user_id]
        similar_users = similar_users[:10]

        # Get user preferences
        user_pref = get_user_preferences(
            user_id, dependencies["df_score"], dependencies["df_anime"]
        )

        # Get recommended animes based on similar users' preferences
        recommended_animes = get_recommended_animes(
            similar_users,
            user_pref,
            filters,
            dependencies["df_score"],
            dependencies["df_anime"],
            n=5,
        )

        return recommended_animes
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


@app.get("/recommendations/content")
def get_content_based_recommendations(
    anime_title: str,
    popularity: int = None,
    score: float = None,
    episodes: int = None,
    genre: str = None,
    dependencies: dict = Depends(get_content_based_dependencies),
):
    try:
        filters = {
            "popularity": popularity,
            "score": score,
            "episodes": episodes,
            "genre": genre,
        }

        # Get content-based recommendations
        recommendations = get_content_recommendations(
            anime_title,
            filters,
            dependencies["cosine_sim"],
            dependencies["df_anime"],
            n=5,
        )
        return recommendations
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
