import numpy as np
from dataclasses import dataclass, field
from typing import Set, Optional, List
import uuid
import math

# small helper
def safe_norm(x: np.ndarray) -> float:
    n = np.linalg.norm(x)
    return float(n) if n > 0 else 0.0

@dataclass
class Wave:
    """Enhanced wave with quantum properties (robust)."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    vector: np.ndarray = field(default_factory=lambda: np.zeros(0, dtype=float))
    amplitude: float = 1.0
    frequency: float = 1.0
    phase: float = 0.0
    timestamp: float = 0.0
    source_text: str = ""
    keywords: Set[str] = field(default_factory=set)
    quantum_state: Optional[np.ndarray] = None  # complex vector for superposition
    entangled_with: Set[str] = field(default_factory=set)  # use set for uniqueness

    def interfere_with(self, other: 'Wave') -> float:
        """Calculate interference score combining normalized cosine similarity,
        phase coherence, frequency match, and optional quantum overlap.

        Returns a scalar score (can be negative for destructive interference).
        """
        # Ensure vectors are numpy arrays
        a = np.asarray(self.vector, dtype=float)
        b = np.asarray(other.vector, dtype=float)

        # cosine similarity (robust to zero-norm)
        na = safe_norm(a)
        nb = safe_norm(b)
        if na == 0 or nb == 0:
            cosine = 0.0
        else:
            cosine = float(np.dot(a, b) / (na * nb))

        # Phase coherence: cos of phase difference
        phase_diff = float(self.phase - other.phase)
        phase_coherence = math.cos(phase_diff)

        # Frequency similarity in (0, 1], higher if frequencies match
        freq_diff = abs(float(self.frequency) - float(other.frequency))
        freq_match = 1.0 / (1.0 + freq_diff)  # bounded (0,1]

        # Classical interference component
        classical_interference = cosine * phase_coherence * freq_match

        # Quantum overlap (if quantum_state present) — bounded [0, 1]
        quantum_interference = 0.0
        if (self.quantum_state is not None) and (other.quantum_state is not None):
            # ensure complex arrays
            qs1 = np.asarray(self.quantum_state, dtype=complex)
            qs2 = np.asarray(other.quantum_state, dtype=complex)
            # normalize if needed (avoid division by zero)
            n1 = safe_norm(qs1)
            n2 = safe_norm(qs2)
            if n1 > 0 and n2 > 0:
                qs1 = qs1 / n1
                qs2 = qs2 / n2
                overlap = np.vdot(qs1, qs2)  # complex inner product
                quantum_interference = float((abs(overlap))**2) * 0.5

        return float(classical_interference + quantum_interference)

    def apply_decay(self, decay_factor: float, rng: Optional[np.random.Generator] = None):
        """Apply temporal decay to amplitude and optional decoherence to quantum state.

        - decay_factor: typically in (0,1) to reduce amplitude.
        - rng: optional numpy.random.Generator for reproducibility.
        """
        # amplitude decay
        self.amplitude = float(self.amplitude * decay_factor)

        # quantum decoherence: small gaussian noise added, then renormalize
        if self.quantum_state is not None:
            if rng is None:
                rng = np.random.default_rng()
            noise = rng.normal(0.0, 0.01, self.quantum_state.shape) + 1j * rng.normal(0.0, 0.01, self.quantum_state.shape)
            qs = np.asarray(self.quantum_state, dtype=complex) + noise
            norm = safe_norm(qs)
            if norm == 0.0:
                # keep previous quantum state if new one degenerates
                return
            self.quantum_state = qs / norm

@dataclass
class WavePacket:
    """Collection of waves that travel together."""
    waves: List[Wave] = field(default_factory=list)
    group_velocity: float = 1.0
    dispersion: float = 0.0

    def propagate(self, time_step: float):
        """Propagate the wave packet through time.

        Updates phase for each wave according to its frequency, group velocity,
        and dispersion. Phase wrapped to [-pi, pi] for stability.
        """
        for wave in self.waves:
            # dispersion causes frequency-dependent phase shift scale
            delta = wave.frequency * time_step * (1.0 + self.dispersion * wave.frequency)
            wave.phase = float((wave.phase + delta) % (2 * math.pi))
            wave.timestamp = float(wave.timestamp + time_step)
