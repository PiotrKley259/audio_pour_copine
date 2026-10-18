#!/bin/bash
# Double-clique sur ce fichier pour installer l'application.
cd "$(dirname "$0")" || exit 1

echo "=== Installation du Transcripteur audio ==="
echo

if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ Python n'est pas installé sur cet ordinateur."
  echo
  echo "   1. Va sur https://www.python.org/downloads/macos/"
  echo "   2. Télécharge et installe la dernière version."
  echo "   3. Relance ce fichier."
  echo
  read -r -p "Appuie sur Entrée pour fermer."
  exit 1
fi

echo "→ Préparation de l'environnement (ça peut prendre quelques minutes)…"
python3 -m venv .venv || { echo "❌ Création de l'environnement impossible."; read -r -p "Entrée pour fermer."; exit 1; }

./.venv/bin/python -m pip install --upgrade pip >/dev/null
if ! ./.venv/bin/python -m pip install -r requirements.txt; then
  echo
  echo "❌ L'installation des composants a échoué. Vérifie ta connexion internet et relance."
  read -r -p "Appuie sur Entrée pour fermer."
  exit 1
fi

# macOS met en quarantaine tout fichier téléchargé, ce qui déclenche l'alerte
# « Apple n'a pas pu confirmer... » à chaque lancement. Puisque l'utilisatrice
# vient d'autoriser explicitement ce dossier, on lève la quarantaine dessus
# pour que « Transcripteur.command » s'ouvre ensuite d'un simple double-clic.
xattr -dr com.apple.quarantine . 2>/dev/null

echo
echo "✅ Installation terminée !"
echo "   Tu peux maintenant double-cliquer sur « Transcripteur.command »."
echo
read -r -p "Appuie sur Entrée pour fermer cette fenêtre."
