# embeddings_fixed.py
import numpy as np
from typing import Optional, Set
from functools import lru_cache
import re
import hashlib

try:
    from sentence_transformers import SentenceTransformer
    _HAS_ST = True
except Exception:
    _HAS_ST = False


_WORD_CLEANER = re.compile(r"[^a-zA-Z0-9']+")

# small stopword set (expand as needed)
_STOPWORDS = {
    "the", "and", "a", "an", "of", "in", "on", "for", "to", "is", "it", "that",
    "this", "with", "as", "was", "were", "by", "be", "are", "at", "from"
}

class EmbeddingEngine:
    """Robust embedding engine with SentenceTransformers (if available)
    and a deterministic trigram fallback.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", fallback_dim: int = 384, cache_size: int = 4096):
        self.model_name = model_name
        self.model = None
        self.use_transformer = False
        self.dimension = int(fallback_dim)

        if _HAS_ST:
            try:
                self.model = SentenceTransformer(model_name)
                self.use_transformer = True
                # get actual model dimension if available
                try:
                    self.dimension = int(self.model.get_sentence_embedding_dimension())
                except Exception:
                    # fallback keeps whatever we set earlier
                    pass
            except Exception:
                # transformer instantiation failed -> fallback
                self.model = None
                self.use_transformer = False

        # Simple LRU cache for embeddings (string -> tuple(serialized vector))
        self._embed_cache = lru_cache(maxsize=cache_size)(self._embed_uncached)

    # Public API
    def embed_text(self, text: str) -> Optional[np.ndarray]:
        """Return a normalized embedding (numpy.ndarray, dtype=float32) or None for empty input."""
        if not text:
            return None
        # Use the cached internal function (which handles transformer or fallback)
        vec = self._embed_cache(text)
        if vec is None:
            return None
        # Ensure float32 numpy array
        vec = np.asarray(vec, dtype=np.float32)
        # defensive normalization (should already be normalized)
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec

    # keep `encode` as alias for compatibility with older code
    def encode(self, text: str) -> Optional[np.ndarray]:
        return self.embed_text(text)

    # Internal - actual embedding computation (not cached)
    def _embed_uncached(self, text: str) -> Optional[np.ndarray]:
        if self.use_transformer and self.model is not None:
            try:
                # SentenceTransformer.encode returns numpy array; normalize explicitly
                vec = self.model.encode(text, show_progress_bar=False)
                vec = np.asarray(vec, dtype=np.float32)
                norm = np.linalg.norm(vec)
                if norm > 0:
                    vec = vec / norm
                return vec
            except Exception:
                # on failure, fall back below
                pass

        # Fallback deterministic trigram hashing
        return self._fallback_trigram_hash(text)

    def _fallback_trigram_hash(self, text: str) -> np.ndarray:
        d = int(self.dimension) if self.dimension > 0 else 384
        vec = np.zeros(d, dtype=np.float32)
        s = text.lower()
        # build trigrams
        for i in range(len(s) - 2):
            tri = s[i : i + 3]
            # ignore spaces-only trigrams
            if tri.strip() == "":
                continue
            h = int(hashlib.sha256(tri.encode("utf-8")).hexdigest(), 16)
            idx = h % d
            # weight contribution by small number to avoid huge counts
            vec[idx] += 1.0
        # final normalization
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec

    def extract_keywords(self, text: str, min_len: int = 4, include_bigrams: bool = True) -> Set[str]:
        """Extract simple keywords: cleaned tokens longer than min_len or not stopwords.
        Returns a set of keyword strings (lowercased).
        """
        if not text:
            return set()

        # Basic tokenization & cleaning
        tokens = []
        for raw in text.split():
            cleaned = _WORD_CLEANER.sub(" ", raw).strip().lower()
            if not cleaned:
                continue
            # split internal cleaned pieces
            for part in cleaned.split():
                if len(part) >= min_len and part not in _STOPWORDS:
                    tokens.append(part)

        keywords = set(tokens)

        # Optionally add bigrams
        if include_bigrams:
            for i in range(len(tokens) - 1):
                bigram = f"{tokens[i]}_{tokens[i+1]}"
                keywords.add(bigram)

        return keywords
