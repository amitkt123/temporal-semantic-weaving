# Testing the Temporal Semantic Weaving System

Your system is fully functional and tested! Here are all the ways you can test it:

## Quick Start Options

### 1. **Run Pre-Built Test Scenarios**
```bash
# Test Technology Learning domain
python test_scenarios.py tech

# Test Personal Life Patterns
python test_scenarios.py personal

# Test Travel & Adventure
python test_scenarios.py travel

# Test Health & Fitness
python test_scenarios.py health

# Test Academic Research
python test_scenarios.py academic

# Test Cooking & Recipes
python test_scenarios.py cooking

# Run ALL scenarios
python test_scenarios.py all
```

### 2. **Use Interactive Mode**
```bash
# Launch interactive testing
python interactive_test.py

# Inside, use commands:
#   add <text>     - Add an experience
#   ask <question> - Ask a question
#   stats          - Show statistics
#   clear          - Reset system
#   exit           - Exit
```

### 3. **Run Testing Guide**
```bash
# Shows examples across multiple domains (Music, Sports, Work+Personal)
python TESTING_GUIDE.py
```

### 4. **Run Original Demo**
```bash
# The original demo that started it all
python demo.py
```

## What You Can Test

### Test Domains (Pre-Built)
- 🏢 **Technology Learning** - Python, PyTorch, ML concepts
- 👥 **Personal Life** - People (Sarah, Tom), activities (coffee, guitar), career
- ✈️ **Travel & Adventure** - Tokyo, Mount Fuji, hiking, friends
- 💪 **Health & Fitness** - Gym, running, yoga, training
- 📚 **Academic Research** - Quantum computing, algorithms, peer review
- 🍳 **Cooking & Recipes** - Homemade pasta, herbs, family meals

### Your Own Data
You can test with ANY domain by creating a Python script:

```python
from main import EnhancedTSW

# Create system
tsw = EnhancedTSW()

# Add experiences (any topic)
tsw.add_experience("Your experience here")
tsw.add_experience("Related experience")
tsw.add_experience("Another connection")

# Query the system
result = tsw.query("Your question here")
print(result['insight'])           # What it found
print(result['confidence'])        # How confident (0-1)
print(result['evidence'])          # Evidence experiences
```

## Key Features to Test

### 1. **Semantic Wave Creation**
- Experiences are encoded as 384-dimensional semantic vectors
- Watch for "📝 Adding:" messages showing vector creation
- Check field energy increases as more experiences added

### 2. **Quantum Entanglement Detection**
- Watch for "🔗 Quantum entanglement created" messages
- These show semantic connections between experiences
- More entanglements = stronger conceptual relationships

### 3. **Pattern Crystallization**
- Watch for "💎 Crystal formed" messages
- These show emerging patterns in your experiences
- Different domains create different crystal patterns

### 4. **Query Answering**
- Ask questions about any domain
- System finds resonating experiences
- Confidence scores show how certain it is
- Evidence shows supporting experiences

### 5. **Field Statistics**
```python
# Check field state
energy = tsw.field.get_field_energy()        # Overall energy
waves = len(tsw.field.waves)                 # Active experiences
entanglements = sum(len(w.entangled_with) 
                   for w in tsw.field.waves) # Connections
crystals = len(tsw.crystallizer.crystals)   # Patterns found
```

## Example Test Session

```bash
# 1. Start interactive mode
python interactive_test.py

# 2. Add some experiences
> add I started learning Python last week
> add Python is great for data analysis
> add I built my first machine learning model
> add Machine learning is fascinating
> add Data science combines statistics and programming

# 3. Check statistics
> stats

# 4. Ask questions
> ask What am I learning about?
> ask How does Python connect to ML?
> ask Why is data science interesting?

# 5. Exit
> exit
```

## What to Look For

### Good Indicators
- ✅ Quantum entanglements appearing (connections found)
- ✅ Crystals forming (patterns discovered)
- ✅ High confidence scores (75%+)
- ✅ Field energy increasing with more experiences
- ✅ Evidence showing relevant experiences

### System Behavior
- 🌊 More related experiences = more entanglements
- 🔮 Related concepts crystallize into patterns
- 💡 Queries find semantically similar experiences
- 📊 Confidence reflects how many connections exist

## Output Metrics Explained

```
Active waves: 10           # Number of experiences stored as waves
Field energy: 45.2        # Total energy in the field (0-100+ scale)
Crystals formed: 3        # Number of pattern clusters discovered
Quantum entanglements: 24 # Number of semantic connections found
Average amplitude: 0.35   # Strength of typical wave (0-1 scale)
Quantum collapse prob: 2.5% # Probability of wave function collapse
Confidence: 85%           # How sure query result is (0-100%)
```

## Test Domains You Can Create

The system works with ANY domain. Here are ideas:

- 📖 **Reading/Books** - Genres, authors, themes
- 🎵 **Music** - Instruments, genres, practice
- 🏃 **Fitness** - Activities, goals, progress
- 💼 **Work** - Projects, colleagues, skills
- 🌱 **Personal Growth** - Habits, changes, learning
- 👨‍👩‍👧 **Family** - Events, relationships, memories
- 🎨 **Creative** - Art, writing, expression
- ✈️ **Travel** - Places, experiences, people
- 🍽️ **Food** - Cooking, restaurants, preferences
- 🎓 **Learning** - Courses, skills, breakthroughs

## Files Reference

| File | Purpose |
|------|---------|
| `main.py` | Core EnhancedTSW system |
| `demo.py` | Original demonstration |
| `test_scenarios.py` | 6 pre-built test domains |
| `interactive_test.py` | Interactive custom testing |
| `TESTING_GUIDE.py` | Examples across domains |
| `CODEBASE_ANALYSIS.md` | System architecture docs |

## Next Steps

1. **Run a scenario** → `python test_scenarios.py tech`
2. **Try interactive** → `python interactive_test.py`
3. **See examples** → `python TESTING_GUIDE.py`
4. **Test your domain** → Create your own script using the code examples
5. **Analyze output** → Check how the system detects patterns in YOUR data

---

🚀 **The system is ready! Pick a test method above and explore how it works with different types of experiences.**
