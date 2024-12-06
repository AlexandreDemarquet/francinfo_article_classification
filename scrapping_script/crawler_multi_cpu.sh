#!/bin/bash

# Liste des catégories à crawler
CATEGORIES=("monde" "monde/environnement" "monde/europe" "societe" "politique" "sports" "culture" "sante" "meteo")

for CATEGORIE in "${CATEGORIES[@]}"; do
    echo "Lancement du crawler pour la catégorie : $CATEGORIE en arrière-plan"
    python3 crawler2.py "$CATEGORIE" &

    PID=$!
    echo "Crawler lancé pour $CATEGORIE avec PID : $PID"
done

wait
echo "Tous les crawlings sont terminés."

