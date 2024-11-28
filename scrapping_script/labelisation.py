import os
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
doc_final = pd.DataFrame(columns=['Id','Titre', 'Label'])
liste_categories = ['culture', 'environnement', 'europe', 'meteo', 'monde', 'politique', 'sante', 'societe', 'sports']

for categ in tqdm(liste_categories):
# Dossier contenant les fichiers HTML
    input_dir = "../data_brute_html/" + categ


    # Fonction pour extraire le titre d'un fichier HTML
    def extract_title(soup):
        # 1. Essayer d'abord d'extraire un titre dans <p class="card-article-majeure__title">
        title = soup.find("p", class_="card-article-majeure__title")
        if title:
            return title.get_text().strip()
        
        # 2. Si cette balise n'existe pas, essayer d'extraire un <h1>
        title = soup.find("h1")
        if title:
            return title.get_text().strip()
        
        # 3. Si pas de <h1>, essayer avec le <meta property="og:title">
        meta_title = soup.find("meta", property="og:title")
        if meta_title and meta_title.get("content"):
            return meta_title["content"].strip()
        
        # 4. Sinon, essayer avec la balise <title>
        page_title = soup.find("title")
        if page_title:
            return page_title.get_text().strip()
        
        # 5. Si aucune des méthodes n'a fonctionné, retourner un titre par défaut
        return "Titre non trouvé"

    # Parcourir chaque fichier dans le dossier
    for filename in tqdm( os.listdir(input_dir)):
        # Vérifier que le fichier a une extension .html
        if filename.endswith(".html"):
            file_path = os.path.join(input_dir, filename)
            
            # Lire le contenu du fichier HTML
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
            except UnicodeDecodeError:
                print(f"Erreur d'encodage pour le fichier {filename}.")
                continue
            
            # Parser le contenu avec BeautifulSoup
            soup = BeautifulSoup(content, "html.parser")
            
            # Extraire le titre en utilisant la fonction extract_title
            title = extract_title(soup)

            if "\n" in title:
                if ":" in title.split("\n")[0] :
                    title = title.split("\n")[-1]
                else:
                    title = title.split("\n")[0]
            
            # Extraire le contenu de l'article en cherchant les balises <p>
            article_content = soup.find_all("p")
            article_text = "\n".join([paragraph.get_text().strip() for paragraph in article_content])
            
            # Afficher le titre et le contenu de l'article
            #print(f"Fichier : {filename}")
            #print("Titre de l'article :")
            #print(title)
            doc_final.loc[len(doc_final)] = [filename, title, categ]
            #print(doc_final)
            # print("\nContenu de l'article :")
            #print(article_text)
            # print("\n" + "="*80 + "\n")  # Séparateur entre les articles



# Exporter le DataFrame en fichier CSV
doc_final.to_csv('donnees_labelisees_test.csv', index=False)
