# temporal_braid.py
import math
from typing import List, Tuple, Dict, Optional, Set
from core.wave import Wave
from core.resonance_field import ResonanceField
import numpy as np
from collections import deque, defaultdict

# Tunable thresholds
KEYWORD_MATCH_MIN = 1                # minimum shared keywords to seed a braid
COSINE_SIM_THRESHOLD = 0.35          # fallback semantic similarity threshold
BRAID_APPEND_SIM = 0.30              # similarity threshold to append to existing braid
MAX_BRAID_GAP = 3600.0               # seconds: max allowed time gap to append (optional)

class TemporalBraid:
    """Robust temporal braid manager.

    - Maintains braids as ordered lists of wave IDs.
    - Appends new waves to the best-matching braid, or creates a new braid.
    - Can detect pairwise repeated patterns and causal loops.
    """

    def __init__(self, field: Optional[ResonanceField] = None):
        # braids: list of lists of wave ids (ordered by insertion time)
        self.braids: List[List[str]] = []
        # index id -> braid index for quick membership queries
        self._id_to_braid: Dict[str, int] = {}
        # counts of occurrences for quick stats
        self._occurrence_counts: Dict[str, int] = defaultdict(int)
        # optional reference to field for embeddings lookup
        self.field = field
        # detected causal loops (tuples of wave ids)
        self.causal_loops: List[Tuple[str, ...]] = []

    # -------------------------
    #  Public API
    # -------------------------
    def weave(self, wave: Wave):
        """Insert a wave into an appropriate braid or create a new braid.

        Strategy:
        - Attempt to append to the most recently active braid whose tail is similar.
        - Similarity uses: keyword overlap, then embedding cosine if available.
        - Falls back to creating a new braid.
        """
        wid = wave.id
        self._occurrence_counts[wid] += 1

        # Quick check: if already present in braid, ignore or reorder
        if wid in self._id_to_braid:
            # already in a braid; optionally move to its braid tail time
            return

        # find candidate braids (we'll check only last element of each braid)
        best_braid_idx = None
        best_score = -math.inf

        for idx, braid in enumerate(self.braids):
            if not braid:
                continue
            tail_id = braid[-1]
            tail_wave = self._get_wave_by_id(tail_id)
            if tail_wave is None:
                continue

            score = self._similarity_score(wave, tail_wave)
            # optionally enforce recency gap
            if (wave.timestamp is not None and tail_wave.timestamp is not None
                    and (wave.timestamp - tail_wave.timestamp) > MAX_BRAID_GAP):
                # considered too old to append
                continue

            if score > best_score:
                best_score = score
                best_braid_idx = idx

        # Append if best score passes threshold, else create new braid
        if best_braid_idx is not None and best_score >= BRAID_APPEND_SIM:
            self.braids[best_braid_idx].append(wid)
            self._id_to_braid[wid] = best_braid_idx
        else:
            # create new braid
            bidx = len(self.braids)
            self.braids.append([wid])
            self._id_to_braid[wid] = bidx

    def detect_patterns(self, min_repeats: int = 2, max_pattern_len: int = 6) -> List[Tuple[List[str], int]]:
        """Detect repeating subsequences across braids.

        Returns list of (pattern_list_of_ids, count) for patterns repeated >= min_repeats.
        This is a simple n-gram frequency mining across braids tails.
        """
        pattern_counts: Dict[Tuple[str, ...], int] = defaultdict(int)

        for braid in self.braids:
            L = len(braid)
            # collect all subsequences up to length max_pattern_len
            for start in range(L):
                for length in range(2, min(max_pattern_len, L - start) + 1):
                    subseq = tuple(braid[start:start + length])
                    pattern_counts[subseq] += 1

        # filter patterns with frequency >= min_repeats
        results = [(list(p), c) for p, c in pattern_counts.items() if c >= min_repeats]
        # sort by count desc then length desc (longer, more informative patterns first)
        results.sort(key=lambda x: (x[1], len(x[0])), reverse=True)
        return results

    def detect_causal_loops(self, max_loop_len: int = 5, min_occurrences: int = 2):
        """Detect repeated cyclic patterns and register as causal loops.

        A causal loop is a repeating sequence that appears at least min_occurrences times
        and whose first and last elements can be treated as cause/effect in time order.
        """
        patterns = self.detect_patterns(min_repeats=min_occurrences, max_pattern_len=max_loop_len)
        loops = []
        for pattern, count in patterns:
            # crude heuristic: if pattern appears multiple times and spans time, treat as loop
            if count >= min_occurrences and len(pattern) >= 2:
                loops.append(tuple(pattern))
        self.causal_loops = loops
        return loops

    # -------------------------
    #  Utilities
    # -------------------------
    def _similarity_score(self, w1: Wave, w2: Wave) -> float:
        """Compute a combined similarity score in [ -1 .. 1 ] (higher means more similar).

        Priority:
        1) keyword overlap -> quick boost
        2) cosine similarity of vectors if available
        """
        # keyword overlap normalized
        kw1 = set(w1.keywords or ())
        kw2 = set(w2.keywords or ())
        if kw1 or kw2:
            overlap = len(kw1 & kw2)
            denom = max(1, len(kw1 | kw2))
            kw_score = overlap / denom
        else:
            kw_score = 0.0

        # embedding cosine similarity (if vectors present)
        vec1 = getattr(w1, "vector", None)
        vec2 = getattr(w2, "vector", None)
        cos = 0.0
        if vec1 is not None and vec2 is not None:
            v1 = np.asarray(vec1, dtype=float)
            v2 = np.asarray(vec2, dtype=float)
            n1 = np.linalg.norm(v1)
            n2 = np.linalg.norm(v2)
            if n1 > 0 and n2 > 0:
                cos = float(np.dot(v1, v2) / (n1 * n2))

        # combine: keyword strong boost + cosine fallback
        # map keyword score (0..1) to [-1..1] range contribution via linear scaling
        combined = 0.6 * (2 * kw_score - 1) + 0.4 * cos
        return float(combined)

    def _get_wave_by_id(self, wid: str) -> Optional[Wave]:
        """Lookup waves from the associated field if available."""
        if self.field is None:
            return None
        # field should expose a mapping or you can search (we'll search for small sizes)
        for w in self.field.waves:
            if w.id == wid:
                return w
        return None

    def summarize_braids(self, top_n: int = 10) -> List[Dict]:
        """Return a summary of braids with sizes, keywords, and representative wave."""
        summaries = []
        for braid in self.braids[:top_n]:
            members = [self._get_wave_by_id(wid) for wid in braid]
            members = [m for m in members if m is not None]
            keywords = set()
            for m in members:
                keywords |= set(getattr(m, "keywords", set()))
            rep = members[-1] if members else None
            summaries.append({
                "size": len(braid),
                "keywords": keywords,
                "representative_id": rep.id if rep else None,
                "representative_snippet": rep.source_text[:200] if rep else None
            })
        return summaries
