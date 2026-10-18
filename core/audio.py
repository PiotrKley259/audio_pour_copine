"""Lecture et écriture de fichiers audio, sans dépendance système.

Le décodage passe par PyAV (ffmpeg embarqué dans la wheel), ce qui évite
d'avoir à installer ffmpeg à la main sur la machine de l'utilisatrice.
"""

from __future__ import annotations

import numpy as np
import av
import soundfile as sf

SAMPLE_RATE = 16000  # ce que Whisper attend


class AudioError(Exception):
    """Problème de contenu audio dont le message est montrable à l'utilisatrice.

    Type dédié car les erreurs de décodage de PyAV héritent de ValueError :
    on ne pourrait pas les distinguer des nôtres.
    """


def load_audio(path: str, sample_rate: int = SAMPLE_RATE) -> np.ndarray:
    """Décode n'importe quel fichier audio/vidéo en mono float32 à `sample_rate`."""
    with av.open(path) as container:
        if not container.streams.audio:
            raise AudioError("Ce fichier ne contient aucune piste audio.")
        stream = container.streams.audio[0]
        resampler = av.AudioResampler(format="flt", layout="mono", rate=sample_rate)
        chunks = []
        for frame in container.decode(stream):
            for resampled in resampler.resample(frame):
                chunks.append(resampled.to_ndarray().reshape(-1))
        # Vider le tampon interne du resampler
        for resampled in resampler.resample(None):
            chunks.append(resampled.to_ndarray().reshape(-1))

    if not chunks:
        raise AudioError("Le fichier audio semble vide.")
    return np.concatenate(chunks).astype(np.float32)


def save_wav(path: str, samples: np.ndarray, sample_rate: int = SAMPLE_RATE) -> str:
    """Écrit un WAV 16 bits lisible partout."""
    sf.write(path, np.clip(samples, -1.0, 1.0), sample_rate, subtype="PCM_16")
    return path


def duration(samples: np.ndarray, sample_rate: int = SAMPLE_RATE) -> float:
    return len(samples) / float(sample_rate)
