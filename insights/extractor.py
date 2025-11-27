from typing import Dict, Any
from core.resonance_field import ResonanceField

class InsightExtractor:
    """Extracts insights from resonance field patterns"""
    
    def __init__(self, field: ResonanceField):
        self.field = field
        
    def extract_insight(self, question: str) -> Dict[str, Any]:
        """Extract insight based on field state and question"""
        resonances = self.field.find_resonances(question)
        
        if not resonances:
            return {
                'insight': 'No patterns found yet.',
                'confidence': 0.0,
                'evidence': []
            }
        
        confidence = min(1.0, len(resonances) * 0.3)
        evidence = [f"{r[0].source_text[:50]}" for r in resonances[:3]]
        
        return {
            'insight': f'Found {len(resonances)} resonating patterns in your experience.',
            'confidence': confidence,
            'evidence': evidence
        }
