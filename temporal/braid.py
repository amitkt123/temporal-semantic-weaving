from typing import List, Tuple
from core.wave import Wave

class TemporalBraid:
    """Weaves waves together through time"""
    
    def __init__(self):
        self.braids: List[List[Wave]] = []
        self.causal_loops: List[Tuple[str, ...]] = []
        
    def weave(self, wave: Wave):
        """Add wave to temporal braid"""
        self.braids.append([wave])
        
    def detect_patterns(self) -> List[Tuple[Wave, Wave]]:
        """Detect repeating patterns in the braid"""
        patterns = []
        for i, braid1 in enumerate(self.braids):
            for braid2 in self.braids[i+1:]:
                if braid1 and braid2:
                    if self._patterns_match(braid1[0], braid2[0]):
                        patterns.append((braid1[0], braid2[0]))
        return patterns
    
    def _patterns_match(self, wave1: Wave, wave2: Wave) -> bool:
        """Check if two waves have similar patterns"""
        return len(wave1.keywords & wave2.keywords) > 0
