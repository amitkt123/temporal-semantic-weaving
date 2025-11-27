# Temporal Semantic Weaving (TSW) - Enhanced Codebase Analysis

## System Overview

The Enhanced Temporal Semantic Weaving system is a sophisticated framework that models human memory, semantic connections, and pattern recognition using quantum mechanics concepts and graph theory. It treats experiences as waves in a semantic field that can interfere, resonate, and crystallize into insights.

---

## Architecture

### Core Layer: `core/`

#### **ResonanceField** (The Brain's Main Processing Unit)
- **Purpose**: Central data structure managing all "waves" (memories/experiences)
- **Key Properties**:
  - `waves`: List of all experiences stored as Wave objects
  - `field_tensor`: 384x384 complex matrix representing semantic field
  - `embedding_engine`: Converts text to semantic vectors
  - `coupling_constant`: Controls how strongly waves affect each other

**How it works**:
1. When you add an experience via `add_experience(text)`:
   - Converts text to semantic vector (384-dimensional)
   - Extracts keywords using NLP
   - Calculates frequency based on semantic importance
   - Creates quantum superposition state
   - Checks for interference with existing waves

**Example Flow**:
```
Text: "Met Sarah for coffee"
   ↓
Embedding: [0.12, -0.45, 0.78, ...] (384 dimensions)
   ↓
Keywords: {'sarah', 'coffee', 'meeting'}
   ↓
Frequency: 3.5 (higher for 'sarah' = 5.0)
   ↓
Wave created and added to field
   ↓
Interference checked with all existing waves
```

#### **Wave** (Individual Memory Unit)
- **Properties**:
  - `vector`: Semantic embedding (384D)
  - `amplitude`: Strength/importance of the memory
  - `frequency`: Semantic frequency (coffee=2.0, sarah=5.0, etc.)
  - `phase`: Temporal position in the field
  - `quantum_state`: Complex superposition state
  - `entangled_with`: List of IDs of related memories

#### **EmbeddingEngine** (Semantic Encoder)
- Uses sentence-transformers for semantic understanding
- Extracts keywords related to life patterns: coffee, guitar, career, sarah, tom, etc.
- Falls back to character trigrams if transformer unavailable

---

### Quantum Layer: `quantum/`

#### **QuantumSuperposition**
- Creates superposition states by combining multiple waves
- `collapse_wavefunction()`: Simulates quantum measurement where a query "measures" the field
- **Demo Output**: "📊 Quantum collapse probability: 6.55%"
  - This is the probability that the superposition collapses to match the query

#### **QuantumEntanglement**
- Creates entanglement links between waves with strong resonance (>0.5 interference)
- Entangled memories are bonded - affecting one affects the other
- **Demo Output**: "🔗 Quantum entanglement created"
  - Shows when 2+ waves with related keywords are discovered

---

### Temporal Layer: `temporal/`

#### **TemporalDecay**
- Simulates memory fading over time
- Types:
  - `exponential_decay`: Memories fade like radioactive decay
  - `power_law_decay`: Slower, more realistic memory decay
  - `adaptive_decay`: Important memories (with keywords/entanglements) decay slower

#### **MemoryConsolidation**
- Long-term memories are "replayed" and strengthened
- Important patterns (age > 10 steps + amplitude > 0.8) get boosted
- Reduces quantum decoherence in established memories

#### **TemporalBraid**
- Weaves waves together chronologically
- Detects causal loops: "A → B → C → A"
- Identifies repeating temporal patterns

---

### Analysis Layer: `crystallisation/`

#### **SemanticCrystallizer**
- Forms "memory crystals" when patterns stabilize
- **Process**:
  1. Groups waves by keyword overlap
  2. Checks cluster stability (average amplitude)
  3. If stable (>0.7), crystallizes into persistent insight
- **Demo Output**: "💎 1 crystal(s) formed"
  - Represents stable semantic patterns like "coffee + sarah connection"

---

### Insight Layer: `insights/`

#### **InsightExtractor**
- Analyzes resonance field to answer queries
- Finds resonating memories (related to query)
- Aggregates evidence from resonances
- Returns: `{'insight': str, 'confidence': float, 'evidence': [...]}`
- **Confidence Calculation**: `min(1.0, len(resonances) * 0.3)`
  - 2 resonances → 60% confidence
  - 3+ resonances → 90%+ confidence

---

### Memory Layer: `holographic/`

#### **HolographicMemory**
- Distributed holographic storage inspired by Penrose-Hameroff theory
- Memories stored in complex fourier space
- **Key Feature**: Survives 50% damage (holographic redundancy)
- Can reconstruct damaged memories via FFT:
  - Apply damage mask
  - FFT (frequency domain)
  - IFFT (reconstruct)

---

### Visualization Layer: `visualisation/`

#### **FieldVisualizer**
- Plots field state across 9 subplots
- Shows: tensor heatmap, amplitudes, frequencies, phases, energy

#### **ResonancePathVisualizer**
- Network graph of resonance connections
- Spring layout positions similar concepts nearby
- Edge thickness = resonance strength

---

## Demo Output Explained

```
📚 Loading experiences with enhanced processing...

📝 Adding: Met Sarah for coffee, she got promoted...
  ↓ Experience added, checking interference with existing waves

🔗 Quantum entanglement created
  ↓ Strong resonance (>0.5) found with existing waves
  ↓ Keywords overlap: sarah + coffee already connected

💎 1 crystal(s) formed
  ↓ Cluster of semantically similar experiences reached stability
  ↓ Pattern crystallized into stable memory structure

🔗 Quantum entanglement: 16
  ↓ Total entanglement links across all waves
  ↓ Shows how interconnected the memory network is
```

---

## Demo Query Example

```
❓ Query: Why do I keep meeting Sarah?

📊 Quantum collapse probability: 6.55%
  ↓ Superposition of all waves collapses to match query
  ↓ Probability it hits correct response space

💡 Insight: Found 2 resonating patterns in your experience.
📈 Confidence: 60.00%
  ↓ 2 resonances × 0.3 = 0.60 (60%)
  ↓ Patterns: "Sarah + coffee" and "Sarah + guitar"
```

---

## Key Metrics in Output

| Metric | Meaning | Example |
|--------|---------|---------|
| **Quantum collapse probability** | How well query matches wave superposition | 6.55% = weak match |
| **Confidence** | Reliability of insight (# resonances × 0.3) | 60% = moderate |
| **Field energy** | Total activity: kinetic + potential + vacuum | ≈ 0.50 |
| **Active waves** | Number of experiences in memory | 13 |
| **Quantum entanglements** | Links between related memories | 16 |
| **Crystals formed** | Stable semantic patterns | 1 |
| **Average amplitude** | Memory strength (fades over time) | 0.782 |

---

## Data Flow Diagram

```
Text Input
   ↓
EmbeddingEngine (384D vector + keywords)
   ↓
Wave Creation (vector, frequency, phase, quantum_state)
   ↓
Interference Analysis (compare with existing waves)
   ↓
[Strong resonance?] → QuantumEntanglement ← [Yes]
   ↓
Field Tensor Update (complex matrix)
   ↓
Crystallization Check (pattern detection)
   ↓
Stored in ResonanceField.waves[]
   ↓
Query: Find Resonances → Collapse Wavefunction → Extract Insight
```

---

## Semantic Frequency Map

```python
'coffee': 2.0      # Morning ritual concept
'morning': 2.5     # Time-related
'guitar': 3.0      # Hobby concept
'practice': 3.2    # Action concept
'chords': 3.5      # Music detail
'career': 4.0      # Life goal
'sarah': 5.0       # Person (highest - most important)
'friend': 5.2      # Relationship
```

Higher frequency = more semantically important = slower decay

---

## Interference Mechanism

When new wave meets existing wave:

```
interference_strength = dot_product(vectors) × cos(phase_diff) × freq_match
  ↓
+ keyword_overlap_bonus (0.2 per shared keyword)
  ↓
If interference > 0.5: Create quantum entanglement
If interference > 0.1: Amplify both waves (constructive)
If interference < -0.2: Dampen (destructive)
```

**Example**: "Sarah helped me with guitar" meets existing "Sarah coffee meeting"
- Vector similarity: high (both about sarah)
- Phase match: good (same semantic domain)
- Keyword overlap: high (sarah + practice)
- Result: Strong entanglement created

---

## Phase Transition & Crystallization

Memory experiences undergo phase transitions:

```
Gas Phase: Individual memories (no pattern)
   ↓ (accumulation)
Liquid Phase: Resonances form connections
   ↓ (pattern strengthens)
Solid Phase: Crystallized insight (stable memory)
```

**Trigger**: Cluster stability > 0.7 (average amplitude of grouped memories)

---

## Quantum Collapse in Queries

When you ask "Why do I keep meeting Sarah?":

1. **Query wave created**: Same process as experience (embedding + keywords)
2. **Superposition created**: All relevant waves combined into superposition
3. **Measurement**: Query vector acts as measurement basis
4. **Collapse**: Probability = |⟨query | superposition⟩|²
5. **Insight extraction**: Resonances ranked by overlap × amplitude × entanglement

---

## Summary

The system models memory as:
- **Semantic field**: 384D embedding space where similar ideas cluster
- **Interference patterns**: How memories affect each other
- **Quantum properties**: Entanglement (linked memories), superposition (combined concepts)
- **Temporal dynamics**: Decay, consolidation, causal patterns
- **Phase transitions**: Individual → connected → crystallized
- **Emergent insights**: Patterns that arise from the field dynamics

**Result**: A sophisticated memory system that finds hidden patterns, ranks confidence, and treats memories as interconnected quantum phenomena rather than isolated data points.
