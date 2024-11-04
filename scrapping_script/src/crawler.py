import requests
from bs4 import BeautifulSoup
import time
import os
from urllib.parse import urljoin
import sys





categorie = sys.argv[1]

base_url = f"https://www.francetvinfo.fr/{categorie}/"
output_dir = f"../../data_brute_html/{categorie}"
os.makedirs(output_dir, exist_ok=True)
visited_urls = set()

def crawl(url, max_pages=50):
    pages_crawled = 0
    urls_to_crawl = [url]
    
    while urls_to_crawl and pages_crawled < max_pages:
        current_url = urls_to_crawl.pop(0)
        
        if current_url in visited_urls:
            continue
        
        try:
            #faire la requête GET avec une limite de temps pour éviter le blocage 
            response = requests.get(current_url, timeout=10)
            response.raise_for_status()
            
        except requests.exceptions.SSLError as ssl_error:
            print(f"Erreur SSL rencontrée pour {current_url}. Nouvel essai...")
            time.sleep(5)
            continue  # Passer à l'URL suivante
        
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la connexion à {current_url}: {e}")
            continue
        
        visited_urls.add(current_url)
        pages_crawled += 1
        soup = BeautifulSoup(response.text, "html.parser")
        
        file_path = os.path.join(output_dir, f"page_{pages_crawled}.html")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(soup.prettify())
        
        print(f"Téléchargé et enregistré : {file_path}")

        for link in soup.find_all("a", href=True):
            full_url = urljoin(base_url, link['href'])
            if base_url in full_url and full_url not in visited_urls:
                urls_to_crawl.append(full_url)

        time.sleep(2)

crawl(base_url, max_pages=50)
