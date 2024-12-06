import requests
from bs4 import BeautifulSoup
import time
import os
from urllib.parse import urljoin, urlparse, urlunparse
import sys
import hashlib

# Catégorie passée en argument
categorie = sys.argv[1]
base_url = f"https://www.francetvinfo.fr/{categorie}/"
output_dir = f"../data_brute_html/{categorie}"
os.makedirs(output_dir, exist_ok=True)
visited_urls = set()

def clean_url(url):
    """Supprime les fragments et paramètres pour éviter les doublons"""
    parsed_url = urlparse(url)
    clean_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, "", "", ""))
    return clean_url

def get_file_name_from_url(url, output_dir):
    """Crée un nom de fichier unique basé sur le hash de l'URL pour éviter les doublons"""
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(output_dir, f"{url_hash}.html")

def crawl(url, max_pages=50):
    pages_crawled = 0
    urls_to_crawl = [url]
    
    while urls_to_crawl and pages_crawled < max_pages:
        current_url = urls_to_crawl.pop(0)
        clean_current_url = clean_url(current_url)
        
        # Vérifier si l'URL a déjà été visitée
        if clean_current_url in visited_urls:
            continue

        try:
            response = requests.get(current_url, timeout=10)
            response.raise_for_status()
            
        except requests.exceptions.SSLError as ssl_error:
            print(f"Erreur SSL rencontrée pour {current_url}. Nouvel essai...")
            time.sleep(5)
            continue  # Passer à l'URL suivante
        
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la connexion à {current_url}: {e}")
            continue

        # Ajouter l'URL nettoyée à l'ensemble des URLs visitées
        visited_urls.add(clean_current_url)
        pages_crawled += 1
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Enregistrer la page dans un fichier avec un nom unique
        file_path = get_file_name_from_url(current_url, output_dir)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(soup.prettify())
        
        print(f"Téléchargé et enregistré : {file_path}")

        # Ajouter de nouvelles URLs à visiter
        for link in soup.find_all("a", href=True):
            full_url = urljoin(base_url, link['href'])
            clean_full_url = clean_url(full_url)
            if base_url in full_url and clean_full_url not in visited_urls:
                urls_to_crawl.append(full_url)

        time.sleep(1)

crawl(base_url, max_pages=800)
