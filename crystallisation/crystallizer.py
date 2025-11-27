from typing import List, Dict
from core.resonance_field import ResonanceField
from core.wave import Wave

class SemanticCrystallizer:
    """Crystallizes semantic patterns from resonance field"""
    
    def __init__(self):
        self.crystals: List[Dict] = []
        self.crystallization_threshold = 0.7
        
    def check_crystallization(self, field: ResonanceField) -> List[Dict]:
        """Check if patterns are crystallizing into stable structures"""
        new_crystals = []
        if len(field.waves) > 3:
            clusters = self._form_clusters(field.waves)
            for cluster in clusters:
                if len(cluster) > 1:
                    crystal = {
                        'members': cluster,
                        'keywords': self._extract_common_keywords(cluster),
                        'stability': self._calculate_stability(cluster)
                    }
                    if crystal['stability'] > self.crystallization_threshold:
                        new_crystals.append(crystal)
                        self.crystals.append(crystal)
        return new_crystals
    
    def _form_clusters(self, waves: List[Wave]) -> List[List[Wave]]:
        """Form clusters of similar waves"""
        clusters = []
        used = set()
        for i, wave1 in enumerate(waves):
            if i in used:
                continue
            cluster = [wave1]
            used.add(i)
            for j, wave2 in enumerate(waves[i+1:], start=i+1):
                if j not in used and len(wave1.keywords & wave2.keywords) > 0:
                    cluster.append(wave2)
                    used.add(j)
            if len(cluster) > 1:
                clusters.append(cluster)
        return clusters
    
    def _extract_common_keywords(self, waves: List[Wave]) -> set:
        """Extract keywords common to all waves in cluster"""
        if not waves:
            return set()
        common = waves[0].keywords.copy()
        for wave in waves[1:]:
            common = common & wave.keywords
        return common
    
    def _calculate_stability(self, waves: List[Wave]) -> float:
        """Calculate stability of a cluster"""
        if not waves:
            return 0.0
        avg_amplitude = sum(w.amplitude for w in waves) / len(waves)
        return min(1.0, avg_amplitude)
