import numpy as np
from typing import List, Tuple
from core.wave import Wave

class QuantumSuperposition:
    """Stable and physically-correct superposition & collapse."""

    # --------------------------------------------------------
    #  SUPERPOSITION
    # --------------------------------------------------------
    def create_superposition(self, waves: List[Wave]) -> np.ndarray:
        """Amplitude-weighted, dimension-safe superposition."""
        if not waves:
            return np.array([], dtype=complex)

        # Determine a canonical dimensionality
        # (use largest quantum_state length among waves)
        max_dim = max(
            (len(w.quantum_state) for w in waves if w.quantum_state is not None),
            default=0
        )
        if max_dim == 0:
            return np.array([], dtype=complex)

        combined = np.zeros(max_dim, dtype=complex)

        for w in waves:
            qs = w.quantum_state
            if qs is None:
                continue

            # pad or trim to match max_dim
            if len(qs) < max_dim:
                padded = np.zeros(max_dim, dtype=complex)
                padded[:len(qs)] = qs
                qs = padded
            elif len(qs) > max_dim:
                qs = qs[:max_dim]

            # amplitude-weighted summation
            # (phase of w.phase incorporated here)
            phase_factor = np.exp(1j * w.phase)
            combined += w.amplitude * phase_factor * qs

        # normalize to unit norm
        norm = np.linalg.norm(combined)
        if norm > 0:
            combined = combined / norm

        return combined

    # --------------------------------------------------------
    #  COLLAPSE
    # --------------------------------------------------------
    def collapse_wavefunction(
        self,
        superposition: np.ndarray,
        measurement_vector: np.ndarray
    ) -> Tuple[np.ndarray, float]:
        """Perform Lüders-rule measurement collapse.

        Uses projector: P = |m><m|
        New state: (Pψ) / sqrt(<ψ|P|ψ>)
        Probability: |<m|ψ>|^2
        """

        ψ = np.asarray(superposition, dtype=complex)
        m = np.asarray(measurement_vector, dtype=complex)

        # Make dimensions consistent
        dim = min(len(ψ), len(m))
        ψ = ψ[:dim]
        m = m[:dim]

        # Normalize measurement vector
        m_norm = np.linalg.norm(m)
        if m_norm == 0:
            raise ValueError("Measurement vector cannot be zero-norm.")
        m = m / m_norm

        # Probability of collapse into |m⟩
        overlap = np.vdot(m, ψ)      # complex amplitude
        probability = float(np.abs(overlap)**2)

        # Collapse state = m (since projector only keeps |m⟩ component)
        collapsed = m.copy()

        return collapsed, probability
