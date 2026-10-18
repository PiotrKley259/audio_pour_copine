"""Habillage de l'interface : palette, typographie, CSS.

Direction : la rigueur éditoriale de santionispirits.com — beaucoup de vide,
une grande typographie art-déco, des filets d'un pixel, un seul accent de
couleur — mais transposée en pastel : fond ivoire au lieu du noir #121212, et
rose profond au lieu du rouge #c82924.

Les polices du site (PP Nikkei Maru, Charles Rosie, GT Era) sont commerciales ;
on leur substitue deux Google Fonts libres d'esprit proche : Poiret One, une
déco fine et élégante pour les titres, et Jost, une géométrique sobre pour le
texte — le couple classique de l'Art déco.
"""

from __future__ import annotations

import gradio as gr
from gradio.themes.utils import colors

# L'unique accent : le rouge sang de Santioni, adouci en rose profond.
ROSE = colors.Color(
    name="rose_profond",
    c50="#fdf4f6", c100="#fbe8ec", c200="#f5cfd8", c300="#eaabbb",
    c400="#da7f96", c500="#c45a76", c600="#a84760", c700="#8a394e",
    c800="#6d2d3e", c900="#52222f", c950="#33151d",
)

# Neutres chauds : l'ivoire et l'encre prune, jamais de gris froid.
IVOIRE = colors.Color(
    name="ivoire",
    c50="#fdfaf8", c100="#faf4f0", c200="#f1e7e1", c300="#e5d6ce",
    c400="#cdb8ae", c500="#ab9389", c600="#8a736a", c700="#6b5852",
    c800="#4e403c", c900="#372d2b", c950="#241d1c",
)

theme = gr.themes.Base(
    primary_hue=ROSE,
    secondary_hue=ROSE,
    neutral_hue=IVOIRE,
    font=(gr.themes.GoogleFont("Jost"), "Helvetica", "sans-serif"),
    font_mono=(gr.themes.GoogleFont("Jost"), "ui-monospace", "monospace"),
    radius_size=gr.themes.sizes.radius_none,
    text_size=gr.themes.sizes.text_md,
    spacing_size=gr.themes.sizes.spacing_lg,
).set(
    body_background_fill="#fdfaf8",
    body_background_fill_dark="#241d1c",
    body_text_color="#372d2b",
    body_text_color_dark="#faf4f0",
    body_text_color_subdued="#8a736a",
    # Pas de cartes : des surfaces nues séparées par des filets.
    block_background_fill="transparent",
    block_background_fill_dark="transparent",
    block_border_width="0px",
    block_shadow="none",
    block_label_background_fill="transparent",
    block_label_text_color="#ab9389",
    block_label_text_size="11px",
    block_label_text_weight="500",
    block_title_text_color="#ab9389",
    block_title_text_size="11px",
    block_title_text_weight="500",
    panel_background_fill="transparent",
    panel_border_width="0px",
    # Le bouton : aplat rose, angles vifs, aucune ombre.
    button_primary_background_fill="#c45a76",
    button_primary_background_fill_hover="#372d2b",
    button_primary_text_color="#fdfaf8",
    button_primary_border_color="#c45a76",
    button_secondary_background_fill="transparent",
    button_secondary_border_color="#e5d6ce",
    button_secondary_text_color="#6b5852",
    button_large_radius="0px",
    button_small_radius="0px",
    # Champs : un simple filet, qui s'assombrit au focus.
    input_background_fill="#fdfaf8",
    input_background_fill_dark="#2f2625",
    input_border_width="1px",
    input_border_color="#e5d6ce",
    input_border_color_focus="#c45a76",
    input_radius="0px",
    slider_color="#c45a76",
    checkbox_background_color_selected="#c45a76",
    checkbox_border_color_selected="#c45a76",
    checkbox_border_radius="0px",
    link_text_color="#a84760",
)

# Gradio suit le thème du système : en mode sombre, l'ivoire disparaît.
# Ce script recharge la page une fois avec le paramètre qui fige la palette.
FORCER_MODE_CLAIR = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poiret+One&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<script>
  if (!window.location.search.includes("__theme")) {
    const s = window.location.search;
    window.location.search = s ? s + "&__theme=light" : "?__theme=light";
  }
</script>
"""

CSS = """
/* ---- Trame générale : une colonne étroite, beaucoup de marge ---- */
html, body, gradio-app { background: #fdfaf8 !important; }
.gradio-container {
  max-width: 940px !important;
  padding: 0 32px 80px !important;
  background: #fdfaf8;
}
footer { display: none !important; }

/* ---- Bandeau : l'emblème, le titre déco, un filet ---- */
#entete { text-align: center; padding: 64px 0 36px; }
#entete .embleme { margin: 0 auto 26px; display: block; }
#entete h1 {
  font-family: 'Poiret One', 'Jost', sans-serif;
  font-size: clamp(2.4rem, 6vw, 3.6rem);
  font-weight: 400; line-height: 1.05; margin: 0;
  color: #372d2b; letter-spacing: .02em;
}
#entete h1 em { font-style: normal; color: #c45a76; }
#entete .accroche {
  margin: 20px auto 0; max-width: 460px;
  font-size: .95rem; font-weight: 300; line-height: 1.7; color: #8a736a;
}
#entete .surtitre, .etiquette {
  font-size: .68rem; font-weight: 500;
  letter-spacing: .28em; text-transform: uppercase; color: #cdb8ae;
}
#entete .surtitre { display: block; margin-bottom: 18px; }
#filet-haut { height: 1px; background: #f1e7e1; margin: 8px 0 44px; }

/* ---- Étiquettes de Gradio : petites capitales espacées ---- */
span[data-testid="block-info"], .gradio-container label span,
#composant-audio span, .block > label > span {
  text-transform: uppercase !important;
  letter-spacing: .2em !important;
  font-size: .66rem !important;
  font-weight: 500 !important;
  color: #ab9389 !important;
}

/* ---- Colonnes séparées par un filet vertical, comme une mise en page de magazine ---- */
#colonne-gauche { padding-right: 38px; border-right: 1px solid #f1e7e1; }
#colonne-droite { padding-left: 38px; }

/* ---- Étiquettes : du texte nu, sans pastille ni cadre ---- */
.block > label, span[data-testid="block-info"] {
  background: transparent !important; border: none !important;
  box-shadow: none !important; padding-left: 0 !important;
}
/* L'icône de type de composant n'apporte rien dans cette mise en page. */
.block > label svg, label > .icon { display: none !important; }

/* ---- Zone de dépôt : un seul rectangle au trait ---- */
#composant-audio {
  border: 1px solid #e5d6ce !important;
  border-radius: 0 !important;
  background: #fdfaf8 !important;
  padding: 0 !important;
}
#composant-audio > div, #composant-audio .wrap {
  border: none !important; background: transparent !important;
}
#composant-audio:hover { border-color: #c45a76 !important; }
#composant-audio .wrap { min-height: 190px !important; }

/* ---- Le bouton : plein, carré, en capitales espacées ---- */
button#bouton-transcrire {
  width: 100%;
  border-radius: 0 !important;
  font-size: .76rem !important;
  font-weight: 500 !important;
  letter-spacing: .26em !important;
  text-transform: uppercase !important;
  padding: 19px 20px !important;
  border: 1px solid #c45a76 !important;
  transition: background-color .35s ease, color .35s ease !important;
}
button#bouton-transcrire:hover { border-color: #372d2b !important; }

/* ---- Onglets : un simple soulignement sous l'onglet actif ---- */
.tab-nav, div[role="tablist"] {
  border-bottom: 1px solid #f1e7e1 !important;
  gap: 28px !important;
}
.tab-nav button, div[role="tablist"] button {
  background: none !important; border: none !important;
  border-radius: 0 !important; padding: 0 0 12px !important;
  font-size: .68rem !important; font-weight: 500 !important;
  letter-spacing: .22em !important; text-transform: uppercase !important;
  color: #cdb8ae !important;
}
.tab-nav button.selected, div[role="tablist"] button.selected {
  color: #c45a76 !important;
  box-shadow: inset 0 -1px 0 0 #c45a76 !important;
}

/* ---- Le texte transcrit : lecture confortable, pas un champ de formulaire ---- */
#zone-texte textarea {
  border: none !important; background: transparent !important;
  font-size: 1.02rem !important; font-weight: 300 !important;
  line-height: 1.85 !important; color: #372d2b !important;
  padding: 26px 0 !important; resize: none !important;
}
#zone-texte textarea::placeholder { color: #cdb8ae !important; font-style: italic; }

/* ---- Sorties : des blocs compacts, séparés par un filet ---- */
#audio-propre, #fichiers {
  border-top: 1px solid #f1e7e1 !important;
  padding-top: 20px !important; margin-top: 26px !important;
}
#audio-propre .wrap, #fichiers .wrap { min-height: 0 !important; }
#fichiers { min-height: 0 !important; }
#fichiers .wrap, #fichiers > div:not(label) { max-height: 110px !important; }

/* ---- Notes de bas de colonne ---- */
#notes { margin-top: 34px; padding-top: 22px; border-top: 1px solid #f1e7e1; }
#notes p {
  font-size: .78rem; font-weight: 300; line-height: 1.75;
  color: #ab9389; margin: 0 0 12px;
}
#notes p strong { color: #8a736a; font-weight: 500; }

/* ---- Pied de page ---- */
#pied {
  text-align: center; margin-top: 70px; padding-top: 26px;
  border-top: 1px solid #f1e7e1;
  font-size: .66rem; letter-spacing: .26em;
  text-transform: uppercase; color: #cdb8ae;
}

/* ---- La barre de progression reprend l'accent ---- */
.progress-bar, .progress-level-inner { background: #c45a76 !important; }
"""
