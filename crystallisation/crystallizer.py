# semantic_crystallizer.py
from typing import List, Dict, Set, Optional
from core.resonance_field import ResonanceField
from core.wave import Wave
import numpy as np

# Tunable hyperparameters
MIN_CLUSTER_SIZE = 2
KEYWORD_SEED_MIN_OVERLAP = 1          # min shared keywords to consider seeding cluster
COHESION_SIM_THRESHOLD = 0.35        # min mean pairwise sim to consider cohesive
STABILITY_ALPHA = 0.6                # weight for cohesion in final stability (rest to amplitude)
MAX_STABILITY = 1.0

class SemanticCrystallizer:
    """Crystallizes semantic patterns from a ResonanceField into 'crystals'."""

    def __init__(self, crystallization_threshold: float = 0.7):
        self.crystals: List[Dict] = []
        self.crystallization_threshold = float(crystallization_threshold)

    def check_crystallization(self, field: ResonanceField) -> List[Dict]:
        """Scan the field and return newly detected crystals (and record them)."""
        new_crystals = []
        waves = list(field.waves)
        if len(waves) <= MIN_CLUSTER_SIZE:
            return new_crystals

        # Step 1: build keyword-based candidate clusters (fast)
        candidate_clusters = self._keyword_seed_clusters(waves)

        # Step 2: validate & refine clusters using semantic cohesion (embeddings) when available
        for cluster in candidate_clusters:
            if len(cluster) < MIN_CLUSTER_SIZE:
                continue

            # compute cohesion: mean pairwise cosine similarity of vectors
            cohesion = self._cluster_cohesion(cluster, field)
            avg_amplitude = float(sum(w.amplitude for w in cluster) / len(cluster))

            # final stability score combines cohesion and amplitude
            stability = self._combine_stability(cohesion, avg_amplitude)

            if stability >= self.crystallization_threshold:
                crystal = {
                    "members": [w.id for w in cluster],
                    "size": len(cluster),
                    "keywords": self._extract_common_keywords(cluster),
                    "cohesion": float(cohesion),
                    "avg_amplitude": float(avg_amplitude),
                    "stability": float(min(MAX_STABILITY, stability)),
                    "representative": self._representative_text(cluster)
                }
                new_crystals.append(crystal)
                self.crystals.append(crystal)

        return new_crystals

    # -----------------------------
    #  Keyword-based seeding
    # -----------------------------
    def _keyword_seed_clusters(self, waves: List[Wave]) -> List[List[Wave]]:
        clusters: List[List[Wave]] = []
        used_ids = set()
        # map from id->wave for quick lookup
        id_map = {w.id: w for w in waves}
        for i, w1 in enumerate(waves):
            if w1.id in used_ids:
                continue
            cluster = [w1]
            used_ids.add(w1.id)
            # examine later waves for keyword overlap
            for w2 in waves[i+1:]:
                if w2.id in used_ids:
                    continue
                if len(w1.keywords & w2.keywords) >= KEYWORD_SEED_MIN_OVERLAP:
                    cluster.append(w2)
                    used_ids.add(w2.id)
            if len(cluster) >= MIN_CLUSTER_SIZE:
                clusters.append(cluster)
        return clusters

    # -----------------------------
    #  Cohesion via embeddings
    # -----------------------------
    def _cluster_cohesion(self, cluster: List[Wave], field: ResonanceField) -> float:
        """Return mean pairwise cosine similarity (0..1 scaled is optional)."""
        vectors = []
        # Use embedding vectors on each wave (should already be present as wave.vector)
        for w in cluster:
            vec = getattr(w, "vector", None)
            if vec is None:
                # try to re-embed with field's embedding engine
                if hasattr(field, "embedding_engine") and getattr(field, "embedding_engine") is not None:
                    vec = field.embedding_engine.embed_text(w.source_text)
            if vec is None:
                # missing vector -> treat as low cohesion
                return 0.0
            vectors.append(np.asarray(vec, dtype=float))

        # Compute pairwise cosine similarities
        n = len(vectors)
        if n <= 1:
            return 0.0
        sims = []
        norms = [np.linalg.norm(v) for v in vectors]
        for i in range(n):
            for j in range(i + 1, n):
                ni = norms[i]; nj = norms[j]
                if ni == 0 or nj == 0:
                    s = 0.0
                else:
                    s = float(np.dot(vectors[i], vectors[j]) / (ni * nj))
                sims.append(s)
        # mean of pairwise sims
        mean_sim = float(np.mean(sims)) if sims else 0.0
        return mean_sim

    # -----------------------------
    #  Keywords & stability
    # -----------------------------
    def _extract_common_keywords(self, waves: List[Wave]) -> Set[str]:
        if not waves:
            return set()
        common = set(waves[0].keywords)
        for w in waves[1:]:
            common &= set(w.keywords)
        return common

    def _combine_stability(self, cohesion: float, avg_amplitude: float) -> float:
        """Combine cohesion (0..1?) and amplitude into a stability score [0..1].
        Expects cohesion roughly in [-1..1] if using raw cosine; we map to 0..1.
        """
        # map cohesion (-1..1) -> (0..1)
        coh01 = (cohesion + 1.0) / 2.0 if cohesion <= 1.0 else cohesion
        # normalize amplitude by a soft cap (assume amplitude typically ~0..2)
        amp_norm = min(1.0, avg_amplitude / 2.0)
        # weighted combination
        return STABILITY_ALPHA * coh01 + (1.0 - STABILITY_ALPHA) * amp_norm

    def _representative_text(self, cluster: List[Wave]) -> str:
        """Pick the highest-amplitude member's snippet as representative."""
        best = max(cluster, key=lambda w: w.amplitude)
        return best.source_text[:250]
