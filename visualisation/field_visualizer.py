# field_visualizer_improved.py
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, Dict
from core.resonance_field import ResonanceField
from collections import Counter

class FieldVisualizer:
    """Improved visualizer for ResonanceField diagnostics."""

    def __init__(self):
        pass

    def plot_complete_field_state(
        self,
        field: ResonanceField,
        *,
        figsize=(14, 10),
        tensor_log_scale: bool = True,
        top_n_keywords: int = 10,
        save_path: Optional[str] = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Create a 2x2 diagnostic figure:
          - Field tensor magnitude (imshow + colorbar)
          - Amplitudes over time (vs timestamp)
          - Frequency histogram
          - Entanglement degree / energy evolution (two-panel combined)
          - Side: a small keyword list printed under the figure

        Returns the matplotlib Figure object.
        """

        # Prepare figure with slightly different layout to show more info
        fig = plt.figure(figsize=figsize)
        gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.4)

        ax_tensor = fig.add_subplot(gs[0:2, 0:2])
        ax_amp = fig.add_subplot(gs[0, 2])
        ax_freq = fig.add_subplot(gs[1, 2])
        ax_bottom = fig.add_subplot(gs[2, 0:3])  # entanglement + energy

        # ---------- Field tensor ----------
        try:
            tensor = np.asarray(field.field_tensor)
            mag = np.abs(tensor)
            if tensor_log_scale:
                # add small epsilon and log-scale for visibility
                im = ax_tensor.imshow(np.log1p(mag), aspect='auto')
                cb = fig.colorbar(im, ax=ax_tensor, fraction=0.046, pad=0.04)
                cb.set_label('log(1 + |tensor|)')
            else:
                im = ax_tensor.imshow(mag, aspect='auto')
                cb = fig.colorbar(im, ax=ax_tensor, fraction=0.046, pad=0.04)
                cb.set_label('|tensor|')
            ax_tensor.set_title('Field Tensor (magnitude)')
        except Exception as e:
            ax_tensor.text(0.5, 0.5, f'Error plotting tensor:\n{e}', ha='center', va='center')
            ax_tensor.set_title('Field Tensor (error)')

        # ---------- Amplitudes vs time ----------
        if field.waves:
            # sort by timestamp if available
            try:
                waves_sorted = sorted(field.waves, key=lambda w: getattr(w, 'timestamp', 0.0))
                timestamps = [getattr(w, 'timestamp', i) for i, w in enumerate(waves_sorted)]
            except Exception:
                waves_sorted = list(field.waves)
                timestamps = list(range(len(waves_sorted)))

            amplitudes = [float(w.amplitude) for w in waves_sorted]
            ax_amp.plot(amplitudes, marker='o', linestyle='-', markersize=4)
            ax_amp.set_title('Wave amplitudes (insertion order)')
            ax_amp.set_xlabel('Index (sorted by timestamp)')
            ax_amp.set_ylabel('Amplitude')

            # ---------- Frequency histogram ----------
            freqs = [float(getattr(w, 'frequency', 0.0)) for w in waves_sorted]
            ax_freq.hist(freqs, bins=12, edgecolor='black')
            ax_freq.set_title('Frequency distribution')
            ax_freq.set_xlabel('Frequency')
            ax_freq.set_ylabel('Count')

            # ---------- Entanglement degree histogram & energy evolution ----------
            ent_degrees = [len(getattr(w, 'entangled_with', [])) for w in waves_sorted]

            # energy evolution: compute incremental "kinetic" proxy (sum of amplitude^2 * freq up to i)
            energies = []
            cumulative = 0.0
            for w in waves_sorted:
                cumulative += (float(w.amplitude) ** 2) * float(getattr(w, 'frequency', 0.0))
                energies.append(cumulative)

            ax_bottom.plot(energies, label='Cumulative kinetic proxy', linewidth=2)
            # show entanglement distribution as bar on same axis (secondary y)
            ax2b = ax_bottom.twinx()
            ax2b.hist(ent_degrees, bins=range(0, max(ent_degrees) + 2 if ent_degrees else 2), alpha=0.3)
            ax_bottom.set_title('Energy evolution (proxy) and entanglement degree histogram')
            ax_bottom.set_xlabel('Index (sorted)')
            ax_bottom.set_ylabel('Energy proxy (amplitude^2 * freq cum.)')
            ax2b.set_ylabel('Entanglement degree (counts)')

            # ---------- Keywords summary (small text area under the tensor) ----------
            all_keywords = []
            for w in waves_sorted:
                kws = getattr(w, 'keywords', None)
                if kws:
                    all_keywords.extend(list(kws))
            kw_counts = Counter(all_keywords)
            top_kw = kw_counts.most_common(top_n_keywords)

            # add keywords as annotation under the tensor plot
            kw_text = "Top keywords: " + ", ".join(f"{k}({c})" for k, c in top_kw) if top_kw else "No keywords"
            # place text below the tensor axes
            fig.suptitle('Complete Field State Overview', fontsize=14)
            ax_tensor.text(0.01, -0.12, kw_text, transform=ax_tensor.transAxes, fontsize=9, va='top')

        else:
            # no waves: annotate subplots
            ax_amp.text(0.5, 0.5, 'No waves', ha='center', va='center')
            ax_freq.text(0.5, 0.5, 'No waves', ha='center', va='center')
            ax_bottom.text(0.5, 0.5, 'No waves', ha='center', va='center')

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        if save_path:
            fig.savefig(save_path, bbox_inches='tight', dpi=150)

        if show:
            plt.show()

        return fig
