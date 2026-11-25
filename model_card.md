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

**The short version:** The system compares every song in the catalog to a listener's taste, gives each song a score from 0 to 1, and shows the five highest-scoring songs.

**What it looks at.** Each song has a genre, a mood, and three numbers: energy, valence (how happy or positive a song sounds), and acousticness (how much it sounds acoustic rather than electronic). The listener describes their taste with a favorite genre, a favorite mood, a target energy level, an optional target valence, and a yes or no answer to whether they like acoustic music. The system also stores tempo and danceability for each song, but it does not use them when scoring yet.

**How a score is built.** The system checks each feature one at a time and gives it points:

- **Numbers get points for being close.** If a song's energy is exactly the listener's target, it earns full points. The farther away it is, the fewer points it earns, and a gap of half the scale or more earns nothing. Energy counts the most, then valence, then acousticness.
- **Labels get points for matching.** A song earns full points for mood if its mood is the listener's mood, and full points for genre if its genre is the listener's genre. Otherwise it earns nothing. Mood counts a little more than genre.
- **The total is averaged by importance.** Every feature has a weight. The points are added up and divided by the total weight of the features the listener actually gave. This keeps the score on the same 0 to 1 scale even when a listener only fills in a few preferences.

If a listener does not give a preference, that feature is skipped. It does not count as a miss.

**Ranking and explanations.** The system sorts all songs from highest score to lowest. Songs with the same score stay in the order they appear in the catalog. Along with each song, the system lists how each feature contributed, so a listener can see why a song ranked where it did.

**Why these weights.** Energy has the most weight because it is the clearest signal of how a song feels to listen to. Mood comes next, and genre comes after it. Taken together, mood and genre carry more weight than energy (0.45 against 0.35), so a song that matches the listener's mood and genre can rank above a song with a slightly closer energy level.

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

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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
