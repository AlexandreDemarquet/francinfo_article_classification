#!/bin/bash

# Liste des catégories à crawler
CATEGORIES=("monde" "environnement" "europe" "societe" "politique" "sport" "culture" "sante" "meteo")

# Boucle sur chaque catégorie et exécution en arrière-plan avec &
for CATEGORIE in "${CATEGORIES[@]}"; do
    echo "Lancement du crawler pour la catégorie : $CATEGORIE en arrière-plan"
    python3 crawler.py "$CATEGORIE" &

    # Capture le PID de la tâche en arrière-plan
    PID=$!
    echo "Crawler lancé pour $CATEGORIE avec PID : $PID"
done

# Attendre que toutes les tâches en arrière-plan se terminent
wait
echo "Tous les crawlings sont terminés."

