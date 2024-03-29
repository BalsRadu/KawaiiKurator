# Add the parent directory to the path
import sys

sys.path.append("..")

### Basic libraries
import numpy as np
import pandas as pd
import torch

# Data Preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder

## Import necessary modules for content-based filtering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Import the recomandation model
from models.recommender_net import RecommenderNet

# Global variables
df_score = None
df_anime = None
user_encoder = None
anime_encoder = None
recommender_model = None
anime_weights = None
user_weights = None
cosine_sim_sparse = None


# Utility functions
def extract_weights(name, model):
    # Access the embedding layer directly by name
    weight_layer = getattr(model, name)

    # Get the weights from the layer; .weight returns the weight tensor for embeddings
    weights = weight_layer.weight.data

    # Normalize the weights
    # Calculate the L2 norm of the weights, keep the dimension for broadcasting
    norms = torch.norm(weights, p=2, dim=1, keepdim=True)

    # Use broadcasting to perform the normalization
    normalized_weights = weights / norms

    # Convert normalized weights to numpy array if necessary
    normalized_weights_np = normalized_weights.cpu().numpy()

    return normalized_weights_np


def filter_recommendations(df: pd.DataFrame, filters: dict):
    if filters is None:
        return df
    for key, value in filters.items():
        if value is not None:
            if key == "popularity":
                df = df[df["Popularity"] <= value]
            elif key == "score":
                df = df[df["Score"] >= value]
            elif key == "episodes":
                df = df[df["Episodes"] >= value]
            elif key == "genre":
                df = df[df["Genres"].str.contains(value, case=False, na=False)]
    return df


# Initialize the app
def init_app():
    global df_score
    global df_anime
    global user_encoder
    global anime_encoder
    global recommender_model
    global anime_weights
    global user_weights
    global cosine_sim_sparse

    # Load the dataset
    print("Loading the dataset...")
    df_score = pd.read_csv("../datasets/users-score-2023.csv")
    df_anime = pd.read_csv("../datasets/anime-dataset-2023.csv")

    # Scaling our "rating" column
    # Create a MinMaxScaler object
    print("Scaling the dataset...")
    scaler = MinMaxScaler(feature_range=(0, 1))
    # Scale the 'score' column between 0 and 1
    df_score["scaled_score"] = scaler.fit_transform(df_score[["rating"]])

    ## Encoding user IDs
    print("Encoding user IDs...")
    user_encoder = LabelEncoder()
    df_score["user_encoded"] = user_encoder.fit_transform(df_score["user_id"])
    num_users = len(user_encoder.classes_)

    ## Encoding anime IDs
    print("Encoding anime IDs...")
    anime_encoder = LabelEncoder()
    df_score["anime_encoded"] = anime_encoder.fit_transform(df_score["anime_id"])
    num_animes = len(anime_encoder.classes_)

    print("Filtering the dataset...")
    popularity_threshold = 50
    df_anime = df_anime.query("Members >= @popularity_threshold")

    print("Initializing the model...")
    recommender_model = RecommenderNet(num_users, num_animes)
    recommender_model.load_state_dict(
        torch.load("../models/anime_recommender_weights.pt")
    )
    anime_weights = extract_weights("anime_embedding", recommender_model)
    user_weights = extract_weights("user_embedding", recommender_model)

    print("Initializing the cosine similarity matrix...")
    # Create a TF-IDF vectorizer
    tfidf = TfidfVectorizer(stop_words="english")
    # Define a generator to compute TF-IDF matrix on the fly
    tfidf_matrix_generator = tfidf.fit_transform(
        (genre for genre in df_anime["Genres"].values.astype("U"))
    )
    # Compute cosine similarity matrix as a sparse matrix
    cosine_sim_sparse = linear_kernel(tfidf_matrix_generator, tfidf_matrix_generator)


# Getters for global variables
def get_model_instance():
    global recommender_model
    if recommender_model is None:
        raise ValueError("The model has not been initialized yet.")
    return recommender_model


def get_user_encoder_instance():
    global user_encoder
    if user_encoder is None:
        raise ValueError("The user encoder has not been initialized yet.")
    return user_encoder


def get_anime_encoder_instance():
    global anime_encoder
    if anime_encoder is None:
        raise ValueError("The anime encoder has not been initialized yet.")
    return anime_encoder


def get_df_score_instance():
    global df_score
    if df_score is None:
        raise ValueError("The dataframe has not been initialized yet.")
    return df_score


def get_df_anime_instance():
    global df_anime
    if df_anime is None:
        raise ValueError("The anime dataframe has not been initialized yet.")
    return df_anime


def get_anime_weights_instance():
    global anime_weights
    if anime_weights is None:
        raise ValueError("The anime weights have not been initialized yet.")
    return anime_weights


def get_user_weights_instance():
    global user_weights
    if user_weights is None:
        raise ValueError("The user weights have not been initialized yet.")
    return user_weights


def get_cosine_sim_sparse_instance():
    global cosine_sim_sparse
    if cosine_sim_sparse is None:
        raise ValueError("The cosine similarity matrix has not been initialized yet.")
    return cosine_sim_sparse
