"""
Enhanced TSW Demo
"""

import numpy as np
from main import EnhancedTSW
import time

def run_enhanced_demo():
    """Run comprehensive demo of enhanced features"""
    
    print("=" * 60)
    print("ENHANCED TEMPORAL SEMANTIC WEAVING DEMONSTRATION")
    print("=" * 60)
    
    # Initialize enhanced system
    tsw = EnhancedTSW()
    
    # Test experiences
    experiences = [
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
    
    # Load experiences
    print("\n📚 Loading experiences with enhanced processing...")
    for exp in experiences:
        tsw.add_experience(exp)
        time.sleep(0.1)
    
    # Run queries
    print("\n" + "=" * 60)
    print("QUANTUM-ENHANCED QUERIES")
    print("=" * 60)
    
    queries = [
        "Why do I keep meeting Sarah?",
        "What connects guitar and coffee?",
        "What patterns exist in my life?",
        "How does Tom influence my thinking?",
        "What emerges from coffee meetings?"
    ]
    
    for query in queries:
        result = tsw.query(query)
        print(f"\n💡 Insight: {result['insight']}")
        print(f"📈 Confidence: {result['confidence']:.2%}")
        time.sleep(0.5)
    
    # Visualizations
    print("\n" + "=" * 60)
    print("VISUALIZATIONS")
    print("=" * 60)
    
    print("\n📊 Generating comprehensive field visualization...")
    tsw.visualize_field()
    
    print("\n🌐 Generating resonance network...")
    tsw.visualize_resonance_network()
    
    print("\n🔮 Demonstrating holographic recovery...")
    tsw.demonstrate_holographic_recovery()
    
    # Show temporal connections
    print("\n" + "=" * 60)
    print("TEMPORAL CONNECTIONS")
    print("=" * 60)
    
    if tsw.temporal_braid.causal_loops:
        print(f"\n🔄 Causal loops detected: {len(tsw.temporal_braid.causal_loops)}")
        for loop in tsw.temporal_braid.causal_loops[:3]:
            print(f"   Loop: {' -> '.join(loop[:4])}...")
    
    # Show quantum entanglements
    entangled_count = sum(len(w.entangled_with) for w in tsw.field.waves)
    print(f"\n🔗 Quantum entanglements: {entangled_count}")
    
    # Field statistics
    print("\n" + "=" * 60)
    print("FIELD STATISTICS")
    print("=" * 60)
    
    print(f"Active waves: {len(tsw.field.waves)}")
    print(f"Field energy: {tsw.field.get_field_energy():.2f}")
    print(f"Crystals formed: {len(tsw.crystallizer.crystals)}")
    print(f"Average amplitude: {np.mean([w.amplitude for w in tsw.field.waves]):.3f}")
    
    print("\n✨ Enhanced demo complete!")
    
    return tsw

if __name__ == "__main__":
    tsw = run_enhanced_demo()
    
    # Optional interactive mode
    print("\n" + "=" * 60)
    response = input("Enter interactive mode? (y/n): ")
    if response.lower() == 'y':
        print("\nEntering interactive mode...")
        print("Commands: 'add: <text>', '? <question>', 'viz', 'quit'")
        
        while True:
            user_input = input("\n> ").strip()
            
            if user_input == 'quit':
                break
            elif user_input == 'viz':
                tsw.visualize_field()
            elif user_input.startswith('add:'):
                text = user_input[4:].strip()
                tsw.add_experience(text)
            elif user_input.startswith('?'):
                query = user_input[1:].strip()
                result = tsw.query(query)
                print(f"💡 {result['insight']}")