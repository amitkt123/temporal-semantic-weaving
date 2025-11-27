import sys
import os
import time
import requests
import re

# --- SETUP PATHS ---

# Ensure we can import from current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main import EnhancedTSW
except ImportError:
    print("❌ Error: Could not import EnhancedTSW from main.py")
    print("   Make sure you are running this from the tsw_enhanced directory.")
    sys.exit(1)

def get_sherlock_story():
    """
    Downloads 'A Scandal in Bohemia' from Project Gutenberg.
    """
    filename = "sherlock.txt"
    
    if os.path.exists(filename):
        print(f"📖 Loading local file: {filename}")
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
            
    print("⬇️ Downloading book from Project Gutenberg...")
    url = "https://www.gutenberg.org/files/1661/1661-0.txt"
    try:
        response = requests.get(url)
        text = response.text
        
        # Extract just the first story to keep the test focused (~20 pages)
        start = text.find("A SCANDAL IN BOHEMIA")
        end = text.find("THE RED-HEADED LEAGUE")
        
        if start != -1 and end != -1:
            story = text[start:end]
            # Clean up Gutenberg headers/newlines
            story = re.sub(r'\r\n', ' ', story)
            story = re.sub(r'\s+', ' ', story)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(story)
            return story
        return text[:50000] # Fallback
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return None

def chunk_text(text, chunk_size=400):
    """Splits the story into digestable semantic chunks."""
    # Split by sentences first
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = []
    current_len = 0
    
    for s in sentences:
        current_chunk.append(s)
        current_len += len(s)
        if current_len > chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_len = 0
            
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def run_literary_test():
    print("\n" + "="*70)
    print("🕵️ TSW LITERARY INTELLIGENCE TEST: SHERLOCK HOLMES")
    print("="*70)
    
    # 1. Initialize
    print("\n[1] Waking up the Detective Engine...")
    tsw = EnhancedTSW()
    
    # 2. Get Data
    story_text = get_sherlock_story()
    if not story_text: return
    
    chunks = chunk_text(story_text)
    print(f"\n[2] Reading Story ({len(chunks)} narrative segments)...")
    
    start_time = time.time()
    for i, chunk in enumerate(chunks):
        tsw.add_experience(chunk)
        if i % 5 == 0:
            print(f"    Reading paragraph {i}/{len(chunks)}...", end='\r')
            
    print(f"    ✓ Finished reading in {time.time() - start_time:.2f}s")
    
    # 3. Stats
    print("\n[3] Memory State")
    print(f"    - Concepts Entangled: {sum(len(w.entangled_with) for w in tsw.field.waves)}")
    print(f"    - Crystals Formed: {len(tsw.crystallizer.crystals)}")

    # 4. The Comprehension Test
    # These questions require linking facts across the story
    questions = [
        "Who is Irene Adler?",
        "What was the King looking for?",
        "Where did the fire start?",
        "Why did Holmes dress up as a clergyman?"
    ]
    
    print("\n[4] Examining the Evidence")
    print("-" * 70)
    
    for q in questions:
        print(f"\n🔍 Query: '{q}'")
        result = tsw.query(q)
        
        print(f"   💡 Answer: {result.get('answer', 'No insight found')}")
        print(f"   📈 Confidence: {result.get('confidence', 0.0):.1%}")
        
        if result.get('evidence'):
            print("   📌 Textual Proof:")
            for i, ev in enumerate(result['evidence'][:2]): # Show top 2 proofs
                text = ev.get('text', str(ev)) if isinstance(ev, dict) else (ev[0] if isinstance(ev, tuple) else str(ev))
                print(f"      - \"{text[:90]}...\"")

if __name__ == "__main__":
    run_literary_test()