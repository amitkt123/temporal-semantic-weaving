"""
Test scenarios for Temporal Semantic Weaving system
Try different datasets and see how the system detects patterns
"""

import numpy as np
from main import EnhancedTSW
import time

# Dataset 1: Original (Personal Life Pattern)
PERSONAL_LIFE = [
    "Met Sarah for coffee, she got promoted and seems stressed about managing",
    "Practiced guitar today, fingers hurt from bar chords",
    "Tom mentioned his promotion last month at lunch",
    "Coffee always helps me think through problems",
    "Sarah plays guitar too, we should jam",
    "Feeling stuck with my career lately",
    "Morning coffee ritual is sacred",
    "Sarah helped me with bar chords over coffee",
    "Tom's promotion made me think about my path",
    "Morning coffee is when I practice guitar",
    "Had energizing coffee with Sarah today",
    "Guitar practice reminds me of learning to code",
    "Sarah and I discussed career transitions over coffee"
]

# Dataset 2: Technology Stack Learning
TECH_LEARNING = [
    "Started learning Python for data science",
    "Python is great for quick prototyping",
    "Implemented neural network in PyTorch",
    "PyTorch makes deep learning intuitive",
    "Read about machine learning best practices",
    "Machine learning requires lots of data",
    "Python libraries are well documented",
    "Deep learning with PyTorch is powerful",
    "Data preprocessing takes most of the time",
    "Machine learning models need validation",
    "PyTorch community is very helpful",
    "Python and machine learning go hand in hand",
    "Understanding data is crucial for ML success"
]

# Dataset 3: Travel & Adventure
TRAVEL_ADVENTURE = [
    "Visited Tokyo last summer",
    "Tokyo has amazing food and culture",
    "Hiked Mount Fuji, exhausting but rewarding",
    "Mountain hiking teaches you about perseverance",
    "Met locals in Tokyo who were very friendly",
    "Friendly people make travel memorable",
    "Hiked to Fuji summit at sunrise",
    "Sunrises from mountains are breathtaking",
    "Tokyo nightlife was incredible",
    "Breathtaking views reward the hiker",
    "Made new friends hiking Mount Fuji",
    "Friends enhance travel experiences",
    "Traveling with friends amplifies the joy"
]

# Dataset 4: Health & Fitness
HEALTH_FITNESS = [
    "Started gym routine Monday mornings",
    "Gym provides physical and mental benefits",
    "Running 5K feels incredible",
    "Running burns calories and improves health",
    "Yoga helps with flexibility and peace",
    "Morning workouts boost energy for the day",
    "Stretching after gym prevents injury",
    "Injury prevention leads to consistent training",
    "Consistent training shows results",
    "Results motivate continued effort",
    "Gym friends keep you accountable",
    "Accountability is crucial for fitness goals",
    "Mental peace comes from regular exercise"
]

# Dataset 5: Academic Research
ACADEMIC_RESEARCH = [
    "Reading papers on quantum computing",
    "Quantum computing could revolutionize cryptography",
    "Submitted thesis on algorithm optimization",
    "Algorithm optimization improves performance",
    "Professor gave feedback on research proposal",
    "Research requires rigorous peer review",
    "Quantum algorithms are mathematically complex",
    "Complex mathematics needs clear explanation",
    "Peer review strengthens research quality",
    "Quality research takes significant time",
    "Conference presentations showcase findings",
    "Findings contribute to scientific knowledge",
    "Knowledge sharing accelerates innovation"
]

# Dataset 6: Cooking & Recipes
COOKING_RECIPES = [
    "Tried making pasta from scratch",
    "Homemade pasta tastes better than store-bought",
    "Added fresh basil to the tomato sauce",
    "Fresh herbs enhance every dish",
    "Served dinner to friends and family",
    "Family meals create lasting memories",
    "Olive oil is essential in Italian cooking",
    "Essential ingredients make simple dishes shine",
    "Cooking relaxes me after work",
    "Relaxation improves creativity in kitchen",
    "Shared recipes with my cooking club",
    "Club members always appreciate new recipes",
    "Appreciation motivates me to cook more"
]

def run_test_scenario(name, experiences, queries=None):
    """Run a test scenario with given experiences and queries"""
    
    print("\n" + "=" * 70)
    print(f"SCENARIO: {name}")
    print("=" * 70)
    
    # Initialize system
    tsw = EnhancedTSW()
    
    # Load experiences
    print(f"\n📚 Loading {len(experiences)} experiences...")
    for i, exp in enumerate(experiences, 1):
        print(f"  {i:2d}. {exp[:60]}...")
        tsw.add_experience(exp)
        time.sleep(0.05)  # Shorter delay
    
    # Stats
    print("\n" + "-" * 70)
    print("📊 SYSTEM STATISTICS")
    print("-" * 70)
    print(f"Active waves: {len(tsw.field.waves)}")
    print(f"Field energy: {tsw.field.get_field_energy():.4f}")
    print(f"Crystals formed: {len(tsw.crystallizer.crystals)}")
    if tsw.field.waves:
        print(f"Average amplitude: {np.mean([w.amplitude for w in tsw.field.waves]):.4f}")
    entangled_count = sum(len(w.entangled_with) for w in tsw.field.waves)
    print(f"Quantum entanglements: {entangled_count}")
    
    # Custom queries if provided, otherwise auto-generate
    if queries is None:
        print("\n(Auto-generated queries)")
        queries = [
            f"What is the main topic?",
            f"What patterns emerge?",
            f"How are concepts connected?"
        ]
    
    # Run queries
    print("\n" + "-" * 70)
    print("❓ QUERIES & INSIGHTS")
    print("-" * 70)
    
    for query in queries:
        print(f"\nQ: {query}")
        result = tsw.query(query)
        print(f"   💡 {result['insight']}")
        print(f"   📈 Confidence: {result['confidence']:.0%}")
        if result.get('evidence'):
            print(f"   📌 Evidence: {result['evidence'][:2]}")
    
    return tsw

def run_all_scenarios():
    """Run all test scenarios"""
    
    scenarios = [
        ("Personal Life Patterns", PERSONAL_LIFE, [
            "Why do I keep meeting Sarah?",
            "What connects guitar and coffee?",
            "How does Tom influence my thinking?"
        ]),
        ("Technology Learning", TECH_LEARNING, [
            "What programming language am I learning?",
            "How does machine learning relate to Python?",
            "What is important for ML success?"
        ]),
        ("Travel & Adventure", TRAVEL_ADVENTURE, [
            "What mountain did I climb?",
            "How do friends enhance travel?",
            "What makes experiences memorable?"
        ]),
        ("Health & Fitness", HEALTH_FITNESS, [
            "What are my fitness activities?",
            "Why is consistency important?",
            "How does exercise improve life?"
        ]),
        ("Academic Research", ACADEMIC_RESEARCH, [
            "What is my research about?",
            "Why is peer review important?",
            "How do findings contribute?"
        ]),
        ("Cooking & Recipes", COOKING_RECIPES, [
            "What cooking style do I prefer?",
            "How do ingredients matter?",
            "Why do I enjoy cooking?"
        ])
    ]
    
    results = {}
    for name, experiences, queries in scenarios:
        tsw = run_test_scenario(name, experiences, queries)
        results[name] = tsw
    
    return results

def interactive_test():
    """Interactive mode to test custom data"""
    
    print("\n" + "=" * 70)
    print("INTERACTIVE TEST MODE")
    print("=" * 70)
    print("\nEnter your own experiences for testing.")
    print("Commands:")
    print("  'done' - Finish adding experiences and run queries")
    print("  'query' - Ask a question")
    print("  'stats' - Show system statistics")
    print("  'quit' - Exit")
    
    tsw = EnhancedTSW()
    experiences_count = 0
    
    while True:
        user_input = input("\n> ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'done':
            if experiences_count == 0:
                print("Add some experiences first!")
                continue
            print("\n" + "-" * 70)
            print("📊 SYSTEM STATISTICS")
            print("-" * 70)
            print(f"Total experiences: {experiences_count}")
            print(f"Active waves: {len(tsw.field.waves)}")
            print(f"Field energy: {tsw.field.get_field_energy():.4f}")
            print(f"Crystals: {len(tsw.crystallizer.crystals)}")
            entangled = sum(len(w.entangled_with) for w in tsw.field.waves)
            print(f"Entanglements: {entangled}")
            
        elif user_input.lower() == 'stats':
            if experiences_count == 0:
                print("No experiences added yet!")
                continue
            print(f"Experiences: {experiences_count}")
            print(f"Waves: {len(tsw.field.waves)}")
            print(f"Energy: {tsw.field.get_field_energy():.4f}")
            
        elif user_input.lower() == 'query':
            if experiences_count == 0:
                print("Add experiences first!")
                continue
            query = input("Enter your query: ").strip()
            if query:
                result = tsw.query(query)
                print(f"\n💡 {result['insight']}")
                print(f"📈 Confidence: {result['confidence']:.0%}")
                
        elif user_input:
            tsw.add_experience(user_input)
            experiences_count += 1
            print(f"✓ Added (Total: {experiences_count})")

if __name__ == "__main__":
    import sys
    
    print("\n" + "=" * 70)
    print("TEMPORAL SEMANTIC WEAVING - TEST SUITE")
    print("=" * 70)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'all':
            print("\nRunning ALL scenarios...")
            run_all_scenarios()
        elif sys.argv[1] == 'personal':
            run_test_scenario("Personal Life Patterns", PERSONAL_LIFE)
        elif sys.argv[1] == 'tech':
            run_test_scenario("Technology Learning", TECH_LEARNING)
        elif sys.argv[1] == 'travel':
            run_test_scenario("Travel & Adventure", TRAVEL_ADVENTURE)
        elif sys.argv[1] == 'health':
            run_test_scenario("Health & Fitness", HEALTH_FITNESS)
        elif sys.argv[1] == 'academic':
            run_test_scenario("Academic Research", ACADEMIC_RESEARCH)
        elif sys.argv[1] == 'cooking':
            run_test_scenario("Cooking & Recipes", COOKING_RECIPES)
        elif sys.argv[1] == 'interactive':
            interactive_test()
    else:
        print("\nUsage: python test_scenarios.py [option]")
        print("\nOptions:")
        print("  all          - Run all 6 test scenarios")
        print("  personal     - Test personal life patterns")
        print("  tech         - Test technology learning")
        print("  travel       - Test travel & adventure")
        print("  health       - Test health & fitness")
        print("  academic     - Test academic research")
        print("  cooking      - Test cooking & recipes")
        print("  interactive  - Interactive custom data mode")
        print("\nExample: python test_scenarios.py tech")
