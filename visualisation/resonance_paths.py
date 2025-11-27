# improved_visualizers.py
import math
from typing import List, Tuple, Optional
import matplotlib.pyplot as plt
from core.wave import Wave
import numpy as np

# networkx is optional; fallback gracefully if not available
try:
    import networkx as nx
    _HAS_NX = True
except Exception:
    _HAS_NX = False


def _clamp01(x):
    return max(0.0, min(1.0, float(x)))


def plot_emergence_path(
    query: str,
    resonances: List[Tuple[Wave, float]],
    top_n: Optional[int] = None,
    save_path: Optional[str] = None,
    show: bool = True
):
    """Plot a clearer emergence path for a query.

    - resonances: list of (Wave, strength) sorted by relevance (desc).
    - top_n: if set, show only the first N resonances.
    - save_path: if given, save the figure to disk.
    - returns: matplotlib.figure.Figure
    """
    if not resonances:
        fig = plt.figure()
        plt.text(0.5, 0.5, "No resonances", ha="center", va="center")
        if save_path:
            plt.savefig(save_path, bbox_inches="tight")
        if show:
            plt.show()
        return fig

    if top_n is not None:
        resonances = resonances[:top_n]

    strengths = [r[1] for r in resonances]
    # normalize strengths to 0..1 for consistent sizing
    s_min, s_max = min(strengths), max(strengths)
    if s_max > s_min:
        strengths_norm = [(s - s_min) / (s_max - s_min) for s in strengths]
    else:
        strengths_norm = [0.5 for _ in strengths]

    # map normalized strengths to marker sizes (avoid extremes)
    marker_sizes = [50 + 300 * s for s in strengths_norm]  # between 50..350

    fig, ax = plt.subplots(figsize=(10, 6))
    xs = list(range(len(resonances)))
    ys = [max(0.0, float(r[1])) for r in resonances]  # clamp negative strengths

    scatter = ax.scatter(xs, ys, s=marker_sizes, alpha=0.7, edgecolors="k", linewidths=0.3)

    # label each point with a short snippet, avoid overlap by small vertical offset
    for i, (wave, raw_strength) in enumerate(resonances):
        label = wave.source_text.strip().replace("\n", " ")
        short = (label[:60] + "...") if len(label) > 63 else label
        ax.text(i, ys[i] + 0.02 * (max(1.0, max(ys) - min(ys) + 1e-6)), short, ha="center", va="bottom", fontsize=8, rotation=25)

    ax.set_xlabel("Resonance Index")
    ax.set_ylabel("Resonance Strength (raw)")
    title = f"Emergence Path: {query[:80]}" if query else "Emergence Path"
    ax.set_title(title)
    ax.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, bbox_inches="tight")

    if show:
        plt.show()
    return fig


def plot_resonance_network(
    resonance_pairs: List[Tuple[str, str, float]],
    node_labels: Optional[dict] = None,
    save_path: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 8),
    show: bool = True
):
    """Plot the resonance network.

    - resonance_pairs: list of (source_id, target_id, weight) where weight is numeric strength.
    - node_labels: optional dict mapping node_id -> short label for display.
    - returns: matplotlib.figure.Figure
    """
    if not resonance_pairs:
        fig = plt.figure(figsize=figsize)
        plt.text(0.5, 0.5, "No resonance pairs to visualize", ha="center", va="center")
        if save_path:
            plt.savefig(save_path, bbox_inches="tight")
        if show:
            plt.show()
        return fig

    if not _HAS_NX:
        # simple fallback: textual summary plot
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
        ax.axis("off")
        ax.text(0.01, 0.99, "networkx not installed; resonance pairs:", va="top")
        y = 0.92
        for a, b, w in resonance_pairs:
            ax.text(0.01, y, f"{a} -- {b} (w={w:.3f})", fontsize=8, family="monospace")
            y -= 0.03
            if y < 0.02:
                break
        if save_path:
            fig.savefig(save_path, bbox_inches="tight")
        if show:
            plt.show()
        return fig

    # Build graph
    G = nx.Graph()
    for a, b, w in resonance_pairs:
        G.add_node(a)
        G.add_node(b)
        G.add_edge(a, b, weight=float(w))

    # Layout (spring is fine for small-medium graphs)
    pos = nx.spring_layout(G, seed=42)

    # edge widths proportional to normalized weights
    weights = np.array([d["weight"] for (_, _, d) in G.edges(data=True)])
    if weights.size:
        w_min, w_max = weights.min(), weights.max()
        if w_max > w_min:
            w_norm = 1.0 + 4.0 * (weights - w_min) / (w_max - w_min)  # widths in 1..5
        else:
            w_norm = np.ones_like(weights) * 2.0
    else:
        w_norm = []

    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title("Resonance Network")

    # draw nodes
    node_sizes = [300 for _ in G.nodes()]  # uniform node size; could be degree-based
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, ax=ax, alpha=0.9)

    # draw edges
    nx.draw_networkx_edges(G, pos, width=w_norm, alpha=0.7, ax=ax)

    # labels
    labels = node_labels if node_labels is not None else {n: (n[:20] + "...") if len(n) > 23 else n for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, ax=ax)

    ax.axis("off")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, bbox_inches="tight")
    if show:
        plt.show()
    return fig
