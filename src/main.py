"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # User profile: target values for each feature in data/songs.csv.
    # Numeric targets use the same 0-1 scale as the song data. tempo_bpm is in BPM.
    user_profile = {
        "genre": "trap",
        "mood": "intense",
        "energy": 0.85,
        "tempo_bpm": 135,
        "valence": 0.50,
        "danceability": 0.75,
        "acousticness": 0.10,
    }
    user_prefs = user_profile

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
