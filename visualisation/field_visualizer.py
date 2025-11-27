import matplotlib.pyplot as plt
import numpy as np
from core.resonance_field import ResonanceField

class FieldVisualizer:
    """Visualizes the complete field state"""
    
    def plot_complete_field_state(self, field: ResonanceField):
        """Plot comprehensive visualization of field"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes[0, 0].imshow(np.abs(field.field_tensor), cmap='viridis')
        axes[0, 0].set_title('Field Tensor')
        if field.waves:
            amplitudes = [w.amplitude for w in field.waves]
            axes[0, 1].plot(amplitudes, marker='o')
            axes[0, 1].set_title('Wave Amplitudes Over Time')
        if field.waves:
            frequencies = [w.frequency for w in field.waves]
            axes[1, 0].hist(frequencies, bins=10, edgecolor='black')
            axes[1, 0].set_title('Frequency Distribution')
        if field.waves:
            energies = [field.get_field_energy() for _ in range(len(field.waves))]
            axes[1, 1].plot(energies)
            axes[1, 1].set_title('Field Energy Evolution')
        plt.tight_layout()
        plt.show()
