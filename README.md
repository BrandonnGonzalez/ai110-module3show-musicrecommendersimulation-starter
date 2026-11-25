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

Real streaming services such as Spotify and YouTube recommend songs by combining two kinds of signals. Collaborative filtering looks at what similar listeners played, and content-based filtering looks at how songs sound and how they are labeled. This version uses only content-based filtering. It compares each song's attributes to a user's stated taste, and it gives the most weight to energy, then mood, genre, valence (how positive a song sounds), and acousticness. Each numeric feature is scored by how close the song is to the user's target, not by whether the value is high or low. Songs are ranked by their total score, and the top results are returned with an explanation.

**Features used by `Song`:** `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`. Only `energy`, `valence`, and `acousticness` are scored so far, and `genre` and `mood` are scored once categorical matching is added. `tempo_bpm` and `danceability` are loaded but not yet scored.

**Information stored by `UserProfile`:** `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`, and the optional `target_valence`. `likes_acoustic` is converted to an acousticness target of 0.80 when true and 0.20 when false.

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
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
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



