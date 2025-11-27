import numpy as np
from typing import Optional
from core.wave import Wave

class HolographicMemory:
    """Holographic memory system for distributed storage"""
    
    def __init__(self, size: int = 100):
        self.hologram = np.zeros((size, size), dtype=complex)
        self.size = size
        
    def add_to_hologram(self, wave: Wave):
        """Add wave to holographic memory"""
        idx_x = int(np.abs(np.sum(wave.vector[:50])) * self.size) % self.size
        idx_y = int(np.abs(np.sum(wave.vector[50:100])) * self.size) % self.size
        self.hologram[idx_x, idx_y] += wave.amplitude * np.exp(1j * wave.phase)
        
    def reconstruct(self, damage_mask: Optional[np.ndarray] = None) -> np.ndarray:
        """Reconstruct memory from (possibly damaged) hologram"""
        if damage_mask is None:
            return np.abs(self.hologram)
        damaged = self.hologram * damage_mask
        fft_damaged = np.fft.fft2(damaged)
        reconstructed = np.abs(np.fft.ifft2(fft_damaged))
        return reconstructed
