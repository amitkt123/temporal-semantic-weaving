try:
    from .wave import Wave, WavePacket
    from .resonance_field import ResonanceField
    from .embeddings import EmbeddingEngine
    
    __all__ = ['Wave', 'WavePacket', 'ResonanceField', 'EmbeddingEngine']
except ImportError as e:
    print(f"Error in core/__init__.py: {e}")
    import traceback
    traceback.print_exc()
    raise