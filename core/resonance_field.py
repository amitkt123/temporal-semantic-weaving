import numpy as np
from typing import List, Tuple, Set, Optional
from .wave import Wave
from .embeddings import EmbeddingEngine
import uuid
import math

# =============================
#  CONFIGURABLE CONSTANTS
# =============================
CONSTRUCTIVE_THRESHOLD = 0.05         # Minimum similarity to consider constructive
ENTANGLE_THRESHOLD = 0.45             # When cosine similarity triggers entanglement
KEYWORD_BONUS = 0.15                  # Boost per overlapping keyword
ENTANGLEMENT_ALPHA = 0.05             # Normalized entanglement bonus
MAX_QUANTUM_DIM = 100                 # Max size of quantum state slice
FIELD_NORM_LIMIT = 10                 # Prevent tensor explosion


class ResonanceField:
    """
    Stable, corrected version of the Resonance Field with:
    - stable embedding API
    - cosine-based retrieval
    - robust quantum state
    - clean entanglement logic
    """

    def __init__(self, dimensions: int = 384):
        self.dimensions = dimensions
        self.waves: List[Wave] = []
        self.time = 0.0
        self.embedding_engine = EmbeddingEngine()

        # Field tensor (square matrix)
        self.field_tensor = np.zeros((dimensions, dimensions), dtype=complex)

    # ================================================================
    #   EXPERIENCE INGESTION
    # ================================================================
    def add_experience(self, text: str) -> Tuple[Wave, List[Tuple[str, float]]]:
        wave = self._create_wave(text)
        resonances = self._apply_interference(wave)
        self.waves.append(wave)
        self._update_field_tensor(wave)
        self.time += 1.0
        return wave, resonances

    # ================================================================
    #   WAVE CREATION
    # ================================================================
    def _create_wave(self, text: str) -> Wave:
        # ---- Embedding ----
        if hasattr(self.embedding_engine, "embed_text"):
            vector = self.embedding_engine.embed_text(text)
        else:
            vector = self.embedding_engine.encode(text)

        if vector is None:
            vector = np.zeros(self.dimensions, dtype=float)

        vector = np.asarray(vector, dtype=float)

        # ---- Fix vector size ----
        if len(vector) != self.dimensions:
            vec = np.zeros(self.dimensions, dtype=float)
            L = min(len(vector), self.dimensions)
            vec[:L] = vector[:L]
            vector = vec

        # ---- Keywords ----
        keywords = self.embedding_engine.extract_keywords(text)

        # ---- Frequency ----
        frequency = self._calculate_frequency(keywords)

        # ---- Phase ----
        phase = (self.time * 0.1) % (2 * math.pi)

        # ---- Quantum State ----
        quantum_state = self._create_quantum_state(vector)

        # ---- Final Wave Object ----
        return Wave(
            id=str(uuid.uuid4()),
            vector=vector,
            amplitude=1.0,
            frequency=frequency,
            phase=phase,
            timestamp=self.time,
            source_text=text,
            keywords=set(keywords),
            quantum_state=quantum_state,
            entangled_with=set()
        )

    # ================================================================
    #   FREQUENCY MAPPING
    # ================================================================
    def _calculate_frequency(self, keywords: Set[str]) -> float:
        freq_map = {
            'coffee': 2.0, 'morning': 2.5, 'ritual': 2.3,
            'guitar': 3.0, 'practice': 3.2, 'chords': 3.5,
            'career': 4.0, 'promotion': 4.2, 'work': 4.1,
            'sarah': 5.0, 'friend': 5.2, 'help': 5.1
        }

        if not keywords:
            return 1.0

        values = [freq_map.get(k, 1.0) for k in keywords]
        return float(np.mean(values))

    # ================================================================
    #   QUANTUM STATE CREATION
    # ================================================================
    def _create_quantum_state(self, vector: np.ndarray) -> np.ndarray:
        vec = np.asarray(vector, dtype=float)
        n = len(vec)
        L = min(MAX_QUANTUM_DIM, n)

        real = vec[:L]
        roll = max(1, L // 4)
        imag = np.roll(real, roll)

        q = real + 1j * imag * 0.5

        norm = np.linalg.norm(q)
        if norm == 0:
            q = q + 1e-9
            norm = np.linalg.norm(q)

        return q / norm

    # ================================================================
    #   INTERFERENCE & ENTANGLEMENT
    # ================================================================
    def _apply_interference(self, new_wave: Wave, top_k: int = 3) -> List[Tuple[str, float]]:
        if not self.waves:
            return []

        qvec = new_wave.vector
        qnorm = np.linalg.norm(qvec) or 1.0

        results = []

        for w in self.waves:
            wvec = w.vector
            wnorm = np.linalg.norm(wvec) or 1.0

            # ---- Cosine Similarity ----
            sim = float(np.dot(qvec, wvec) / (qnorm * wnorm))

            # ---- Keyword Boost ----
            k_overlap = len(new_wave.keywords & w.keywords)
            sim += KEYWORD_BONUS * k_overlap

            # ---- Weighted ----
            weighted = sim * w.amplitude

            # ---- Entanglement Trigger ----
            if sim > ENTANGLE_THRESHOLD:
                w.entangled_with.add(new_wave.id)
                new_wave.entangled_with.add(w.id)

            # ---- Constructive / destructive ----
            if weighted > CONSTRUCTIVE_THRESHOLD:
                w.amplitude *= (1.0 + 0.05 * weighted)
                new_wave.amplitude *= (1.0 + 0.03 * weighted)
            elif weighted < -0.2:
                w.amplitude *= (1.0 - 0.03 * abs(weighted))

            results.append((w.source_text[:200], float(weighted)))

        # Return top-K by weighted similarity
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    # ================================================================
    #   FIELD TENSOR UPDATE
    # ================================================================
    def _update_field_tensor(self, wave: Wave):
        vec = wave.vector
        L = len(vec)

        # Resize tensor if needed
        if self.field_tensor.shape != (L, L):
            self.field_tensor = np.zeros((L, L), dtype=complex)
            self.dimensions = L

        outer = np.outer(vec, vec)
        phase = np.exp(1j * wave.phase)

        self.field_tensor += wave.amplitude * outer * phase

        # Prevent blow-up
        max_val = np.max(np.abs(self.field_tensor))
        if max_val > FIELD_NORM_LIMIT:
            self.field_tensor /= (max_val / FIELD_NORM_LIMIT)

    # ================================================================
    #   RETRIEVAL
    # ================================================================
    def find_resonances(self, query_text: str, top_k: int = 5) -> List[Tuple[Wave, float]]:
        if hasattr(self.embedding_engine, "embed_text"):
            qvec = self.embedding_engine.embed_text(query_text)
        else:
            qvec = self.embedding_engine.encode(query_text)

        if qvec is None:
            return []

        qvec = np.asarray(qvec, dtype=float)
        qnorm = np.linalg.norm(qvec)
        if qnorm == 0:
            return []

        results = []

        for wave in self.waves:
            wvec = wave.vector
            wnorm = np.linalg.norm(wvec) or 1.0

            # Base cosine similarity
            sim = float(np.dot(qvec, wvec) / (qnorm * wnorm))

            # Normalized entanglement bonus
            ec = len(wave.entangled_with)
            if ec > 0:
                sim *= (1.0 + ENTANGLEMENT_ALPHA * (ec / (ec + 5.0)))

            results.append((wave, sim))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    # ================================================================
    #   FIELD ENERGY (OPTIONAL)
    # ================================================================
    def get_field_energy(self) -> float:
        """Calculate total field energy with overflow protection."""
        kinetic = 0.0
        for w in self.waves:
            # Clamp amplitude to prevent overflow
            amp = max(-1e10, min(1e10, float(w.amplitude)))
            freq = max(0.01, min(1000.0, float(w.frequency)))
            # Use safe computation with bounds
            term = min(1e15, amp**2 * freq)  # Cap individual terms
            kinetic = min(1e15, kinetic + term)
        
        potential = min(1e15, float(np.sum(np.abs(self.field_tensor)**2)))
        vacuum = 0.01 * len(self.waves)
        
        total = kinetic + potential + vacuum
        return min(1e15, float(total))  # Final cap to prevent overflow
