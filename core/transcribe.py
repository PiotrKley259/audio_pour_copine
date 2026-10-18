"""Transcription locale via faster-whisper (aucune donnée ne quitte la machine)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

import numpy as np
from faster_whisper import WhisperModel

_models: dict[str, WhisperModel] = {}


@dataclass
class Segment:
    start: float
    end: float
    text: str


def get_model(size: str = "small") -> WhisperModel:
    """Charge le modèle une seule fois par taille et le garde en mémoire."""
    if size not in _models:
        _models[size] = WhisperModel(size, device="cpu", compute_type="int8")
    return _models[size]


def _timestamp(seconds: float, sep: str = ",") -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def to_srt(segments: Iterable[Segment]) -> str:
    blocks = []
    for i, seg in enumerate(segments, start=1):
        blocks.append(
            f"{i}\n{_timestamp(seg.start)} --> {_timestamp(seg.end)}\n{seg.text}\n"
        )
    return "\n".join(blocks)


def to_timestamped(segments: Iterable[Segment]) -> str:
    return "\n".join(
        f"[{_timestamp(seg.start, sep='.')[:-4]}] {seg.text}" for seg in segments
    )


def transcribe(
    samples: np.ndarray,
    sample_rate: int,
    size: str = "small",
    language: str | None = None,
    progress_cb: Callable[[float], None] | None = None,
) -> tuple[str, list[Segment]]:
    """Retourne (texte complet, segments). `language=None` = détection auto."""
    model = get_model(size)
    total = max(len(samples) / float(sample_rate), 1e-6)
    raw_segments, _info = model.transcribe(
        samples,
        language=language,
        vad_filter=True,
        beam_size=1,
        condition_on_previous_text=False,
    )

    segments: list[Segment] = []
    for seg in raw_segments:  # générateur paresseux : le travail se fait ici
        text = seg.text.strip()
        if text:
            segments.append(Segment(seg.start, seg.end, text))
        if progress_cb is not None:
            progress_cb(min(seg.end / total, 1.0))

    return " ".join(s.text for s in segments), segments
