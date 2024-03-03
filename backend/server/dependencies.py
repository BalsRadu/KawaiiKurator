from init import get_anime_encoder_instance, get_anime_weights_instance, get_model_instance, get_user_encoder_instance, get_user_weights_instance, get_df_anime_instance, get_df_score_instance

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

def get_cosine_sim_sparse_instance():
    # This function returns the cosine similarity matrix as a sparse matrix.
    return get_cosine_sim_sparse_instance()

def get_anime_recommendation_dependencies():
    # This function aggregates the dependencies required for the anime  recommendation functionality.
    return {
        "df_anime": get_df_anime(),
        "anime_encoder": get_anime_encoder(),
        "anime_weights": get_anime_weights(),
    }

def get_user_recommendation_dependencies():
    # This function aggregates the dependencies required for the user recommendation functionality.
    return {
        "df_score": get_df_score(),
        "user_encoder": get_user_encoder(),
        "user_weights": get_user_weights(),
        "df_anime": get_df_anime(),
    }

def get_content_based_dependencies():
    # This function aggregates the dependencies required for the content-based recommendation functionality.
    return {
        "df_anime": get_df_anime(),
        "cosine_sim": get_cosine_sim_sparse_instance(),
    }