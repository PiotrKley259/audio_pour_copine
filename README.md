# 🎙️ Transcripteur audio

Une petite application pour **nettoyer le bruit de fond** d'un enregistrement et le **transcrire en texte**.

Tout se passe sur ton ordinateur : **aucun fichier n'est envoyé sur internet**, et c'est entièrement gratuit.

---

## Installation (une seule fois)

1. En haut de cette page, clique sur le bouton vert **« Code »** puis **« Download ZIP »**.
2. Ouvre le fichier téléchargé pour le décompresser, et place le dossier où tu veux (par exemple dans *Documents*).
3. Double-clique sur **`installer.command`**.
4. 🔒 **macOS va refuser une première fois**, avec le message *« Apple n'a pas pu confirmer que « installer.command » ne contenait pas de logiciel malveillant »*. C'est normal : le Mac se méfie de tout fichier téléchargé. Pour l'autoriser :
   - clique sur **« Terminé »** (⚠️ **pas** « Déplacer vers la corbeille ») ;
   - ouvre **Réglages Système** → **Confidentialité et sécurité** ;
   - descends jusqu'à la section **Sécurité** : la ligne *« installer.command » a été bloqué…* apparaît, avec un bouton **« Ouvrir quand même »** ;
   - clique dessus, confirme avec Touch ID ou ton mot de passe, puis **« Ouvrir »**.
5. Une fenêtre noire s'ouvre et installe ce qu'il faut. Ça prend quelques minutes. Quand tu vois **« Installation terminée ! »**, tu peux la fermer.

*Cette autorisation n'est à donner qu'une seule fois : l'installateur débloque le dossier au passage, donc l'application se lancera ensuite d'un simple double-clic.*

## Utilisation (à chaque fois)

1. Double-clique sur **`Transcripteur.command`**.
2. La page s'ouvre toute seule dans ton navigateur.
3. Glisse ton fichier audio dans le cadre, puis clique sur **« Transcrire »**.
4. Récupère le texte (bouton copier), ou télécharge le `.txt` et les sous-titres `.srt`.

Garde la fenêtre noire ouverte pendant que tu utilises l'application. Pour quitter, ferme-la.

> ⏳ **Le tout premier « Transcrire » est long** (quelques minutes) : l'application télécharge une fois pour
> toutes son modèle de reconnaissance vocale. Les fois suivantes sont beaucoup plus rapides.

## Options (dans le panneau « Options »)

| Réglage | À quoi ça sert |
|---|---|
| **Enlever le bruit de fond** | Décoche-la si l'enregistrement est déjà propre. |
| **Force du nettoyage** | Plus haut = plus propre, mais la voix peut sonner métallique. 0,75 va bien. |
| **Qualité de la transcription** | *Standard* est le bon compromis. *Précise* / *Maximale* sont meilleures mais nettement plus lentes. |
| **Langue** | Laisse *Détection automatique*, ou force *Français* si elle se trompe. |

## Formats acceptés

`mp3`, `m4a` (mémos vocaux iPhone), `wav`, `aac`, `ogg`, `flac`, et même les vidéos `mp4` / `mov`.

Les résultats sont aussi enregistrés dans le sous-dossier **`sorties/`** du dossier de l'application.

## Ça ne marche pas ?

- **« Python n'est pas installé »** → installe-le depuis <https://www.python.org/downloads/macos/> puis relance `installer.command`.
- **« Apple n'a pas pu confirmer… »** → c'est la protection des fichiers téléchargés : suis l'étape 4 de l'installation (Réglages Système → Confidentialité et sécurité → **« Ouvrir quand même »**).
- **`Transcripteur.command` est encore bloqué** → relance `installer.command` : il lève le blocage sur tout le dossier.
- **« L'installation des composants a échoué »** → vérifie la connexion internet et relance `installer.command`.
- **La page ne s'ouvre pas** → ouvre ton navigateur et va sur <http://127.0.0.1:7860>.
- **Transcription farfelue** → force la langue sur *Français* et passe la qualité sur *Précise*.

## Sous le capot

- Transcription : [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (modèle Whisper d'OpenAI), en local sur le processeur.
- Débruitage : filtre passe-haut + [noisereduce](https://github.com/timsainb/noisereduce) + normalisation du volume.
- Interface : [Gradio](https://www.gradio.app/) servie uniquement sur cet ordinateur.
