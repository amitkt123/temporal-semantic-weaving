import numpy as np
from typing import List
from core.wave import Wave

class TemporalDecay:
    """Stabilized multi-model temporal decay subsystem."""

    MIN_DECAY = 0.05     # never fully die
    MAX_DECAY = 1.0

    @staticmethod
    def exponential_decay(time_delta: float, rate: float = 0.01) -> float:
        raw = float(np.exp(-rate * time_delta))
        return max(TemporalDecay.MIN_DECAY, min(raw, TemporalDecay.MAX_DECAY))

    @staticmethod
    def power_law_decay(time_delta: float, exponent: float = 0.5) -> float:
        raw = 1.0 / ((1.0 + time_delta) ** exponent)
        return max(TemporalDecay.MIN_DECAY, min(raw, TemporalDecay.MAX_DECAY))

    @staticmethod
    def adaptive_decay(wave: Wave, time_delta: float, field_context: dict) -> float:
        """Adaptive decay based on importance, but always bounded."""
        # base exponential
        base = float(np.exp(-0.01 * time_delta))

        # importance: number of keywords, normalized 0..1
        importance_norm = min(1.0, len(wave.keywords) / 12.0)

        # entanglement: stronger memories decay slower
        entanglement_norm = min(1.0, len(wave.entangled_with) / 10.0)

        # combine: important & strongly entangled memories decay slower
        # weighted sum keeps output in safe range
        protected = base * (0.7 + 0.3 * importance_norm + 0.3 * entanglement_norm)

        return max(TemporalDecay.MIN_DECAY, min(protected, TemporalDecay.MAX_DECAY))

    @staticmethod
    def interference_protected_decay(time_delta: float, active_resonances: int) -> float:
        """Waves with many active resonances decay slower."""
        base = float(np.exp(-0.01 * time_delta))
        protection = 1.0 + min(0.8, active_resonances * 0.1)
        raw = base * protection

        return max(TemporalDecay.MIN_DECAY, min(raw, TemporalDecay.MAX_DECAY))


class MemoryConsolidation:
    """Stabilized long-term memory consolidation."""

    def __init__(self):
        self.consolidation_threshold = 0.7
        self.max_amplitude = 2.0          # cap to prevent explosion
        self.replay_factor = 1.1          # gentle strengthening

    def consolidate(self, waves: List[Wave], current_time: float) -> List[Wave]:
        consolidated = []
        for wave in waves:
            if self._should_consolidate(wave, current_time):
                self._apply_consolidation(wave)
            consolidated.append(wave)
        return consolidated

    # ----------------------------------------------------------
    #  Internal methods
    # ----------------------------------------------------------
    def _should_consolidate(self, wave: Wave, current_time: float) -> bool:
        age = current_time - wave.timestamp
        if age < 8:  # too recent to consolidate
            return False

        # Consolidate if wave shows stable presence
        return (
            wave.amplitude > self.consolidation_threshold or
            len(wave.entangled_with) >= 2 or
            len(wave.keywords) >= 4
        )

    def _apply_consolidation(self, wave: Wave):
        """Apply amplitude & coherence strengthening safely."""
        # safe amplitude strengthening
        wave.amplitude *= self.replay_factor
        wave.amplitude = min(wave.amplitude, self.max_amplitude)

        # strengthen quantum coherence slightly
        if wave.quantum_state is not None:
            wave.quantum_state *= 1.05
            # normalize
            n = np.linalg.norm(wave.quantum_state)
            if n > 0:
                wave.quantum_state /= n
