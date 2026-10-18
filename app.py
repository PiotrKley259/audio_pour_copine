"""Transcripteur audio — interface locale.

Dépose un fichier audio, l'app enlève le bruit de fond et écrit la transcription.

Le serveur n'écoute que sur 127.0.0.1 : les enregistrements ne quittent pas la
machine. La télémétrie de Gradio (activée par défaut, vers api.gradio.app) est
coupée, ce qui désactive aussi celle de Hugging Face au téléchargement du modèle.
Seul accès réseau restant : le téléchargement du modèle Whisper, une seule fois.
"""

from __future__ import annotations

import re
from pathlib import Path

import gradio as gr

from core.audio import SAMPLE_RATE, AudioError, duration, load_audio, save_wav
from core.denoise import clean
from core.transcribe import to_srt, to_timestamped, transcribe

OUT_DIR = Path(__file__).parent / "sorties"

QUALITES = {
    "Rapide — moins précis": "base",
    "Standard (conseillé)": "small",
    "Précise — plus lent": "medium",
    "Maximale — très lent": "large-v3",
}

LANGUES = {
    "Détection automatique": None,
    "Français": "fr",
    "Anglais": "en",
}


def _slug(name: str) -> str:
    return re.sub(r"[^\w\-]+", "_", Path(name).stem)[:60] or "audio"


def traiter(
    fichier: str | None,
    nettoyer: bool,
    force: float,
    qualite: str,
    langue: str,
    progress=gr.Progress(),
):
    if not fichier:
        raise gr.Error("Choisis d'abord un fichier audio 🙂")

    progress(0.02, desc="Lecture du fichier…")
    try:
        samples = load_audio(fichier)
    except AudioError as exc:  # pas de piste audio, fichier vide
        raise gr.Error(str(exc)) from exc
    except Exception as exc:  # fichier corrompu ou format non reconnu
        raise gr.Error(
            "Impossible de lire ce fichier. Vérifie qu'il s'agit bien d'un "
            "enregistrement audio ou vidéo (mp3, m4a, wav, mp4…)."
        ) from exc

    if duration(samples) < 0.2:
        raise gr.Error("Cet enregistrement est trop court (moins d'une seconde).")

    if nettoyer:
        progress(0.08, desc="Nettoyage du bruit de fond…")
        samples = clean(samples, SAMPLE_RATE, force=force)

    OUT_DIR.mkdir(exist_ok=True)
    base = OUT_DIR / _slug(fichier)
    wav_propre = save_wav(str(base.with_suffix(".nettoye.wav")), samples)

    def avance(ratio: float) -> None:
        progress(0.15 + 0.8 * ratio, desc="Transcription en cours…")

    progress(0.15, desc="Transcription en cours… (le 1er lancement télécharge le modèle)")
    texte, segments = transcribe(
        samples,
        SAMPLE_RATE,
        size=QUALITES[qualite],
        language=LANGUES[langue],
        progress_cb=avance,
    )

    if not segments:
        raise gr.Error("Aucune parole détectée dans cet enregistrement.")

    chemin_txt = base.with_suffix(".txt")
    chemin_srt = base.with_suffix(".srt")
    chemin_txt.write_text(texte, encoding="utf-8")
    chemin_srt.write_text(to_srt(segments), encoding="utf-8")

    progress(1.0, desc="Terminé ✅")
    return (
        texte,
        to_timestamped(segments),
        wav_propre,
        [str(chemin_txt), str(chemin_srt)],
    )


with gr.Blocks(
    title="Transcripteur audio",
    theme=gr.themes.Soft(),
    analytics_enabled=False,  # pas de télémétrie vers api.gradio.app
    # Gradio recopie chaque fichier déposé dans un dossier temporaire et ne les
    # supprime jamais par défaut. On purge les copies de plus de 30 minutes.
    delete_cache=(1800, 1800),
) as demo:
    gr.Markdown(
        "# 🎙️ Transcripteur audio\n"
        "Dépose un enregistrement : le bruit de fond est enlevé et le texte est écrit pour toi.\n"
        "*Tout se passe sur cet ordinateur : tes enregistrements ne sont envoyés nulle part.*"
    )

    with gr.Row():
        with gr.Column(scale=1):
            entree = gr.Audio(
                label="Ton enregistrement",
                type="filepath",
                sources=["upload", "microphone"],
            )
            with gr.Accordion("Options", open=False):
                nettoyer = gr.Checkbox(value=True, label="Enlever le bruit de fond")
                force = gr.Slider(
                    0.3, 0.95, value=0.75, step=0.05,
                    label="Force du nettoyage",
                    info="Plus haut = plus propre, mais la voix peut sonner métallique.",
                )
                qualite = gr.Dropdown(
                    choices=list(QUALITES), value="Standard (conseillé)",
                    label="Qualité de la transcription",
                )
                langue = gr.Dropdown(
                    choices=list(LANGUES), value="Détection automatique",
                    label="Langue",
                )
            bouton = gr.Button("Transcrire", variant="primary", size="lg")

        with gr.Column(scale=2):
            with gr.Tabs():
                with gr.Tab("Texte"):
                    texte = gr.Textbox(
                        label="Transcription", lines=14, show_copy_button=True,
                        placeholder="Le texte apparaîtra ici…",
                    )
                with gr.Tab("Avec horodatage"):
                    horodate = gr.Textbox(
                        label="Transcription horodatée", lines=14, show_copy_button=True,
                    )
            audio_propre = gr.Audio(label="Audio nettoyé", type="filepath")
            fichiers = gr.File(label="Télécharger (.txt et .srt)")

    bouton.click(
        traiter,
        inputs=[entree, nettoyer, force, qualite, langue],
        outputs=[texte, horodate, audio_propre, fichiers],
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", inbrowser=True, show_api=False)
