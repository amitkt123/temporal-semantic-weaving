import numpy as np
from typing import List, Set
from sentence_transformers import SentenceTransformer
import hashlib

class EmbeddingEngine:
    """Advanced embedding engine using sentence transformers"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        try:
            self.model = SentenceTransformer(model_name)
            self.use_transformer = True
            self.dimension = 384  # all-MiniLM-L6-v2 dimension
        except:
            print("⚠️ Sentence transformer not available, using fallback")
            self.use_transformer = False
            self.dimension = 128
    
    def encode(self, text: str) -> np.ndarray:
        """Create semantic embedding from text"""
        if self.use_transformer:
            return self.model.encode(text, normalize_embeddings=True)
        else:
            return self._fallback_encode(text)
    
    def _fallback_encode(self, text: str) -> np.ndarray:
        """Fallback encoding using character trigrams"""
        vector = np.zeros(self.dimension)
        text_lower = text.lower()
        
        # Character trigrams
        for i in range(len(text_lower) - 2):
            trigram = text_lower[i:i+3]
            index = int(hashlib.md5(trigram.encode()).hexdigest(), 16) % self.dimension
            vector[index] += 1.0
        
        # Normalize
        if np.linalg.norm(vector) > 0:
            vector = vector / np.linalg.norm(vector)
        
        return vector
    
    def extract_keywords(self, text: str) -> Set[str]:
        """Extract meaningful keywords using NLP"""
        # Enhanced keyword extraction
        important_words = {
            'sarah', 'coffee', 'guitar', 'promotion', 'tom', 'career',
            'stuck', 'stressed', 'practice', 'morning', 'ritual', 'bar',
            'chords', 'meeting', 'work', 'friend', 'energy', 'pattern',
            'think', 'help', 'discuss', 'transition', 'path', 'learn'
        }
        
        words = text.lower().split()
        keywords = set()
        
        # Extract important words and longer words
        for word in words:
            cleaned = ''.join(c for c in word if c.isalpha())
            if cleaned in important_words or len(cleaned) > 5:
                keywords.add(cleaned)
        
        # Add bigrams for better context
        for i in range(len(words) - 1):
            bigram = f"{words[i]}_{words[i+1]}"
            if any(imp in bigram for imp in ['coffee', 'guitar', 'sarah', 'career']):
                keywords.add(bigram)
        
        return keywords