# Function to get recommendations based on cosine similarity, genre, and ratings based on score
def get_content_recommendations(title, cosine_sim, df_anime, n=5):
    idx = df_anime[df_anime["Name"] == title].index[0]

    # Compute the similarity scores between the anime at the given index and all other animes
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Filter out animes with unknown scores
    valid_scores = [x for x in sim_scores if df_anime.iloc[x[0]]["Score"] != "UNKNOWN"]

    # Sort the valid anime similarity scores based on the cosine similarity and ratings score in descending order
    sorted_scores = sorted(
        valid_scores, key=lambda x: (x[1], df_anime.iloc[x[0]]["Score"]), reverse=True
    )

    # Get the top 10 similar animes (excluding the anime itself)
    top_animes = [x for x in sorted_scores if x[0] != idx][:10]

    # Extract the indices of the recommended animes
    recommended_indices = [idx for idx, _ in top_animes]
    recommended_animes = df_anime.iloc[recommended_indices][
        ["Name", "Genres", "Score", "Synopsis", "Image URL"]
    ]

    return recommended_animes.head(n).to_dict("records")
