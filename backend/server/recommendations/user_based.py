import pandas as pd
import numpy as np

from init import filter_recommendations


def lookup_user_id(username, df_score):
    user_info = df_score[df_score["Username"] == username]
    if not user_info.empty:
        return user_info.iloc[0]["user_id"]
    return None


def find_similar_users(item_input, user_encoder, user_weights, n=10, neg=False):
    try:
        index = item_input
        encoded_index = user_encoder.transform([index])[0]

        weights = user_weights
        dists = np.dot(weights, weights[encoded_index])
        sorted_dists = np.argsort(dists)
        n = n + 1

        if neg:
            closest = sorted_dists[:n]
        else:
            closest = sorted_dists[-n:]

        SimilarityArr = []

        for close in closest:
            similarity = dists[close]

            decoded_id = user_encoder.inverse_transform([close])[0]
            SimilarityArr.append(
                {"similar_users": decoded_id, "similarity": similarity}
            )

        Frame = pd.DataFrame(SimilarityArr).sort_values(
            by="similarity", ascending=False
        )
        return Frame
    except Exception as e:
        raise ValueError("\033[1m{}\033[0m, Not Found in User list".format(item_input))


def get_user_preferences(user_id, df_score, df_anime):
    animes_watched_by_user = df_score[df_score["user_id"] == user_id]

    if animes_watched_by_user.empty:
        raise ValueError("User #{} has not watched any animes.".format(user_id))

    user_rating_percentile = np.percentile(animes_watched_by_user.rating, 75)
    animes_watched_by_user = animes_watched_by_user[
        animes_watched_by_user.rating >= user_rating_percentile
    ]
    top_animes_user = animes_watched_by_user.sort_values(
        by="rating", ascending=False
    ).anime_id.values

    anime_df_rows = df_anime[df_anime["anime_id"].isin(top_animes_user)]
    anime_df_rows = anime_df_rows[["Name", "Genres"]]

    return anime_df_rows


def get_recommended_animes(similar_users, user_pref, filters, df_score, df_anime, n=5):
    recommended_animes = []
    anime_list = []

    for user_id in similar_users.similar_users.values:
        pref_list = get_user_preferences(int(user_id), df_score, df_anime)
        if not pref_list.empty:  # Check if user has watched any animes
            pref_list = pref_list[~pref_list["Name"].isin(user_pref["Name"].values)]
            anime_list.append(pref_list.Name.values)

    if len(anime_list) == 0:
        raise ValueError("No anime recommendations available for the given users.")

    anime_list = pd.DataFrame(anime_list)
    sorted_list = pd.DataFrame(
        pd.Series(anime_list.values.ravel()).value_counts()
    ).head(n)
    # Count the occurrences of each anime in the entire dataset
    anime_count = df_score["anime_id"].value_counts()

    for i, anime_name in enumerate(sorted_list.index):
        if isinstance(anime_name, str):
            try:
                anime_id = df_anime[df_anime.Name == anime_name].anime_id.values[0]
                english_name = df_anime[df_anime["Name"] == anime_name][
                    "English name"
                ].values[0]
                display_name = anime_name
                score = float(
                    df_anime[df_anime.Name == anime_name].Score.values[0]
                    if df_anime[df_anime.Name == anime_name].Score.values[0]
                    != "UNKNOWN"
                    else 0
                )
                image_url = df_anime[df_anime.Name == anime_name]["Image URL"].values[0]
                genre = df_anime[df_anime.Name == anime_name].Genres.values[0]
                Synopsis = df_anime[df_anime.Name == anime_name].Synopsis.values[0]
                popularity = df_anime[df_anime.Name == anime_name].Popularity.values[0]
                episodes = float(
                    df_anime[df_anime.Name == anime_name].Episodes.values[0]
                    if df_anime[df_anime.Name == anime_name].Episodes.values[0]
                    != "UNKNOWN"
                    else 0
                )
                n_user_pref = anime_count.get(
                    anime_id, 0
                )  # Get the total count of users who have watched this anime
                recommended_animes.append(
                    {
                        "Name": display_name,
                        "Score": score,
                        "Genres": genre,
                        "Popularity": popularity,
                        "Episodes": episodes,
                        "Synopsis": Synopsis,
                        "Image URL": image_url,
                        "Total Preferences": n_user_pref,
                    }
                )
            except:
                pass

    result_frame = pd.DataFrame(recommended_animes)
    result_frame = filter_recommendations(result_frame, filters)

    return result_frame.head(n).to_dict("records")
