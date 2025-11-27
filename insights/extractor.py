from typing import Dict, Any, List
from core.resonance_field import ResonanceField

class InsightExtractor:
    """Extracts meaningful insights or answers from resonance field patterns."""

    def __init__(self, field: ResonanceField, llm=None):
        """
        field: ResonanceField instance
        llm: optional callable like llm(prompt) -> str
        """
        self.field = field
        self.llm = llm

    # ---------------------------------------------
    # PUBLIC API
    # ---------------------------------------------
    def extract_insight(self, question: str, top_k: int = 5, use_llm: bool = False) -> Dict[str, Any]:
        """Extract meaningful insight or an actual answer."""
        resonances = self.field.find_resonances(question, top_k=top_k)

        if not resonances:
            return self._no_insight()

        # Unpack: each element = (wave, score)
        waves, scores = zip(*resonances)

        # Confidence derived from max similarity (0..1 scaled)
        confidence = self._compute_confidence(scores)

        # Evidence: top selected segments with scores
        evidence = self._format_evidence(waves, scores)

        # If LLM available, produce a real answer
        if use_llm and self.llm is not None:
            answer = self._synthesize_answer_llm(question, evidence)
        else:
            answer = self._synthesize_answer_fallback(question, evidence)

        return {
            "question": question,
            "answer": answer,
            "confidence": confidence,
            "top_resonances": len(waves),
            "evidence": evidence,
        }

    # ---------------------------------------------
    # INTERNAL HELPERS
    # ---------------------------------------------
    def _no_insight(self) -> Dict[str, Any]:
        return {
            "answer": "I couldn't find any relevant patterns in memory yet.",
            "confidence": 0.0,
            "evidence": []
        }

    def _compute_confidence(self, scores: List[float]) -> float:
        """Use max similarity, scaled into [0, 1]."""
        max_sim = max(scores)
        # cosine similarity can be [-1..1] -> scale into [0..1]
        conf = (max_sim + 1.0) / 2.0
        return float(max(0.0, min(1.0, conf)))

    def _format_evidence(self, waves, scores):
        """Return structured evidence sorted by relevance."""
        ev = []
        for w, s in zip(waves, scores):
            snippet = w.source_text.strip().replace("\n", " ")
            ev.append({
                "wave_id": w.id,
                "similarity": float(s),
                "text": snippet[:240]  # short snippet
            })
        return ev

    def _synthesize_answer_fallback(self, question: str, evidence: List[Dict[str, Any]]) -> str:
        """
        A non-LLM summarizer: extracts answer by picking the highest scoring snippet.
        """
        if not evidence:
            return "No relevant information available."

        best = evidence[0]
        return f"Based on the strongest memory pattern: '{best['text']}'."

    def _synthesize_answer_llm(self, question: str, evidence: List[Dict[str, Any]]) -> str:
        """LLM-enabled summarization."""
        chunks = "\n\n".join([f"[Evidence]: {e['text']}" for e in evidence])

        prompt = (
            f"Question: {question}\n"
            f"Relevant evidence from memory:\n{chunks}\n\n"
            f"Based only on the evidence above, answer clearly and concisely:"
        )

        return self.llm(prompt)
