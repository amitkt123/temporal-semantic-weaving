import sys
import os
import time

# --- SETUP PATHS ---
# Ensure we can import from the 'tsw_enhanced' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
tsw_path = os.path.join(current_dir, 'tsw_enhanced')
if tsw_path not in sys.path:
    sys.path.append(tsw_path)

try:
    from tsw_enhanced.holographic.holographic_memory import HolographicMemory
except ImportError:
    print("❌ Critical Error: Could not import HolographicMemory.")
    print("   Ensure the folder is named 'tsw_enhanced' (underscore, not hyphen).")
    sys.exit(1)

def get_large_dataset():
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

def run_stress_test():
    print("\n" + "="*60)
    print(" 🏙️ PROJECT CHIMERA: TSW LARGE SCALE INVESTIGATION")
    print("="*60)
    
    # 1. Initialize Memory
    user_id = "Detective_Unit_01"
    print(f"Initializing Holographic Memory for Agent: {user_id}...")
    brain = HolographicMemory(user_id=user_id)
    
    # 2. Ingest Data
    dataset = get_large_dataset()
    print(f"\n[PHASE 1] Ingesting {len(dataset)} evidence logs...")
    
    start_time = time.time()
    for i, log in enumerate(dataset):
        # Ingest into TSW
        brain.ingest(log)
        
        # Progress indicator
        if i % 5 == 0:
            print(f"  Processed {i}/{len(dataset)} logs...", end='\r')
            
    total_time = time.time() - start_time
    print(f"  ✓ Ingestion Complete in {total_time:.2f} seconds.")

    # 3. The "Detective" Queries
    # These questions test if the system connected the dots.
    
    queries = [
        "What happened to Alice?",
        "Why did the servers overheat?",
        "Is Bob suspicious?",
        "What was Dave doing?"
    ]
    
    print("\n[PHASE 2] Running Investigative Queries...")
    
    for q in queries:
        print(f"\n🔍 Query: '{q}'")
        
        # We assume the new architecture has a 'retrieve' or similar method
        # Adjust method name if your API differs (e.g., find_resonances)
        try:
            if hasattr(brain, 'retrieve'):
                results = brain.retrieve(q, limit=3)
            elif hasattr(brain, 'find_resonances'):
                results = brain.find_resonances(q) # Might return tuples
            else:
                # Fallback to internal field if direct method missing
                results = ["Method 'retrieve' not found on HolographicMemory object"]

            # Display Results
            print("   💡 TSW Insights:")
            for i, res in enumerate(results):
                # Handle different return types (String, Object, Tuple)
                text = "Unknown"
                if isinstance(res, str): text = res
                elif isinstance(res, tuple): text = res[0] # (text, score)
                elif hasattr(res, 'source_text'): text = res.source_text
                elif hasattr(res, 'text'): text = res.text
                
                print(f"      {i+1}. {text}")
                
        except Exception as e:
            print(f"   ❌ Error querying brain: {e}")

    print("\n" + "="*60)
    print(" TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    run_stress_test()