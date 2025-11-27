import numpy as np
from dataclasses import dataclass
from typing import Set, Optional, List
import uuid

@dataclass
class Wave:
    """Enhanced wave with quantum properties"""
    id: str
    vector: np.ndarray
    amplitude: float
    frequency: float
    phase: float
    timestamp: float
    source_text: str
    keywords: Set[str]
    quantum_state: Optional[np.ndarray] = None  # For superposition
    entangled_with: List[str] = None  # IDs of entangled waves
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.entangled_with is None:
            self.entangled_with = []
    
    def interfere_with(self, other: 'Wave') -> float:
        """Calculate quantum interference with another wave"""
        # Classical interference
        vector_similarity = np.dot(self.vector, other.vector)
        phase_diff = self.phase - other.phase
        freq_match = 1.0 / (1.0 + abs(self.frequency - other.frequency))
        
        classical_interference = vector_similarity * np.cos(phase_diff) * freq_match
        
        # Quantum interference if both have quantum states
        quantum_interference = 0
        if self.quantum_state is not None and other.quantum_state is not None:
            quantum_overlap = np.abs(np.vdot(self.quantum_state, other.quantum_state)) ** 2
            quantum_interference = quantum_overlap * 0.5
        
        return classical_interference + quantum_interference
    
    def apply_decay(self, decay_factor: float):
        """Apply temporal decay"""
        self.amplitude *= decay_factor
        
        # Quantum decoherence
        if self.quantum_state is not None:
            noise = np.random.normal(0, 0.01, self.quantum_state.shape)
            self.quantum_state += noise
            self.quantum_state /= np.linalg.norm(self.quantum_state)

@dataclass
class WavePacket:
    """Collection of waves that travel together"""
    waves: List[Wave]
    group_velocity: float
    dispersion: float
    
    def propagate(self, time_step: float):
        """Propagate the wave packet through time"""
        for wave in self.waves:
            # Dispersion causes different frequencies to travel at different speeds
            wave.phase += wave.frequency * time_step * (1 + self.dispersion * wave.frequency)