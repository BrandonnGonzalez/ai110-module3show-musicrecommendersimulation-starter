import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_tempo: float
    target_valence: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        preferences = _user_profile_to_prefs(user)
        scored_songs = []

        for song in self.songs:
            song_data = _song_to_dict(song)
            score, _ = score_song(preferences, song_data)
            scored_songs.append((score, song))

        scored_songs.sort(key=lambda item: item[0], reverse=True)
        return [song for _, song in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        preferences = _user_profile_to_prefs(user)
        song_data = _song_to_dict(song)
        score, reasons = score_song(preferences, song_data)

        explanation = f"Score: {score:.2f}."
        if reasons:
            explanation += " Reasons: " + ", ".join(reasons)
        else:
            explanation += " No strong matches found."

        return explanation


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    if song["genre"].lower() == user_prefs.get("favorite_genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"].lower() == user_prefs.get("favorite_mood", "").lower():
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_score = _similarity(user_prefs.get("target_energy", 0.0), song["energy"], 1.0) * 1.0
    if energy_score > 0:
        score += energy_score
        reasons.append(f"energy similarity (+{energy_score:.2f})")

    tempo_score = _similarity(user_prefs.get("target_tempo", 0.0), song["tempo_bpm"], 200.0) * 0.5
    if tempo_score > 0:
        score += tempo_score
        reasons.append(f"tempo similarity (+{tempo_score:.2f})")

    valence_score = _similarity(user_prefs.get("target_valence", 0.0), song["valence"], 1.0) * 0.5
    if valence_score > 0:
        score += valence_score
        reasons.append(f"valence similarity (+{valence_score:.2f})")

    if user_prefs.get("likes_acoustic", False):
        acoustic_score = song.get("acousticness", 0.0) * 1.0
        if acoustic_score > 0:
            score += acoustic_score
            reasons.append(f"acousticness bonus (+{acoustic_score:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    ranked: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "No strong matches found."
        ranked.append((song, score, explanation))

    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked[:k]


def _similarity(target: float, value: float, scale: float) -> float:
    difference = abs(target - value)
    return max(0.0, 1.0 - (difference / scale))


def _song_to_dict(song: Song) -> Dict:
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "tempo_bpm": song.tempo_bpm,
        "valence": song.valence,
        "danceability": song.danceability,
        "acousticness": song.acousticness,
    }


def _user_profile_to_prefs(user: UserProfile) -> Dict:
    return {
        "favorite_genre": user.favorite_genre,
        "favorite_mood": user.favorite_mood,
        "target_energy": user.target_energy,
        "target_tempo": user.target_tempo,
        "target_valence": user.target_valence,
        "likes_acoustic": user.likes_acoustic,
    }
