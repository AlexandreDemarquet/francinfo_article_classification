# francinfo_article_classification


projet MODIA
Extraction des titres et texte des articles du site FranceInfo dans différentes catégorie (monde, sport, culture, politique, ect, ...)

On crawl dans une page franceinfo et on telecharge toutes les pages html en multicpu en exectutant la commande suivante:
./crawler_multi_cpu.sh  ici on enregistre (10 pages par categorie dans l'exmple à modifier dans crawler2.py)

qui enregistre en parallèles dans un dossier data_brute_html les html

on peut extraire les titres de chaque page html avec le fichier python extraction_titre_html_file.py ou dans l'exemple il extrait les titres de pages html enregistré dans la categorie monde. 