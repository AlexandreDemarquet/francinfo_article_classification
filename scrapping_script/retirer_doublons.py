import pandas as pd


def traiter_csv(fichier_csv):
    df = pd.read_csv(fichier_csv)
    titres_uniques = {}
    for _, row in df.iterrows():
        label = row['Label']
        titre = row['Titre']
        date = row['Date']
        
        # Si le label n'est pas dans le dictionnaire, l'ajouter avec le titre
        if label not in titres_uniques:
            titres_uniques[label] = set()
        
        # Ajouter le titre à l'ensemble du label, ce qui supprime automatiquement les doublons

        titres_uniques[label].add(titre)
    
    result = []
    l_date = []
    for label, titres in titres_uniques.items():
        for titre in titres:
            date = df[df["Titre"] == titre]["Date"].iloc[0]
            result.append({'Label': label, 'Titre': titre, 'Date':date})
    df_sans_doublons = pd.DataFrame(result)

    return df_sans_doublons


fichier_csv = '/home/n7student/deep_learning/projet/francinfo_article_classification/scrapping_script/donnees_final_avec_doublons.csv' 
df_sans_doublons = traiter_csv(fichier_csv)
print(df_sans_doublons["Label"].unique())
for label in df_sans_doublons["Label"].unique():
    print(f"{label} : {len(df_sans_doublons[df_sans_doublons['Label'] == label])}")
# print(pd.read_csv(fichier_csv))
# print(len(df_sans_doublons["culture"]))

df_sans_doublons.to_csv("donnees_final_sans_doublons.csv", index=False)