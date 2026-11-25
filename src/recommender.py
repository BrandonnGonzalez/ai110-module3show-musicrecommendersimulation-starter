import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# --- Scoring configuration -------------------------------------------------

# Tolerance width for the linear proximity score. A song whose value is this
# far (or farther) from the user's target earns 0 points for that feature.
DEFAULT_WIDTH = 0.5

# Weights for the numeric features. Mood (0.25) and genre (0.20) will be added
# when categorical scoring is implemented.
NUMERIC_WEIGHTS: Dict[str, float] = {
    "energy": 0.35,
    "valence": 0.15,
    "acousticness": 0.05,
}

# `likes_acoustic` is turned into an acousticness target on the 0-1 scale.
ACOUSTIC_TARGET_IF_LIKED = 0.80
ACOUSTIC_TARGET_IF_NOT_LIKED = 0.20


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
    likes_acoustic: bool
    # Optional so existing four-argument construction keeps working.
    target_valence: Optional[float] = None


def proximity_score(value: float, target: float, width: float = DEFAULT_WIDTH) -> float:
    """
    Scores how close `value` is to `target` on a 0-1 scale: 1.0 for an exact
    match, falling in a straight line to 0.0 once the distance reaches `width`.

        score = max(0, 1 - |value - target| / width)

    Both inputs are clamped to [0, 1], so this is meant for features already on
    that scale (energy, valence, acousticness). Normalize others (e.g. tempo) first.
    """
    if width <= 0:
        raise ValueError("width must be greater than 0")
    value = min(max(value, 0.0), 1.0)
    target = min(max(target, 0.0), 1.0)
    return max(0.0, 1.0 - abs(value - target) / width)


def acousticness_target(likes_acoustic: bool) -> float:
    """Maps the user's likes_acoustic flag to a target acousticness value."""
    return ACOUSTIC_TARGET_IF_LIKED if likes_acoustic else ACOUSTIC_TARGET_IF_NOT_LIKED


def numeric_targets(user_prefs: Dict) -> Dict[str, float]:
    """
    Extracts the user's numeric targets from a preferences dict.
    Features the user did not specify are left out, so they are skipped in scoring.
    Recognized keys: "energy", "valence", "likes_acoustic".
    """
    targets: Dict[str, float] = {}
    if user_prefs.get("energy") is not None:
        targets["energy"] = float(user_prefs["energy"])
    if user_prefs.get("valence") is not None:
        targets["valence"] = float(user_prefs["valence"])
    if user_prefs.get("likes_acoustic") is not None:
        targets["acousticness"] = acousticness_target(bool(user_prefs["likes_acoustic"]))
    return targets


def score_numeric_features(
    user_prefs: Dict, song: Dict, width: float = DEFAULT_WIDTH
) -> Tuple[float, List[str]]:
    """
    Weighted proximity score over the numeric features, between 0 and 1.
    Features without a user target are skipped, and the result is divided by the
    total weight of the features that were scored.
    Returns (score, reasons) with one reason string per scored feature.
    """
    targets = numeric_targets(user_prefs)
    weighted_sum = 0.0
    active_weight = 0.0
    reasons: List[str] = []

    for feature, weight in NUMERIC_WEIGHTS.items():
        target = targets.get(feature)
        if target is None or feature not in song:
            continue
        value = float(song[feature])
        closeness = proximity_score(value, target, width)
        weighted_sum += closeness * weight
        active_weight += weight
        reasons.append(
            f"{feature}: song {value:.2f} vs target {target:.2f} "
            f"-> closeness {closeness:.2f} x weight {weight:.2f}"
        )

    if active_weight == 0:
        return 0.0, []
    return weighted_sum / active_weight, reasons


def user_to_prefs(user: UserProfile) -> Dict:
    """Converts a UserProfile into the preferences dict used by the scoring functions."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "valence": user.target_valence,
        "likes_acoustic": user.likes_acoustic,
    }


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        prefs = user_to_prefs(user)
        scored = [(song, score_song(prefs, asdict(song))[0]) for song in self.songs]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = score_song(user_to_prefs(user), asdict(song))
        return "; ".join(reasons) if reasons else "No preferences available to score this song."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into dicts with numeric fields converted.
    Required by src/main.py
    """
    int_fields = ("id",)
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    Returns (score, reasons).
    """
    # Only numeric features are scored so far. Mood and genre matching will be
    # added here and combined with the numeric score using their weights.
    return score_numeric_features(user_prefs, song)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    Returns the top k as (song_dict, score, explanation), best first.
    Songs with equal scores keep their original catalog order.
    """
    results = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        results.append((song, score, "; ".join(reasons)))
    results.sort(key=lambda item: item[1], reverse=True)
    return results[:k]
