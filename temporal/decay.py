import numpy as np
from typing import List
from core.wave import Wave

class TemporalDecay:
    """Sophisticated temporal decay mechanisms"""
    
    @staticmethod
    def exponential_decay(wave: Wave, time_delta: float, rate: float = 0.01) -> float:
        """Standard exponential decay"""
        return float(np.exp(-rate * time_delta))
    
    @staticmethod
    def power_law_decay(wave: Wave, time_delta: float, exponent: float = 0.5) -> float:
        """Power law decay - slower than exponential"""
        return 1.0 / (1.0 + time_delta) ** exponent
    
    @staticmethod
    def adaptive_decay(wave: Wave, time_delta: float, field_context: dict) -> float:
        """Adaptive decay based on importance"""
        base_decay = float(np.exp(-0.01 * time_delta))
        importance = len(wave.keywords) / 10.0
        importance_factor = 1.0 - importance * 0.5
        entanglement_factor = 1.0 - len(wave.entangled_with) * 0.1
        return base_decay * importance_factor * entanglement_factor
    
    @staticmethod
    def interference_protected_decay(wave: Wave, time_delta: float, active_resonances: int) -> float:
        """Decay protected by active resonances"""
        base_decay = float(np.exp(-0.01 * time_delta))
        protection = 1.0 + active_resonances * 0.2
        return min(1.0, base_decay * protection)

class MemoryConsolidation:
    """Long-term memory consolidation"""
    
    def __init__(self):
        self.consolidation_threshold = 0.8
        self.replay_factor = 1.2
        
    def consolidate(self, waves: List[Wave], time: float) -> List[Wave]:
        """Consolidate important memories"""
        consolidated = []
        for wave in waves:
            if self._should_consolidate(wave, time):
                wave.amplitude *= self.replay_factor
                wave.quantum_state = self._strengthen_quantum_state(wave.quantum_state)
            consolidated.append(wave)
        return consolidated
    
    def _should_consolidate(self, wave: Wave, current_time: float) -> bool:
        """Determine if memory should be consolidated"""
        age = current_time - wave.timestamp
        return age > 10 and wave.amplitude > self.consolidation_threshold
    
    def _strengthen_quantum_state(self, state):
        """Strengthen quantum coherence"""
        if state is None:
            return None
        state = state * 1.1
        state = state / np.linalg.norm(state)
        return state
