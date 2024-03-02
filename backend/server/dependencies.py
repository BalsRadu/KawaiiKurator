from .init import get_anime_encoder_instance, get_anime_weights_instance, get_model_instance, get_user_encoder_instance, get_user_weights_instance, get_df_anime_instance, get_df_score_instance

def get_model():
    return get_model_instance()

def get_user_encoder():
    return get_user_encoder_instance()

def get_anime_encoder():
    return get_anime_encoder_instance()

def get_anime_weights():
    return get_anime_weights_instance()

def get_user_weights():
    return get_user_weights_instance()

def get_df_anime():
    return get_df_anime_instance()

def get_df_score():
    return get_df_score_instance()

def get_anime_recommendation_dependencies():
    # This function aggregates the dependencies required for the anime  recommendation functionality.
    return {
        "df_anime": get_df_anime(),
        "anime_encoder": get_anime_encoder(),
        "anime_weights": get_anime_weights(),
    }