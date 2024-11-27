import pandas as pd


def traiter_csv(fichier_csv):
    df = pd.read_csv(fichier_csv)
    titres_uniques = {}
    for _, row in df.iterrows():
        label = row['Label']
        titre = row['Titre']
        
        # Si le label n'est pas dans le dictionnaire, l'ajouter avec le titre
        if label not in titres_uniques:
            titres_uniques[label] = set()
        
        # Ajouter le titre à l'ensemble du label, ce qui supprime automatiquement les doublons
        titres_uniques[label].add(titre)
    
    result = []

    for label, titres in titres_uniques.items():
        for titre in titres:
            result.append({'Label': label, 'Titre': titre})
    df_sans_doublons = pd.DataFrame(result)

    return df_sans_doublons


fichier_csv = '/home/gris/Bureau/Projet_DL/Donnees_projet/donnees_labelisees.csv' 
df_sans_doublons = traiter_csv(fichier_csv)

df_sans_doublons.to_csv("donnees_propres.csv", index=False)