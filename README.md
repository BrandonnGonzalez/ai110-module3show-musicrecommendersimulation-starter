# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real streaming services such as Spotify and YouTube recommend songs by combining two kinds of signals. Collaborative filtering looks at what similar listeners played, and content-based filtering looks at how songs sound and how they are labeled. This version uses only content-based filtering. It compares each song's attributes to a user's stated taste, then ranks the catalog by a weighted total score and returns the top results with an explanation.

### Plan

The goal was a second route to a high score besides energy. Energy stays the largest single signal, but a song that matches the user's mood and genre should be able to outrank a song with slightly closer energy. Mood ranks second and genre third, because mood describes how a song feels while genre is a coarser label.

### Algorithmic Recipe

1. **Load the catalog.** Read `data/songs.csv` and convert `id`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness` to numbers.
2. **Build numeric targets.** Use `energy`, `valence`, and `likes_acoustic` from the user profile. If `likes_acoustic` is set, it becomes an acousticness target of 0.80 when true and 0.20 when false. Any target the user leaves out is skipped.
3. **Score each numeric feature by proximity.** For each feature, `closeness = max(0, 1 - |song value - target| / 0.5)`. A match earns 1.0, and a gap of 0.5 or more earns 0.0. Weights: energy 0.35, valence 0.15, acousticness 0.05.
4. **Score each categorical feature by exact match.** Mood and genre earn 1.0 when the song's label equals the profile's label, ignoring case and surrounding spaces. Otherwise they earn 0.0. Weights: mood 0.25, genre 0.20.
5. **Combine into one score.** `score = (sum of weight × feature score) / (sum of weights for the features the profile specifies)`. The score stays between 0 and 1, and features the profile leaves out do not lower it.
6. **Rank and return.** Sort all songs by score, highest first. Songs with equal scores keep their CSV order. Return the top k (default 5), each with its score and a "Because:" list of per-feature reasons.

`tempo_bpm` and `danceability` are loaded but not scored. The starter profile in `src/main.py` also sets `acousticness` directly, but the scorer reads `likes_acoustic` instead, so that target is not used yet.

**Features used by `Song`:** `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`. Scored: `energy`, `valence`, `acousticness`, `mood`, and `genre`. Loaded but not scored: `tempo_bpm` and `danceability`.

**Information stored by `UserProfile`:** `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`, and the optional `target_valence`. `likes_acoustic` is converted to an acousticness target of 0.80 when true and 0.20 when false.

### Expected Biases

- **Exact-label matching is strict.** "rock" earns nothing for a "trap" profile, even though the two genres are close. Songs labeled with a neighboring genre are penalized in the same way as unrelated ones.
- **Mood and genre can outweigh sound.** Together they carry 0.45 of the weight, so a song that matches both labels can outrank a song whose energy and valence are much closer to the target. The system may favor labels over how a song actually sounds.
- **Energy is still the main driver.** Its 0.5 tolerance means a song 0.4 away on energy still earns 0.2 for that feature. Loud or quiet songs may win on energy alone when the other signals are weak.
- **One target point cannot describe mixed taste.** A listener who enjoys both intense rock and chill lofi gets a single profile, so the system favors one side and rarely recommends the other.
- **Unscored features are ignored.** Songs that differ only in `tempo_bpm` or `danceability` score the same.
- **Small catalog.** With 15 songs, some genres and moods have only one entry. Users with those tastes see few real options, and the numeric values for the newer songs are estimates, not measured audio data.
- **Scores are not comparable across profiles.** The total is divided by the weights of the features each profile specifies, so a profile with fewer targets can produce scores on a different scale.
- **Binary acousticness.** `likes_acoustic` maps to a single target, so it cannot express a preference for a moderate amount of acoustic sound.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python src/main.py
```

### Running Tests

Run the starter tests with:

```bash
python -m pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output from `python src/main.py` for the starter profile (genre=trap, mood=intense, energy=0.85, valence=0.50, likes_acoustic not set):

```
Top recommendations:

Storm Runner - Score: 0.74
Because: energy: song 0.91 vs target 0.85 -> closeness 0.88 x weight 0.35; valence: song 0.48 vs target 0.50 -> closeness 0.96 x weight 0.15; mood: song 'intense' vs target 'intense' -> match x weight 0.25; genre: song 'rock' vs target 'trap' -> no match x weight 0.20

Lord Of Chaos - Score: 0.68
Because: energy: song 0.93 vs target 0.85 -> closeness 0.84 x weight 0.35; valence: song 0.35 vs target 0.50 -> closeness 0.70 x weight 0.15; mood: song 'intense' vs target 'intense' -> match x weight 0.25; genre: song 'rage' vs target 'trap' -> no match x weight 0.20

Bada Bing, Bada Bøøm - Score: 0.67
Because: energy: song 0.85 vs target 0.85 -> closeness 1.00 x weight 0.35; valence: song 0.72 vs target 0.50 -> closeness 0.56 x weight 0.15; mood: song 'happy' vs target 'intense' -> no match x weight 0.25; genre: song 'trap' vs target 'trap' -> match x weight 0.20

All Stars - Score: 0.65
Because: energy: song 0.78 vs target 0.85 -> closeness 0.86 x weight 0.35; valence: song 0.62 vs target 0.50 -> closeness 0.76 x weight 0.15; mood: song 'confident' vs target 'intense' -> no match x weight 0.25; genre: song 'trap' vs target 'trap' -> match x weight 0.20

Gym Hero - Score: 0.65
Because: energy: song 0.93 vs target 0.85 -> closeness 0.84 x weight 0.35; valence: song 0.77 vs target 0.50 -> closeness 0.46 x weight 0.15; mood: song 'intense' vs target 'intense' -> match x weight 0.25; genre: song 'pop' vs target 'trap' -> no match x weight 0.20
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



