import numpy as np
from typing import List, Tuple, Dict, Optional, Set
from .wave import Wave, WavePacket
from .embeddings import EmbeddingEngine

class ResonanceField:
    """Enhanced resonance field with quantum properties"""
    
    def __init__(self, dimensions: int = 384):
        self.dimensions = dimensions
        self.waves: List[Wave] = []
        self.field_tensor = np.zeros((dimensions, dimensions), dtype=complex)
        self.time = 0
        self.embedding_engine = EmbeddingEngine()
        
        # Quantum field properties
        self.vacuum_energy = 0.01
        self.coupling_constant = 0.1
        
    def add_experience(self, text: str) -> Tuple[Wave, List[Tuple[str, float]]]:
        """Add experience to field and return wave with resonances"""
        # Create wave from text
        wave = self._create_wave(text)
        
        # Find and apply interference
        resonances = self._apply_interference(wave)
        
        # Add to field
        self.waves.append(wave)
        
        # Update field tensor
        self._update_field_tensor(wave)
        
        # Increment time
        self.time += 1
        
        return wave, resonances
    
    def _create_wave(self, text: str) -> Wave:
        """Create enhanced wave from text"""
        vector = self.embedding_engine.encode(text)
        keywords = self.embedding_engine.extract_keywords(text)
        
        # Calculate frequency from semantic content
        frequency = self._calculate_frequency(keywords)
        
        # Phase based on current field time
        phase = (self.time * 0.1) % (2 * np.pi)
        
        # Create quantum state (superposition)
        quantum_state = self._create_quantum_state(vector)
        
        return Wave(
            id=None,  # Will be auto-generated
            vector=vector,
            amplitude=1.0,
            frequency=frequency,
            phase=phase,
            timestamp=self.time,
            source_text=text,
            keywords=keywords,
            quantum_state=quantum_state
        )
    
    def _calculate_frequency(self, keywords: Set[str]) -> float:
        """Calculate semantic frequency from keywords"""
        if not keywords:
            return 1.0
        
        # Different concepts have different frequencies
        freq_map = {
            'coffee': 2.0, 'morning': 2.5, 'ritual': 2.3,
            'guitar': 3.0, 'practice': 3.2, 'chords': 3.5,
            'career': 4.0, 'promotion': 4.2, 'work': 4.1,
            'sarah': 5.0, 'friend': 5.2, 'help': 5.1
        }
        
        frequencies = [freq_map.get(k, 1.0) for k in keywords]
        return np.mean(frequencies) if frequencies else 1.0
    
    def _create_quantum_state(self, vector: np.ndarray) -> np.ndarray:
        """Create quantum superposition state"""
        # Create complex quantum state
        real_part = vector[:min(100, len(vector))]
        imag_part = np.roll(vector[:min(100, len(vector))], len(vector)//4)
        
        quantum_state = real_part + 1j * imag_part * 0.5
        quantum_state = quantum_state / np.linalg.norm(quantum_state)
        
        return quantum_state
    
    def _apply_interference(self, new_wave: Wave) -> List[Tuple[str, float]]:
        """Apply interference and return resonances"""
        resonances = []
        
        for existing_wave in self.waves:
            interference = new_wave.interfere_with(existing_wave)
            
            # Keyword overlap bonus
            keyword_overlap = len(new_wave.keywords & existing_wave.keywords)
            if keyword_overlap > 0:
                interference += keyword_overlap * 0.2
            
            if interference > 0.1:
                # Constructive interference
                existing_wave.amplitude *= (1 + self.coupling_constant * interference)
                new_wave.amplitude *= (1 + self.coupling_constant * interference * 0.5)
                
                # Quantum entanglement for strong resonance
                if interference > 0.5:
                    new_wave.entangled_with.append(existing_wave.id)
                    existing_wave.entangled_with.append(new_wave.id)
                
                resonances.append((existing_wave.source_text[:30], interference))
            elif interference < -0.2:
                # Destructive interference
                existing_wave.amplitude *= (1 - self.coupling_constant * abs(interference))
        
        return sorted(resonances, key=lambda x: x[1], reverse=True)[:3]
    
    def _update_field_tensor(self, wave: Wave):
        """Update complex field tensor"""
        # Add wave pattern to field (now complex)
        wave_pattern = np.outer(wave.vector, wave.vector)
        
        # Add quantum phase information
        phase_factor = np.exp(1j * wave.phase)
        self.field_tensor += wave.amplitude * wave_pattern * phase_factor
        
        # Normalize to prevent explosion
        max_val = np.max(np.abs(self.field_tensor))
        if max_val > 10:
            self.field_tensor /= (max_val / 10)
    
    def find_resonances(self, query_text: str) -> List[Tuple[Wave, float]]:
        """Find quantum resonances with query"""
        query_wave = self._create_wave(query_text)
        resonances = []
        
        for wave in self.waves:
            # Calculate quantum resonance
            resonance_strength = query_wave.interfere_with(wave)
            
            # Entanglement bonus
            if wave.entangled_with:
                entanglement_bonus = 0.1 * len(wave.entangled_with)
                resonance_strength += entanglement_bonus
            
            # Amplitude weighting
            weighted_strength = resonance_strength * wave.amplitude
            
            if weighted_strength > 0.05:
                resonances.append((wave, weighted_strength))
        
        return sorted(resonances, key=lambda x: x[1], reverse=True)
    
    def get_field_energy(self) -> float:
        """Calculate total field energy"""
        kinetic = sum(w.amplitude ** 2 * w.frequency for w in self.waves)
        potential = np.sum(np.abs(self.field_tensor) ** 2)
        vacuum = self.vacuum_energy * len(self.waves)
        
        return kinetic + potential + vacuum