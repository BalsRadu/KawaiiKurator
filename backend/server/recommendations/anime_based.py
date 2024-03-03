import pandas as pd
import numpy as np

def find_similar_animes(name, df_anime, anime_encoder, anime_weights, n=5, neg=False):
    try:
        anime_row = df_anime[df_anime['Name'] == name].iloc[0]
        index = anime_row['anime_id']
        encoded_index = anime_encoder.transform([index])[0]
        weights = anime_weights
        dists = np.dot(weights, weights[encoded_index])
        sorted_dists = np.argsort(dists)
        n = n + 1  # To account for the anime itself in the results
        if neg:
            closest = sorted_dists[:n]
        else:
            closest = sorted_dists[-n:]

        similarity_arr = []

        for close in closest:
            decoded_id = anime_encoder.inverse_transform([close])[0]
            anime_frame = df_anime[df_anime['anime_id'] == decoded_id]

            display_name = anime_frame['Name'].values[0]
            score = anime_frame['Score'].values[0]
            genres = anime_frame['Genres'].values[0]
            synopsis = anime_frame['Synopsis'].values[0]
            image_url = anime_frame['Image URL'].values[0]
            similarity = dists[close]
            similarity_percentage = "{:.2f}%".format(similarity * 100)

            similarity_arr.append({
                "Name": display_name,
                "Score": score,
                "Genres": genres,
                "Synopsis": synopsis,
                "Image URL": image_url,
            })

        # Excluding the queried anime from the results if it's in the list
        result_frame = pd.DataFrame(similarity_arr).sort_values(by="Similarity", ascending=False)
        return result_frame[result_frame.Name != name].head(n).to_dict('records')
    except Exception as e:
        raise ValueError(f'Error finding similar animes for {name}: {str(e)}')