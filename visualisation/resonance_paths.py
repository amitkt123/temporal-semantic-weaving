from typing import List, Tuple
import matplotlib.pyplot as plt
from core.wave import Wave

class ResonancePathVisualizer:
    """Visualizes resonance paths and emergence patterns"""
    
    def __init__(self):
        self.graph = None
        self.resonance_pairs = []
        
    def plot_emergence_path(self, query: str, resonances: List[Tuple[Wave, float]]):
        """Plot the emergence path from query"""
        if not resonances:
            return
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (wave, strength) in enumerate(resonances):
            ax.scatter(i, strength, s=100*strength, alpha=0.6)
            ax.text(i, strength + 0.05, wave.source_text[:20], ha='center', fontsize=8)
        ax.set_xlabel('Resonance Index')
        ax.set_ylabel('Resonance Strength')
        ax.set_title(f'Emergence Path: {query[:50]}')
        plt.tight_layout()
        plt.show()
        
    def build_resonance_graph(self, waves: List[Wave], resonance_pairs: List[Tuple]):
        """Build graph structure for resonances"""
        self.resonance_pairs = resonance_pairs
        
    def plot_resonance_network(self):
        """Plot the resonance network"""
        if not self.resonance_pairs:
            print("No resonance pairs to visualize")
            return
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_title('Resonance Network')
        ax.text(0.5, 0.5, f'Network with {len(self.resonance_pairs)} connections', 
                ha='center', va='center')
        plt.tight_layout()
        plt.show()
