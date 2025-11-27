import numpy as np
from typing import Optional
from core.wave import Wave

class HolographicMemory:
    """Holographic memory system (robust, toy-model).
    
    - Stores each Wave as a complex outer-product pattern in a size x size hologram.
    - Uses FFT-based projection to map arbitrary-length vectors into the hologram frame.
    - Provides reconstruct() to read out the hologram and probe() to score a query vector.
    """

    def __init__(self, size: int = 128):
        self.size = int(size)
        # complex hologram matrix
        self.hologram = np.zeros((self.size, self.size), dtype=np.complex128)
        # optional counter for items stored
        self._count = 0

    # -------------------------
    #  Internal helpers
    # -------------------------
    def _project_to_frame(self, vec: np.ndarray) -> np.ndarray:
        """Project / compress an arbitrary-length real vector into a complex frame of length `size`.

        Strategy:
        - Use FFT to capture spectral content, then take the first `size` complex coefficients.
        - If vec is shorter, pad; if longer, FFT compresses.
        - Normalize resulting projected vector to unit norm (if possible).
        """
        v = np.asarray(vec, dtype=float)
        if v.size == 0:
            return np.zeros(self.size, dtype=np.complex128)

        # zero-pad to power-of-two for nice FFT behaviour (optional)
        # But here we simply compute FFT and take leading 'size' bins (wrap if necessary).
        fftv = np.fft.fft(v)
        # take first `size` bins (wrap if needed)
        if fftv.size >= self.size:
            proj = fftv[:self.size]
        else:
            # pad with zeros in frequency domain
            proj = np.zeros(self.size, dtype=complex)
            proj[:fftv.size] = fftv

        # convert to complex128 and normalize
        proj = np.asarray(proj, dtype=np.complex128)
        norm = np.linalg.norm(proj)
        if norm > 0:
            proj = proj / norm
        return proj

    # -------------------------
    #  Public API
    # -------------------------
    def add_to_hologram(self, wave: Wave, strength: Optional[float] = None):
        """Add a wave into the hologram.

        - Projects wave.vector into the holographic frame.
        - Creates a rank-1 complex pattern = outer(proj, conj(proj)).
        - Adds wave.amplitude * exp(1j*phase) * pattern to hologram.
        """
        vec = getattr(wave, "vector", None)
        if vec is None:
            raise ValueError("Wave must have a .vector to store in hologram")

        proj = self._project_to_frame(vec)                # complex vector length = size
        phase = float(getattr(wave, "phase", 0.0))
        amp = float(strength) if strength is not None else float(getattr(wave, "amplitude", 1.0))
        pattern = np.outer(proj, np.conjugate(proj))     # size x size complex
        factor = amp * np.exp(1j * phase)
        self.hologram += factor * pattern
        self._count += 1

    def reconstruct(self, damage_mask: Optional[np.ndarray] = None) -> np.ndarray:
        """Return a real-valued reconstruction map of the hologram.

        If `damage_mask` is supplied, it must be same shape as hologram and will be applied multiplicatively.
        The returned array is the magnitude (abs) of the inverse-frequency-style reconstruction
        (we invert the rank-1 patterns via a simple 2D IFFT pipeline for visualization).
        """
        H = self.hologram.copy()
        if damage_mask is not None:
            if damage_mask.shape != H.shape:
                raise ValueError("damage_mask must match hologram shape")
            H = H * damage_mask

        # simple readout: apply 2D inverse FFT and return magnitude
        # (this is a toy readout — for more advanced retrieval use correlation/probe())
        try:
            # transform to spatial domain and take abs
            recon = np.fft.ifft2(H)
            recon_mag = np.abs(recon)
        except Exception:
            # fallback: return abs of hologram directly
            recon_mag = np.abs(H)
        return recon_mag

    def probe(self, query_vector: np.ndarray) -> float:
        """Probe the hologram with a query vector and return a similarity score (scalar).

        - Project query into frame, form its pattern, correlate with hologram (Frobenius inner product).
        - Returns a real scalar: higher means stronger activation.
        """
        qproj = self._project_to_frame(query_vector)
        qpattern = np.outer(qproj, np.conjugate(qproj))
        # Frobenius inner product (real part)
        score = np.real(np.vdot(self.hologram.flatten(), qpattern.flatten()))
        return float(score)

    def clear(self):
        """Reset hologram"""
        self.hologram.fill(0)
        self._count = 0

    def stored_count(self) -> int:
        return int(self._count)
