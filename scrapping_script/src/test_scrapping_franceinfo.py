import requests
from bs4 import BeautifulSoup

# URL de la page
url = "https://www.francetvinfo.fr/monde/environnement/crise-climatique/baisse-des-emissions-deploiement-des-renouvelables-renovations-la-france-devoile-sa-nouvelle-feuille-de-route-pour-le-climat-et-l-energie_6877433.html"

# Faire une requête GET
response = requests.get(url)
response.raise_for_status()

# Parser le contenu de la page avec BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Extraire le titre de l'article (souvent dans une balise <h1>)
title = soup.find("h1").get_text()

# Extraire le contenu de l'article en cherchant les balises <p>
article_content = soup.find_all("p")
article_text = "\n".join([paragraph.get_text() for paragraph in article_content])

print("Titre de l'article :")
print(title)
print("\nContenu de l'article :")
print(article_text)
