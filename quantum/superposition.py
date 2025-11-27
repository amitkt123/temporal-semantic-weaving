import numpy as np
from typing import List, Tuple
from core.wave import Wave

class QuantumSuperposition:
    """Creates and manages quantum superposition states"""
    
    def create_superposition(self, waves: List[Wave]) -> np.ndarray:
        """Create superposition from multiple waves"""
        if not waves:
            return np.array([])
        combined = np.zeros_like(waves[0].quantum_state) if waves[0].quantum_state is not None else np.zeros(100)
        for wave in waves:
            if wave.quantum_state is not None:
                combined += wave.amplitude * wave.quantum_state
        norm = np.linalg.norm(combined)
        if norm > 0:
            combined = combined / norm
        return combined
    
    def collapse_wavefunction(self, superposition: np.ndarray, measurement: np.ndarray) -> Tuple[np.ndarray, float]:
        """Collapse superposition with measurement"""
        overlap = np.abs(np.vdot(superposition, measurement))
        probability = float(overlap ** 2)
        collapsed = measurement * probability + superposition * (1 - probability)
        norm = np.linalg.norm(collapsed)
        if norm > 0:
            collapsed = collapsed / norm
        return collapsed, probability
