#!/usr/bin/env python3
"""
Interactive testing mode for Temporal Semantic Weaving
Add your own experiences and ask questions in real-time
"""

from main import EnhancedTSW
import numpy as np

def main():
    """Interactive mode to test custom data"""
    
    print("\n" + "=" * 70)
    print("🌀 TEMPORAL SEMANTIC WEAVING - INTERACTIVE MODE")
    print("=" * 70)
    print("\nAdd your experiences and ask questions about them!")
    print("\nCommands:")
    print("  add <text>     - Add an experience")
    print("  ask <question> - Ask a question about your experiences")
    print("  stats          - Show system statistics")
    print("  clear          - Reset system")
    print("  help           - Show this help")
    print("  exit           - Exit program")
    
    tsw = EnhancedTSW()
    exp_count = 0
    
    while True:
        user_input = input("\n> ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'exit':
            print("\n👋 Goodbye!\n")
            break
        
        elif user_input.lower() == 'help':
            print("\nCommands:")
            print("  add <text>     - Add an experience")
            print("  ask <question> - Ask a question")
            print("  stats          - Show statistics")
            print("  clear          - Reset system")
            print("  exit           - Exit")
        
        elif user_input.lower() == 'stats':
            if exp_count == 0:
                print("❌ No experiences added yet!")
                continue
            print("\n" + "-" * 70)
            print("📊 SYSTEM STATISTICS")
            print("-" * 70)
            print(f"Total experiences added: {exp_count}")
            print(f"Active waves in field: {len(tsw.field.waves)}")
            print(f"Field energy level: {tsw.field.get_field_energy():.4f}")
            print(f"Crystals formed: {len(tsw.crystallizer.crystals)}")
            entangled = sum(len(w.entangled_with) for w in tsw.field.waves)
            print(f"Quantum entanglements: {entangled}")
            if tsw.field.waves:
                print(f"Avg wave amplitude: {np.mean([w.amplitude for w in tsw.field.waves]):.4f}")
        
        elif user_input.lower() == 'clear':
            tsw = EnhancedTSW()
            exp_count = 0
            print("✓ System reset!")
        
        elif user_input.lower().startswith('add '):
            exp = user_input[4:].strip()
            if exp:
                tsw.add_experience(exp)
                exp_count += 1
                print(f"✓ Added experience #{exp_count}")
            else:
                print("❌ Please provide text after 'add'")
        
        elif user_input.lower().startswith('ask '):
            if exp_count == 0:
                print("❌ Add some experiences first!")
                continue
            query = user_input[4:].strip()
            if query:
                print(f"\n🔍 Analyzing: '{query}'")
                result = tsw.query(query)
                print("\n" + "-" * 70)
                print(f"💡 Insight: {result['insight']}")
                print(f"📈 Confidence: {result['confidence']:.0%}")
                if result.get('evidence') and len(result['evidence']) > 0:
                    print(f"📌 Evidence:")
                    for i, ev in enumerate(result['evidence'][:3], 1):
                        print(f"   {i}. {ev[:70]}")
                print("-" * 70)
            else:
                print("❌ Please provide a question after 'ask'")
        
        else:
            print("❌ Unknown command. Type 'help' for commands.")

if __name__ == "__main__":
    main()
