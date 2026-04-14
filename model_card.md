# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**  

---

## 2. Intended Use  

The recommender predicts which songs a user might like. It suggests top songs from a small list. It assumes users have clear preferences for genre and energy. It is for classroom exploration only. Do not use it for real music apps.  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

The model scores songs by matching genre, energy, tempo, valence, and acousticness to user preferences. It gives points for exact genre matches and closeness in other features. Songs with higher scores are recommended first. I removed mood matching to test changes.

---

## 4. Data  

Describe the dataset the model uses.  

The dataset has 15 songs. It includes genres like pop, lofi, rock, jazz, and others. Features are genre, mood, energy, tempo, valence, danceability, acousticness. I did not add or remove data. It misses lyrics and user listening history. The data is small and may not cover all tastes.

## 5. Strengths  

The system works well for users with clear genre preferences. It captures energy and tempo patterns correctly. Recommendations often match intuition for common profiles.  

---

## 6. Limitations and Bias 

The system ignores lyrics and user history. Some genres like classical are rare. It overfits to genre over energy. It may favor high-energy songs unfairly.  

- The current scoring logic creates a bias toward genre matches and broad energy/tempo similarity rather than truly capturing niche preferences. Because energy_score is calculated as 1 - abs(target - energy) on a 0–1 scale, almost every song still gets a positive energy contribution, so extreme or unusual energy tastes are not sharply separated. In other words, if a user wants very low energy, a mid-energy song still receives a nonzero score and can compete with better matches, which favors songs that are “close enough” rather than a real preference fit. This can produce a filter bubble where users with nonstandard mood or acoustic preferences are ignored in favor of songs that simply share genre and average energy/tempo.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

I tested several user profiles including HIGH_ENERGY_POP (favoring pop genre, happy mood, high energy 0.9, tempo 130, valence 0.9, no acoustic preference), CHILL_LOFI (favoring lofi genre, chill mood, low energy 0.3, tempo 80, valence 0.6, likes acoustic), and DEEP_INTENSE_ROCK (favoring rock genre, intense mood, high energy 0.95, tempo 150, valence 0.3, no acoustic preference). I looked for whether the top recommendations aligned with the user's preferences in genre, energy levels, tempo, valence, and acousticness, checking if the rankings made intuitive sense based on the scoring logic. What surprised me was that even after temporarily removing the mood feature from the scoring, the system still heavily favored genre matches (weighted at 2.0 points), which overshadowed other preferences like low energy or acoustic liking, leading to less diverse recommendations for niche users and highlighting how the linear similarity functions allow "close enough" matches to dominate over exact fits.

---

## 8. Future Work  

Add lyrics and user history features. Explain recommendations better with reasons. Improve diversity by balancing genres. Handle mixed tastes like acoustic rock.  

---

## 9. Personal Reflection  

I learned recommenders use simple rules to predict likes. I was surprised by how genre dominates. This makes me think real apps need more balance. Human judgment still matters for unique tastes.  
