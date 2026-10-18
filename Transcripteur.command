#!/bin/bash
# Double-clique sur ce fichier pour lancer l'application.
cd "$(dirname "$0")" || exit 1

if [ ! -x "./.venv/bin/python" ]; then
  echo "L'application n'est pas encore installée. Lance d'abord « installer.command »."
  read -r -p "Appuie sur Entrée pour fermer."
  exit 1
fi

echo "Démarrage… la page va s'ouvrir dans ton navigateur."
echo "Garde cette fenêtre ouverte pendant que tu utilises l'application."
echo "Pour quitter : ferme cette fenêtre."
echo
exec ./.venv/bin/python app.py
