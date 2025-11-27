from typing import Dict, List, Set, Tuple
from core.wave import Wave

class QuantumEntanglement:
    """
    Robust entanglement manager.

    - Uses adjacency list graph structure.
    - Ensures no duplicates (set-based links).
    - Supports reversible lookup.
    - Provides normalized entanglement strengths.
    - Compatible with updated Wave class where entangled_with = set().
    """

    def __init__(self):
        # adjacency: wave_id -> set of wave_ids it is entangled with
        self.graph: Dict[str, Set[str]] = {}

    # -------------------------------------------------------
    #  ENTANGLING OPERATIONS
    # -------------------------------------------------------
    def entangle_waves(self, w1: Wave, w2: Wave):
        """Create symmetric entanglement edge between the two waves."""
        if w1.id == w2.id:
            return  # cannot entangle a wave with itself

        self.graph.setdefault(w1.id, set()).add(w2.id)
        self.graph.setdefault(w2.id, set()).add(w1.id)

        # also update wave objects themselves (for compatibility)
        if hasattr(w1, "entangled_with"):
            w1.entangled_with.add(w2.id)
        if hasattr(w2, "entangled_with"):
            w2.entangled_with.add(w1.id)

    # -------------------------------------------------------
    #  QUERY OPERATIONS
    # -------------------------------------------------------
    def get_entangled_ids(self, wave_id: str) -> Set[str]:
        """Return set of IDs entangled with given wave_id."""
        return self.graph.get(wave_id, set())

    def get_entangled_states(self, wave: Wave, wave_lookup: Dict[str, Wave]) -> List[Wave]:
        """Return the actual Wave objects entangled with `wave`."""
        ids = self.get_entangled_ids(wave.id)
        return [wave_lookup[w_id] for w_id in ids if w_id in wave_lookup]

    # -------------------------------------------------------
    #  STRENGTH MEASUREMENT
    # -------------------------------------------------------
    def measure_entanglement_strength(self, w1: Wave, w2: Wave) -> float:
        """Return entanglement strength based on normalized interfere_with()."""
        if w2.id not in self.get_entangled_ids(w1.id):
            return 0.0

        raw = w1.interfere_with(w2)  # raw similarity (can be -1..1)
        # normalize to 0..1
        strength = (raw + 1.0) / 2.0
        # clip
        return max(0.0, min(1.0, strength))

    # -------------------------------------------------------
    #  GRAPH ANALYTICS
    # -------------------------------------------------------
    def neighborhood(self, wave: Wave, depth: int = 1) -> Set[str]:
        """
        Return IDs in the entanglement neighborhood of a wave (BFS depth).
        depth=1 -> direct entanglement.
        depth=2 -> entangled with entangled, etc.
        """
        visited = {wave.id}
        frontier = {wave.id}

        for _ in range(depth):
            new_frontier = set()
            for wid in frontier:
                new_frontier |= self.graph.get(wid, set())
            new_frontier -= visited
            visited |= new_frontier
            frontier = new_frontier

        visited.remove(wave.id)
        return visited
