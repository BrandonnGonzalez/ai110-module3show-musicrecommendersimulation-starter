import pytest

from src.recommender import (
    categorical_match,
    score_categorical_features,
    score_song,
    Song,
    UserProfile,
    Recommender,
    proximity_score,
    acousticness_target,
    numeric_targets,
    score_numeric_features,
    load_songs,
    recommend_songs,
)


# --- proximity_score -------------------------------------------------------

def test_exact_match_scores_one():
    assert proximity_score(0.4, 0.4) == 1.0


def test_score_is_symmetric_above_and_below_target():
    assert proximity_score(0.7, 0.4) == pytest.approx(proximity_score(0.1, 0.4))


def test_score_never_increases_as_distance_grows():
    scores = [proximity_score(0.4 + d / 20, 0.4) for d in range(0, 12)]
    assert all(a >= b for a, b in zip(scores, scores[1:]))


def test_distance_at_or_beyond_width_scores_zero():
    assert proximity_score(0.9, 0.4, width=0.5) == 0.0
    assert proximity_score(0.93, 0.4, width=0.5) == 0.0


def test_known_values_with_default_width():
    # Sunrise City energy 0.82 vs target 0.40 -> 1 - 0.42 / 0.5 = 0.16
    assert proximity_score(0.82, 0.40) == pytest.approx(0.16)
    # Library Rain energy 0.35 vs target 0.40 -> 1 - 0.05 / 0.5 = 0.90
    assert proximity_score(0.35, 0.40) == pytest.approx(0.90)


def test_width_one_is_plain_one_minus_distance():
    assert proximity_score(0.82, 0.40, width=1.0) == pytest.approx(0.58)


def test_invalid_width_raises():
    with pytest.raises(ValueError):
        proximity_score(0.5, 0.5, width=0)


# --- targets ---------------------------------------------------------------

def test_acousticness_target_mapping():
    assert acousticness_target(True) == 0.80
    assert acousticness_target(False) == 0.20


def test_user_profile_works_with_and_without_valence():
    old_style = UserProfile("pop", "happy", 0.8, False)
    new_style = UserProfile("pop", "happy", 0.8, False, target_valence=0.7)
    assert old_style.target_valence is None
    assert new_style.target_valence == 0.7


def test_numeric_targets_skips_unspecified_features():
    assert numeric_targets({"energy": 0.4}) == {"energy": 0.4}
    assert numeric_targets({"energy": 0.4, "valence": 0.6, "likes_acoustic": True}) == {
        "energy": 0.4,
        "valence": 0.6,
        "acousticness": 0.80,
    }


# --- score_numeric_features ------------------------------------------------

PERFECT_SONG = {"energy": 0.4, "valence": 0.6, "acousticness": 0.8}


def test_perfect_match_on_all_numeric_features_scores_one():
    prefs = {"energy": 0.4, "valence": 0.6, "likes_acoustic": True}
    score, reasons = score_numeric_features(prefs, PERFECT_SONG)
    assert score == pytest.approx(1.0)
    assert len(reasons) == 3


def test_missing_target_is_skipped_without_error():
    score, reasons = score_numeric_features({"energy": 0.4}, PERFECT_SONG)
    assert score == pytest.approx(1.0)
    assert len(reasons) == 1
    assert reasons[0].startswith("energy")


def test_no_targets_returns_zero_and_no_reasons():
    assert score_numeric_features({}, PERFECT_SONG) == (0.0, [])


def test_weighted_score_matches_hand_calculation():
    # energy: 0.82 vs 0.40 -> 0.16 (weight 0.35); valence: 0.84 vs 0.84 -> 1.0 (weight 0.15)
    song = {"energy": 0.82, "valence": 0.84}
    score, _ = score_numeric_features({"energy": 0.40, "valence": 0.84}, song)
    assert score == pytest.approx((0.16 * 0.35 + 1.0 * 0.15) / 0.50)


# --- load_songs and ranking ------------------------------------------------

def test_load_songs_returns_fifteen_songs_with_numeric_fields():
    songs = load_songs("data/songs.csv")
    assert len(songs) == 15
    first = songs[0]
    assert first["title"] == "Sunrise City"
    assert isinstance(first["id"], int)
    for field in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
        assert isinstance(first[field], float)


def test_low_energy_target_ranks_closest_energy_first():
    songs = load_songs("data/songs.csv")
    results = recommend_songs({"energy": 0.40}, songs, k=3)
    assert [song["title"] for song, _, _ in results] == [
        "Focus Flow",           # energy 0.40, distance 0.00
        "Midnight Coding",      # energy 0.42, distance 0.02
        "Coffee Shop Stories",  # energy 0.37, distance 0.03
    ]
    scores = [score for _, score, _ in results]
    assert scores == sorted(scores, reverse=True)
    assert all(explanation for _, _, explanation in results)


def test_recommender_class_uses_numeric_scoring():
    songs = [
        Song(1, "Loud", "A", "rock", "intense", 0.9, 150, 0.5, 0.7, 0.1),
        Song(2, "Quiet", "B", "lofi", "chill", 0.4, 80, 0.5, 0.5, 0.9),
    ]
    user = UserProfile("lofi", "chill", target_energy=0.4, likes_acoustic=True)
    assert Recommender(songs).recommend(user, k=2)[0].title == "Quiet"


# --- mood and genre --------------------------------------------------------

def test_categorical_match_ignores_case_and_spaces():
    assert categorical_match("Lofi ", "lofi") == 1.0
    assert categorical_match("rock", "pop") == 0.0


def test_mood_outweighs_genre():
    song = {"mood": "intense", "genre": "rock"}
    mood_only, _ = score_categorical_features({"mood": "intense", "genre": "pop"}, song)
    genre_only, _ = score_categorical_features({"mood": "chill", "genre": "rock"}, song)
    assert mood_only == pytest.approx(0.25 / 0.45)
    assert genre_only == pytest.approx(0.20 / 0.45)
    assert mood_only > genre_only


def test_missing_categorical_target_is_skipped():
    score, reasons = score_categorical_features({"mood": "chill"}, {"mood": "chill", "genre": "lofi"})
    assert score == 1.0
    assert len(reasons) == 1


def test_mood_and_genre_match_can_beat_closer_energy():
    prefs = {"energy": 0.9, "mood": "chill", "genre": "lofi"}
    matching = {"energy": 0.6, "mood": "chill", "genre": "lofi"}
    closer_energy = {"energy": 0.9, "mood": "intense", "genre": "rock"}
    assert score_song(prefs, matching)[0] > score_song(prefs, closer_energy)[0]


def test_combined_score_matches_hand_calculation():
    # energy 1.0 x 0.35, mood match x 0.25, genre miss x 0.20 -> 0.60 / 0.80
    prefs = {"energy": 0.5, "mood": "chill", "genre": "pop"}
    song = {"energy": 0.5, "mood": "chill", "genre": "lofi"}
    assert score_song(prefs, song)[0] == pytest.approx(0.60 / 0.80)
