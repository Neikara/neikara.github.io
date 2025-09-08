import requests
import time

# --- Configuration ---
ID_DU_JOUEUR = "1484188"  # <<< REMPLACEZ CECI PAR L'ID DU JOUEUR
INTERVALLE_DE_VERIFICATION = 120  # en secondes (vérification toutes les minutes)

url_api = f"https://online-go.com/api/v1/players/{ID_DU_JOUEUR}/games"

# On initialise le nombre de parties en cours au démarrage
try:
    reponse = requests.get(url_api, timeout=10)
    reponse.raise_for_status()  # Lève une erreur pour les mauvaises réponses (4xx ou 5xx)
    donnees = reponse.json()
    nombre_de_parties_initial = donnees.get('count')
    print(f"Initialisation : Le joueur a actuellement {nombre_de_parties_initial} parties connues.")
except requests.exceptions.RequestException as e:
    print(f"Erreur lors de l'initialisation : {e}")
    exit()

# Boucle principale pour la surveillance
while True:
    try:
        # Envoie une requête à l'API d'OGS pour obtenir la liste des parties du joueur
        reponse = requests.get(url_api, timeout=10)
        reponse.raise_for_status()
        donnees = reponse.json()

        # Le nombre de parties en cours est dans le champ 'count'
        nombre_de_parties_actuel = donnees.get('count')

        # Compare le nombre de parties actuel avec le nombre de parties initial
        if nombre_de_parties_actuel > nombre_de_parties_initial:
            print("\n--- ATTENTION ! NOUVELLE PARTIE DÉTECTÉE ! ---")
            print(f"Le joueur a commencé une nouvelle partie. Total actuel : {nombre_de_parties_actuel}.")

            # Vous pouvez ajouter une logique de notification plus avancée ici
            # Par exemple : envoi d'un e-mail, d'une notification push, etc.

            # Mise à jour du nombre de parties pour la prochaine vérification
            nombre_de_parties_initial = nombre_de_parties_actuel

        elif nombre_de_parties_actuel < nombre_de_parties_initial:
            # Gère le cas où une partie se termine
            print(f"Une partie a été terminée. Le joueur a maintenant {nombre_de_parties_actuel} parties.")
            nombre_de_parties_initial = nombre_de_parties_actuel

        else:
            # Pas de changement
            print(f"Pas de nouvelle partie détectée. Le nombre de parties reste à {nombre_de_parties_actuel}.")

    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion : {e}. Réessai dans {INTERVALLE_DE_VERIFICATION} secondes.")

    # Attend l'intervalle défini avant de recommencer
    time.sleep(INTERVALLE_DE_VERIFICATION)