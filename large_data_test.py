#!/usr/bin/env python3
"""
Project Chimera: Large Scale Stress Test
Simulates a corporate breakdown scenario to test Crystal formation and Quantum Entanglement.
"""

import time
import sys
import os

# Ensure we can import from current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main import EnhancedTSW
except ImportError:
    print("❌ Error: Could not import EnhancedTSW from main.py")
    print("   Make sure you are running this from the tsw_enhanced directory.")
    sys.exit(1)

def get_chimera_dataset():
    """
    Returns a chronologically ordered list of 50+ experiences.
    Themes: Corporate Espionage, Burnout, Technical Failure.
    """
    return [
        # --- JANUARY: THE BEGINNING ---
        "Jan 01: Project Chimera kickoff meeting. Morale is high.",
        "Jan 02: Alice appointed as Lead Engineer for Chimera.",
        "Jan 03: Bob joins as CFO. He seems nervous.",
        "Jan 05: Ordered 50 NVIDIA H100 GPUs for the training cluster.",
        "Jan 10: Alice loves drinking Matcha Tea in the morning.",
        "Jan 12: Dave joins the team as System Administrator.",
        
        # --- FEBRUARY: THE WORK ---
        "Feb 01: First prototype of the AI model is working.",
        "Feb 03: Dave is complaining about the server room cooling.",
        "Feb 14: Bob is having late night meetings with a competitor.",
        "Feb 15: Alice is working weekends. Feeling tired.",
        "Feb 20: The electric bill is unusually high this month.",
        "Feb 22: Dave forgot his keycard at home.",
        "Feb 25: Alice feels jittery and can't sleep.",
        
        # --- MARCH: THE CRACKS ---
        "Mar 01: Performance metrics are dropping.",
        "Mar 03: Found unauthorized encrypted traffic on port 8080.",
        "Mar 05: Bob bought a new Porsche. Everyone is surprised.",
        "Mar 08: Alice's Matcha tastes weird today.",
        "Mar 10: Server Room B overheated and shut down.",
        "Mar 12: Logs show Dave logged in at 3 AM remotely.",
        "Mar 15: The backup drive is missing.",
        
        # --- APRIL: THE BREAKDOWN ---
        "Apr 01: Investors are asking where the money went.",
        "Apr 02: Alice collapsed at her desk. Paramedics called.",
        "Apr 03: Hospital says Alice has severe exhaustion and dehydration.",
        "Apr 05: Bob resigned effectively immediately.",
        "Apr 06: Dave is nowhere to be found.",
        "Apr 07: Security camera footage from March 10 is deleted.",
        "Apr 10: Project Chimera is officially cancelled.",
        
        # --- MAY: THE AFTERMATH (Hindsight) ---
        "May 01: Audit reveals $1M missing from the hardware budget.",
        "May 02: Police found the backup drive in Bob's Porsche.",
        "May 05: Dave admits he was mining crypto on the servers.",
        "May 08: Alice is recovering in Hawaii.",
        "May 10: The 'competitor' Bob met was actually an FBI informant."
    ]

def main():
    print("\n" + "=" * 70)
    print("🏙️ PROJECT CHIMERA: LARGE SCALE STRESS TEST")
    print("=" * 70)
    
    # 1. Initialize
    print("\n[1] Initializing Enhanced TSW System...")
    tsw = EnhancedTSW()
    
    # 2. Ingest Data
    dataset = get_chimera_dataset()
    print(f"\n[2] Ingesting {len(dataset)} log entries...")
    print("    This effectively simulates 5 months of corporate history.")
    
    start_time = time.time()
    for i, log in enumerate(dataset, 1):
        tsw.add_experience(log)
        if i % 10 == 0:
            print(f"    Processed {i}/{len(dataset)}...")
            
    duration = time.time() - start_time
    print(f"    ✓ Ingestion complete in {duration:.2f}s")

    # 3. System Health Check
    print("\n[3] System State Analysis")
    # Accessing internals safely based on your interactive_test structure
    waves_count = len(tsw.field.waves)
    crystals_count = len(tsw.crystallizer.crystals)
    entanglements = sum(len(w.entangled_with) for w in tsw.field.waves)
    
    print(f"    - Active Waves: {waves_count}")
    print(f"    - Semantic Crystals Formed: {crystals_count}")
    print(f"    - Quantum Entanglements: {entanglements}")

    # 4. Detective Queries
    queries = [
        "What happened to Alice?",
        "Why did the servers overheat?",
        "Is Bob suspicious?",
        "What was Dave doing?"
    ]
    
    print("\n[4] Running Investigative Queries")
    print("-" * 70)
    
    for q in queries:
        print(f"\n🔍 Query: '{q}'")
        result = tsw.query(q)
        
        # Display Results
        insight = result.get('insight', 'No insight found')
        confidence = result.get('confidence', 0.0)
        
        print(f"   💡 Insight: {insight}")
        print(f"   📈 Confidence: {confidence:.1%}")
        
        evidence = result.get('evidence', [])
        if evidence:
            print("   📌 Key Evidence:")
            for i, ev in enumerate(evidence[:3], 1):
                text = ev[0] if isinstance(ev, tuple) else str(ev)
                print(f"      {i}. {text[:90]}...")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")

if __name__ == "__main__":
    main()