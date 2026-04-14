# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

- The current scoring logic creates a bias toward genre matches and broad energy/tempo similarity rather than truly capturing niche preferences. Because energy_score is calculated as 1 - abs(target - energy) on a 0–1 scale, almost every song still gets a positive energy contribution, so extreme or unusual energy tastes are not sharply separated. In other words, if a user wants very low energy, a mid-energy song still receives a nonzero score and can compete with better matches, which favors songs that are “close enough” rather than a real preference fit. This can produce a filter bubble where users with nonstandard mood or acoustic preferences are ignored in favor of songs that simply share genre and average energy/tempo.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

I tested several user profiles including HIGH_ENERGY_POP (favoring pop genre, happy mood, high energy 0.9, tempo 130, valence 0.9, no acoustic preference), CHILL_LOFI (favoring lofi genre, chill mood, low energy 0.3, tempo 80, valence 0.6, likes acoustic), and DEEP_INTENSE_ROCK (favoring rock genre, intense mood, high energy 0.95, tempo 150, valence 0.3, no acoustic preference). I looked for whether the top recommendations aligned with the user's preferences in genre, energy levels, tempo, valence, and acousticness, checking if the rankings made intuitive sense based on the scoring logic. What surprised me was that even after temporarily removing the mood feature from the scoring, the system still heavily favored genre matches (weighted at 2.0 points), which overshadowed other preferences like low energy or acoustic liking, leading to less diverse recommendations for niche users and highlighting how the linear similarity functions allow "close enough" matches to dominate over exact fits.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
