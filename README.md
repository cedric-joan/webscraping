# Apprenez le webscraping avec Python

Projet servant de fil rouge au cours Apprenez le webscraping avec Python, disponible sur OpenClassrooms. 

Nous allons extraire et enregistrer les données d'un site web. Nous cherchons à extraire :
- à partir d'un livre extraire les inforations suivantes: categorie, titre, description, prix, image...  
- à partir d'une catégorie extraire tous les livres et les enregrister dans un fichier csv.
- extraire toutes les livres de toutes les catégories et enregistrer chaque catégorie dans un fichier csv distinct.
- extraire toutes les livres de toutes les catégories et enregistrer toutes les données dans un fichier.
- télécharger les images de tous les livres de toutes les catégories et les sauvegarder localement.


# Installation des paquets

Créer un environnement virtuel, utiliser la commande : python -m venv env
Pour activer l'environnement, exécuter: env/bin/activate ou env/Scripts/activate.bat (sous Windows).

Pour extraire des données, vous allez avoir besoin d'installer `requests` et `BeautifulSoup4` :

    pip install requests
    pip install bs4

Enfin vérifier les versions des paquets installés (ils doivent correspondre au fichier requirements) en exécutant :

    pip freeze     

# Données

url du site internet :http://books.toscrape.com/

# Lancer le programme


    ./scrap_books.py
