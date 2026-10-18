"""Transcripteur audio — interface locale.

Dépose un fichier audio, l'app enlève le bruit de fond et écrit la transcription.

Le serveur n'écoute que sur 127.0.0.1 : les enregistrements ne quittent pas la
machine. La télémétrie de Gradio (activée par défaut, vers api.gradio.app) est
coupée, ce qui désactive aussi celle de Hugging Face au téléchargement du modèle.
Seul accès réseau restant : le téléchargement du modèle Whisper, une seule fois.
"""

from __future__ import annotations

import re
import webbrowser
from pathlib import Path

import gradio as gr

from theme import CSS, FORCER_MODE_CLAIR, theme
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
    title="Studio de transcription",
    theme=theme,
    css=CSS,
    head=FORCER_MODE_CLAIR,
    analytics_enabled=False,  # pas de télémétrie vers api.gradio.app
    # Gradio recopie chaque fichier déposé dans un dossier temporaire et ne les
    # supprime jamais par défaut. On purge les copies de plus de 30 minutes.
    delete_cache=(1800, 1800),
) as demo:
    gr.HTML(
        """
        <div id="entete">
          <svg class="embleme" width="92" height="92" viewBox="0 0 92 92" fill="none"
               stroke="#c45a76" stroke-width="1" aria-hidden="true">
            <circle cx="46" cy="46" r="43"/>
            <circle cx="46" cy="46" r="36" stroke="#e5d6ce"/>
            <!-- rayons, en écho au médaillon du vitrail -->
            <g stroke="#e5d6ce">
              <path d="M46 10V18M46 74v8M10 46h8M74 46h8"/>
              <path d="M20.6 20.6l5.7 5.7M65.7 65.7l5.7 5.7M71.4 20.6l-5.7 5.7M26.3 65.7l-5.7 5.7"/>
            </g>
            <!-- micro de studio, au trait -->
            <rect x="39" y="26" width="14" height="25" rx="7"/>
            <path d="M33 45c0 7.2 5.8 13 13 13s13-5.8 13-13"/>
            <path d="M46 58v9M38 67h16"/>
          </svg>
          <p class="accroche">
            Dépose un enregistrement. Le bruit de fond s'efface,
            les mots s'écrivent. Tout reste sur ton ordinateur.
          </p>
        </div>
        <div id="filet-haut"></div>
        """
    )

    with gr.Row(equal_height=False):
        with gr.Column(scale=4, elem_id="colonne-gauche"):
            entree = gr.Audio(
                label="L'enregistrement",
                type="filepath",
                sources=["upload", "microphone"],
                elem_id="composant-audio",
            )
            with gr.Accordion("Réglages", open=False):
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
            bouton = gr.Button(
                "Transcrire", variant="primary", size="lg", elem_id="bouton-transcrire"
            )
            gr.HTML(
                """
                <div id="notes">
                  <p><strong>Formats</strong> — mp3, m4a, wav, et même les vidéos.</p>
                  <p><strong>Première fois</strong> — le modèle se télécharge, comptez
                     quelques minutes. Ensuite tout va vite.</p>
                  <p><strong>Si le texte se trompe</strong> — ouvrez les réglages,
                     choisissez Français et la qualité Précise.</p>
                </div>
                """
            )

        with gr.Column(scale=6, elem_id="colonne-droite"):
            with gr.Tabs():
                with gr.Tab("Texte"):
                    texte = gr.Textbox(
                        label="", lines=8, show_copy_button=True, container=False,
                        placeholder="Le texte apparaîtra ici.",
                        elem_id="zone-texte",
                    )
                with gr.Tab("Horodaté"):
                    horodate = gr.Textbox(
                        label="", lines=8, show_copy_button=True, container=False,
                        placeholder="Le texte minuté apparaîtra ici.",
                        elem_id="zone-texte-minute",
                    )
            audio_propre = gr.Audio(
                label="Audio nettoyé", type="filepath", elem_id="audio-propre"
            )
            fichiers = gr.File(
                label="Fichiers à télécharger", height=110, elem_id="fichiers"
            )

    bouton.click(
        traiter,
        inputs=[entree, nettoyer, force, qualite, langue],
        outputs=[texte, horodate, audio_propre, fichiers],
    )

if __name__ == "__main__":
    # On ouvre soi-même le navigateur pour imposer la palette claire dès la
    # première image, plutôt que de laisser Gradio suivre le thème du système.
    _, url, _ = demo.launch(
        server_name="127.0.0.1",
        inbrowser=False,
        prevent_thread_lock=True,
        show_api=False,
    )
    webbrowser.open(f"{url}?__theme=light")
    demo.block_thread()
