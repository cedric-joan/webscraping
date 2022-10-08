import requests
from bs4 import BeautifulSoup
import csv

# url de la page
page_book_url = "http://books.toscrape.com/catalogue/the-dirty-little-secrets-of-getting-your-dream-job_994/index.html"

# requête pour accéder à la page du livre
def get_content_page_book():
    reponse = requests.get(page_book_url)
    page_book = reponse.content
    return page_book

# parser la page
soup = BeautifulSoup(get_content_page_book(), "html.parser")

# catégorie du livre
def get_caterogy():
    anchors = soup.find_all("a")
    book_category = []
    for anchor in anchors:
        category = anchor.text
        book_category.append(category)
    return book_category[3] 
get_caterogy()

# url du livre
def get_book_url():
    anchors = soup.find_all("a")
    book_links = []
    for anchor in anchors:
        link = anchor["href"]
        link = requests.compat.urljoin(page_book_url, link)
        book_links.append(link)
    return book_links[3]
get_book_url() 

# image du livre
def get_image_url():
    image = soup.select("img")
    src = image[0]["src"]
    src = requests.compat.urljoin(page_book_url,src)
    img_url = src
    return img_url 
get_image_url()    

# titre du livre
def get_title():
    book_title = soup.h1.string
    return book_title
get_title()

# description du livre
def get_description():
    descriptions = soup.find_all("p")
    description_text = []
    for description in descriptions:
        description_text.append(description.text)
    return description_text[3]
get_description()

# informations du livre
def get_informations():
    informations = soup.find_all("td")
    book_informations = []
    for information in informations:
        book_informations.append(information.text)
    return book_informations

def get_upc():
    univers = get_informations()
    return univers[0]
get_upc()

def get_price_excl():
    price_ex = get_informations()
    return price_ex[2]
get_price_excl()  

def get_price_in():
    price_in = get_informations()
    return price_in[3]
get_price_in()

def get_num_available():
    num_av = get_informations()
    return num_av[5]
get_num_available()

def get_rev_rating():
    rev_rating = get_informations()
    return rev_rating[6]
get_rev_rating() 

page_category_url = "http://books.toscrape.com/catalogue/category/books/music_14/index.html"

# requête pour accéder à la page d'une catégorie
def get_content_page_category():
    reponse = requests.get(page_category_url)
    page_category = reponse.content
    return page_category

soup_category = BeautifulSoup(get_content_page_category(), "html.parser")

# urls des livres d'une catégorie
def get_all_books_urls():
    anchors = soup_category.find_all("div", class_="image_container")
    book_links = []
    for anchor in anchors:
        links = anchor.find("a")["href"]
        links = requests.compat.urljoin(page_category_url, links)
        book_links.append(links)
    return book_links

# création d'en-tête
headers_data = ["product_page_url","category", "title", "product_description", "universal_product_code", "price_excluding_tax", "price_including_tax", "number_available", "review_rating", "image_url"]
data_list = [get_book_url(),get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]

# écrire les données dans un fichier csv
# with open("data_book.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     writer.writerow(data_list)
#     books = get_all_books_urls()
#     for book in books:
#         r = requests.get(book)
#         soup = BeautifulSoup(r.content, "html.parser")
#         book = [ get_book_url(), get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         books_list = book
#         writer.writerow(books_list)


def get_all_categories():
    anc = soup_category.find("ul", class_="nav")
    links = anc.find_all("a")
    for link in links:
        links_categories = []
        liens = link["href"]
        liens = requests.compat.urljoin(page_category_url, liens)
        links_categories.append(liens)
    return links_categories



get_all_categories()        





