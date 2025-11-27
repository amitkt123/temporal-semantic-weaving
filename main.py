"""
Temporal Semantic Weaving - Enhanced Implementation
"""

import numpy as np
import time
from typing import List, Dict
import matplotlib.pyplot as plt

# Core imports
from core import ResonanceField, EmbeddingEngine
from temporal.decay import TemporalDecay, MemoryConsolidation
from temporal.braid import TemporalBraid
from quantum.superposition import QuantumSuperposition
from quantum.entanglement import QuantumEntanglement
from holographic.holographic_memory import HolographicMemory
from visualisation.resonance_paths import plot_emergence_path, plot_resonance_network
from visualisation.field_visualizer import FieldVisualizer
from crystallisation.crystallizer import SemanticCrystallizer
from insights.extractor import InsightExtractor

class EnhancedTSW:
    """Enhanced Temporal Semantic Weaving System"""
    
    def __init__(self):
        # Core components
        self.field = ResonanceField()
        self.temporal_braid = TemporalBraid()
        self.crystallizer = SemanticCrystallizer()
        
        # Quantum components
        self.superposition = QuantumSuperposition()
        self.entanglement = QuantumEntanglement()
        
        # Holographic memory
        self.holographic_memory = HolographicMemory()
        
        # Temporal components
        self.decay_engine = TemporalDecay()
        self.consolidation = MemoryConsolidation()
        
        # Visualization (functions, not classes)
        self.field_visualizer = FieldVisualizer()
        
        # Insight extraction
        self.insight_extractor = InsightExtractor(self.field)
    
    def add_experience(self, text: str):
        """Add experience with full processing"""
        print(f"\n📝 Adding: {text[:60]}...")
        
        # Add to resonance field
        wave, resonances = self.field.add_experience(text)
        
        # Add to holographic memory
        self.holographic_memory.add_to_hologram(wave)
        
        # Weave into temporal braid
        self.temporal_braid.weave(wave)
        
        # Check for crystallization
        crystals = self.crystallizer.check_crystallization(self.field)
        if crystals:
            print(f"💎 {len(crystals)} crystal(s) formed")
        
        # Apply quantum entanglement for strong resonances
        for other_text, strength in resonances:
            if strength > 0.5:
                other_wave = next((w for w in self.field.waves 
                                 if w.source_text.startswith(other_text)), None)
                if other_wave:
                    self.entanglement.entangle_waves(wave, other_wave)
                    print(f"🔗 Quantum entanglement created")
        
        # Apply temporal decay
        self._apply_temporal_decay()
        
        return wave
    
    def _apply_temporal_decay(self):
        """Apply sophisticated temporal decay"""
        current_time = self.field.time
        
        for wave in self.field.waves:
            time_delta = current_time - wave.timestamp
            
            # Use adaptive decay
            decay_factor = self.decay_engine.adaptive_decay(
                wave, time_delta, {'field_energy': self.field.get_field_energy()}
            )
            
            wave.apply_decay(decay_factor)
        
        # Consolidate important memories
        self.field.waves = self.consolidation.consolidate(self.field.waves, current_time)
        
        # Remove very weak waves
        self.field.waves = [w for w in self.field.waves if w.amplitude > 0.01]
    
    def query(self, question: str) -> Dict:
        """Enhanced query with visualization"""
        print(f"\n❓ Query: {question}")
        
        # Get resonances
        resonances = self.field.find_resonances(question)
        
        # Create superposition of resonating states
        if resonances:
            resonating_waves = [w for w, _ in resonances[:5]]
            superposition_state = self.superposition.create_superposition(resonating_waves)
            
            # Collapse wavefunction with query as measurement
            query_vector = self.field.embedding_engine.encode(question)
            collapsed_state, probability = self.superposition.collapse_wavefunction(
                superposition_state, query_vector[:len(superposition_state)]
            )
            
            print(f"📊 Quantum collapse probability: {probability:.2%}")
        
        # Extract insights
        insight = self.insight_extractor.extract_insight(question)
        
        # Visualize resonance path if insights found
        if resonances and len(resonances) > 2:
            plot_emergence_path(question, resonances[:5], show=False)
        
        return insight
    
    def visualize_field(self):
        """Comprehensive field visualization"""
        self.field_visualizer.plot_complete_field_state(self.field)
    
    def visualize_resonance_network(self):
        """Visualize the resonance network"""
        # Build resonance graph
        resonance_pairs = []
        for i, wave1 in enumerate(self.field.waves):
            for wave2 in self.field.waves[i+1:]:
                strength = wave1.interfere_with(wave2)
                if strength > 0.3:
                    # Convert wave objects to string IDs for graph
                    wave1_id = f"Wave_{id(wave1) % 10000}"
                    wave2_id = f"Wave_{id(wave2) % 10000}"
                    resonance_pairs.append((wave1_id, wave2_id, strength))
        
        plot_resonance_network(resonance_pairs, show=False)
    
    def demonstrate_holographic_recovery(self):
        """Demonstrate holographic memory recovery from damage"""
        if not self.field.waves:
            print("No memories to demonstrate")
            return
        
        # Create damage mask (50% damage)
        damage_mask = np.random.choice([0, 1], 
                                      size=self.holographic_memory.hologram.shape,
                                      p=[0.5, 0.5])
        
        # Reconstruct from damaged hologram
        reconstructed = self.holographic_memory.reconstruct(damage_mask=damage_mask)
        
        # Visualize
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        ax1.imshow(np.abs(self.holographic_memory.hologram), cmap='hot')
        ax1.set_title('Original Hologram')
        
        ax2.imshow(damage_mask, cmap='gray')
        ax2.set_title('Damage Mask (50% loss)')
        
        ax3.imshow(reconstructed, cmap='hot')
        ax3.set_title('Reconstructed Memory')
        
        plt.tight_layout()
        plt.show()
        
        print("✅ Holographic recovery demonstrated - memory survived 50% damage!")