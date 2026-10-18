"""Débruitage léger : passe-haut, spectral gating, normalisation."""

from __future__ import annotations

import noisereduce as nr
import numpy as np
from scipy.signal import butter, sosfiltfilt

TARGET_RMS = 10 ** (-20 / 20)  # -20 dBFS
PEAK_CEILING = 0.97


def _highpass(samples: np.ndarray, sample_rate: int, cutoff: float = 80.0) -> np.ndarray:
    """Coupe les grondements et le souffle de basse fréquence (clim, trafic, poignée)."""
    sos = butter(2, cutoff / (sample_rate / 2), btype="highpass", output="sos")
    return sosfiltfilt(sos, samples).astype(np.float32)


def normalize(samples: np.ndarray) -> np.ndarray:
    """Remonte le niveau à -20 dBFS RMS sans jamais saturer."""
    rms = float(np.sqrt(np.mean(samples**2)))
    if rms < 1e-9:
        return samples
    gain = TARGET_RMS / rms
    peak = float(np.max(np.abs(samples)))
    if peak * gain > PEAK_CEILING:
        gain = PEAK_CEILING / peak
    return (samples * gain).astype(np.float32)


def clean(samples: np.ndarray, sample_rate: int, force: float = 0.75) -> np.ndarray:
    """Enlève le bruit de fond puis réaligne le volume.

    `force` (0-1) est la proportion de bruit retirée : plus c'est haut, plus
    c'est propre, mais plus la voix risque de sonner métallique.
    """
    out = _highpass(samples, sample_rate)
    out = nr.reduce_noise(
        y=out,
        sr=sample_rate,
        stationary=False,
        prop_decrease=float(np.clip(force, 0.0, 1.0)),
    ).astype(np.float32)
    return normalize(out)
