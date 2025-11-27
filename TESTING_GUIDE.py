#!/usr/bin/env python3
"""
Quick Testing Guide - How to test TSW with your own data
"""

from main import EnhancedTSW
import numpy as np

print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║    TEMPORAL SEMANTIC WEAVING - QUICK START GUIDE                  ║
║                                                                    ║
║    This shows you how to test the system with any topic            ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
""")

# Example 1: Testing with a custom domain
print("\n" + "=" * 70)
print("EXAMPLE 1: Testing with Music/Instruments Domain")
print("=" * 70)

tsw = EnhancedTSW()

music_experiences = [
    "Started piano lessons last month",
    "Piano requires daily practice",
    "My teacher emphasizes hand position",
    "Hand position prevents injury",
    "I practice Bach pieces mostly",
    "Bach's compositions are mathematically precise",
    "Math in music helps me understand patterns",
    "Patterns repeat in classical music",
    "I perform at local recitals",
    "Recitals help build confidence"
]

print(f"\n📝 Adding {len(music_experiences)} music-related experiences...\n")
for i, exp in enumerate(music_experiences, 1):
    tsw.add_experience(exp)
    print(f"   ✓ {i:2}. {exp}")

# Show stats
print("\n" + "-" * 70)
energy = tsw.field.get_field_energy()
entanglements = sum(len(w.entangled_with) for w in tsw.field.waves)
print(f"📊 Results: {len(tsw.field.waves)} waves, {energy:.2f} energy, {entanglements} entanglements")

# Ask some questions
print("\n🔍 Testing queries:\n")
questions = [
    "What instrument do I play?",
    "Why is practice important?",
    "How does math connect to music?"
]

for q in questions:
    result = tsw.query(q)
    confidence = int(result['confidence'] * 100)
    print(f"Q: {q}")
    print(f"   ✓ Insight: {result['insight']}")
    print(f"   ✓ Confidence: {confidence}%\n")

# Example 2: Different domain - Sports
print("\n" + "=" * 70)
print("EXAMPLE 2: Testing with Sports/Football Domain")
print("=" * 70)

tsw2 = EnhancedTSW()

sports_experiences = [
    "Started playing soccer with a local team",
    "Soccer is great cardiovascular exercise",
    "Team dynamics are crucial for success",
    "Success requires consistent training",
    "I play midfield position",
    "Midfield controls game tempo",
    "Tempo management wins matches",
    "Matches taught me discipline",
    "Discipline improves all areas of life",
    "My teammates are like family"
]

print(f"\n📝 Adding {len(sports_experiences)} sports-related experiences...\n")
for i, exp in enumerate(sports_experiences, 1):
    tsw2.add_experience(exp)
    print(f"   ✓ {i:2}. {exp}")

print("\n" + "-" * 70)
energy2 = tsw2.field.get_field_energy()
entanglements2 = sum(len(w.entangled_with) for w in tsw2.field.waves)
print(f"📊 Results: {len(tsw2.field.waves)} waves, {energy2:.2f} energy, {entanglements2} entanglements")

print("\n🔍 Testing queries:\n")
questions2 = [
    "What sport do I play?",
    "Why do I play sports?",
    "How does teamwork matter?"
]

for q in questions2:
    result = tsw2.query(q)
    confidence = int(result['confidence'] * 100)
    print(f"Q: {q}")
    print(f"   ✓ Insight: {result['insight']}")
    print(f"   ✓ Confidence: {confidence}%\n")

# Example 3: Complex mixed domain
print("=" * 70)
print("EXAMPLE 3: Mixed Domain (Work + Personal)")
print("=" * 70)

tsw3 = EnhancedTSW()

mixed_experiences = [
    "Got promoted to project lead at work",
    "Leadership requires better communication",
    "Communication skills improve relationships",
    "I practice meditation in mornings",
    "Meditation reduces work stress",
    "Stress management is important",
    "My team is diverse and talented",
    "Diversity brings different perspectives",
    "Perspectives help solve problems",
    "Problem-solving is my strength"
]

print(f"\n📝 Adding {len(mixed_experiences)} mixed-domain experiences...\n")
for i, exp in enumerate(mixed_experiences, 1):
    tsw3.add_experience(exp)
    print(f"   ✓ {i:2}. {exp}")

print("\n" + "-" * 70)
energy3 = tsw3.field.get_field_energy()
entanglements3 = sum(len(w.entangled_with) for w in tsw3.field.waves)
print(f"📊 Results: {len(tsw3.field.waves)} waves, {energy3:.2f} energy, {entanglements3} entanglements")

print("\n🔍 Testing queries:\n")
questions3 = [
    "What is my new role?",
    "How do work and personal life connect?",
    "What are my strengths?"
]

for q in questions3:
    result = tsw3.query(q)
    confidence = int(result['confidence'] * 100)
    print(f"Q: {q}")
    print(f"   ✓ Insight: {result['insight']}")
    print(f"   ✓ Confidence: {confidence}%\n")

# Summary
print("\n" + "=" * 70)
print("📚 HOW TO USE WITH YOUR OWN DATA:")
print("=" * 70)
print("""
1. IMPORT THE SYSTEM:
   from main import EnhancedTSW
   tsw = EnhancedTSW()

2. ADD EXPERIENCES (any domain):
   tsw.add_experience("Your experience text here")
   tsw.add_experience("Another related experience")
   tsw.add_experience("And another...")

3. QUERY THE SYSTEM:
   result = tsw.query("Your question here")
   print(result['insight'])
   print(f"Confidence: {result['confidence']:.0%}")

4. SEE STATS:
   energy = tsw.field.get_field_energy()
   waves = len(tsw.field.waves)
   entanglements = sum(len(w.entangled_with) for w in tsw.field.waves)

EXAMPLE USE CASES:
- Journal analysis: Add diary entries, ask about patterns
- Learning tracking: Add study notes, find connections
- Life events: Add experiences, discover relationships
- Project notes: Track development, find insights
- Personal growth: Monitor reflections, identify growth areas
""")

print("\n" + "=" * 70)
print("🚀 Ready to test? Try these commands:")
print("=" * 70)
print("""
# Run test scenarios:
python test_scenarios.py tech      # Technology learning
python test_scenarios.py personal  # Personal life patterns
python test_scenarios.py travel    # Travel adventures
python test_scenarios.py cooking   # Cooking experiences

# Interactive mode:
python interactive_test.py

# Or create your own Python script using this guide!
""")
