from unicodedata import category
import requests
from bs4 import BeautifulSoup

# url de la page
page_url = "http://books.toscrape.com/catalogue/the-dirty-little-secrets-of-getting-your-dream-job_994/index.html"

# requête pour accéder à la page du livre
def get_content_page():
    reponse = requests.get(page_url)
    page = reponse.content
    return page
get_content_page()

# parser la page
soup = BeautifulSoup(get_content_page(), "html.parser")

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
        link = requests.compat.urljoin(page_url, link)
        book_links.append(link)
    return book_links[3]
get_book_url() 

# image du livre
def get_image_url():
    image = soup.select("img")
    src = image[0]["src"]
    src = requests.compat.urljoin(page_url, src)
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
informations = soup.find_all("td")
book_informations = []
for information in informations:
    book_informations.append(information.text)
upc = book_informations[0]    
price_excl = book_informations[2]    
price_incl = book_informations[3]    
num_available = book_informations[5]    
rev_rating = book_informations[6]    