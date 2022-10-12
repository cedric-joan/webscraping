import requests
from bs4 import BeautifulSoup
import csv

# url de la page
page_book_url = "http://books.toscrape.com/catalogue/the-dirty-little-secrets-of-getting-your-dream-job_994/"

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

page_category_url = "http://books.toscrape.com/catalogue/category/books/music_14/"

# requête pour accéder à la page d'une catégorie
def get_content_page_category():
    reponse = requests.get(page_category_url)
    page_category = reponse.content
    return page_category

soup_category = BeautifulSoup(get_content_page_category(), "html.parser")


def get_all_books_urls():
    anchors = soup_category.find_all("div", class_="image_container")
    book_links = []
    for anchor in anchors:
        links = anchor.find("a")["href"]
        links = requests.compat.urljoin(page_category_url, links)
        book_links.append(links)
    return book_links
get_all_books_urls()

# création d'en-tête
headers_data = ["product_page_url","category", "title", "product_description", "universal_product_code", "price_excluding_tax", "price_including_tax", "number_available", "review_rating", "image_url"]
data_one_book = [get_book_url(),get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]

# écrire les données pour un livre et une catégorie dans un fichier csv
with open("data_book.csv", "w") as file_csv:
    writer = csv.writer(file_csv, delimiter=",")
    writer.writerow(headers_data)
    writer.writerow(data_one_book)
    books = get_all_books_urls()
    for book in books:
        r = requests.get(book)
        soup = BeautifulSoup(r.content, "html.parser")
        book = [ book, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
        books_list = book
        writer.writerow(books_list)

# extraction de toutes les urls de toutes les catégories de la page d'accueil
home_page_url = "http://books.toscrape.com"

def get_content_home_page():
    reponse = requests.get(home_page_url)
    home_page_category = reponse.content
    return home_page_category

soup_home = BeautifulSoup(get_content_home_page(), "html.parser")    

def get_all_links_categories():
    anc = soup_home.find("ul", class_="nav")
    links = anc.find_all("a")
    links_categories = []
    for link in links:
        liens = link["href"]
        liens = requests.compat.urljoin(home_page_url, liens)
        links_categories.append(liens)
    return links_categories

def get_travel_category_url():
    travel_link = get_all_links_categories()
    return travel_link[1]

# écrire les données pour la catégorie  travel dans un fichier 
with open("travel_category.csv", "w") as file_csv:
    writer = csv.writer(file_csv, delimiter=",")
    writer.writerow(headers_data)
    travels = get_travel_category_url()
    res = requests.get(travels)
    soup_category = BeautifulSoup(res.content, "html.parser")
    travels = get_all_books_urls()
    for travel in travels:
        r = requests.get(travel)
        soup = BeautifulSoup(r.content, "html.parser")
        travel = [travel, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
        writer.writerow(travel)
    
def get_mustery_category_url():
    mustery_link = get_all_links_categories()
    return mustery_link[2]

# écrire les données pour la catégorie  mytery dans un fichier 
with open("mustery_category.csv", "w") as file_csv:
    writer = csv.writer(file_csv, delimiter=",")
    writer.writerow(headers_data)
    musterys = get_mustery_category_url()
    res = requests.get(musterys)
    soup_category = BeautifulSoup(res.content, "html.parser")
    cur_page = soup_category.find("li", class_="next")
    cur_href = cur_page.find("a")["href"]
    next_pag = cur_href
    for i in range(1,3):
        next_pag = requests.compat.urljoin(musterys, "page-" + str(i) +".html" )
        urls_pages = []
        urls_pages.append(next_pag)
        for urls in urls_pages:
            r = requests.get(urls)
            soup_category = BeautifulSoup(r.content, "html.parser")
            urls = get_all_books_urls()
            for urls_books_mustery in urls:
                r = requests.get(urls_books_mustery)
                soup = BeautifulSoup(r.content, "html.parser")
                urls_books_mustery = [ urls_books_mustery, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
                writer.writerow(urls_books_mustery)


def get_historical_fiction_category_url():
    historical_fiction_link = get_all_links_categories()
    return historical_fiction_link[3]

# # # écrire les données pour la catégorie historical fiction dans un fichier
with open("historical_fiction_category.csv", "w") as file_csv:
    writer = csv.writer(file_csv, delimiter=",")
    writer.writerow(headers_data)
    historical_fictions = get_historical_fiction_category_url()
    res = requests.get(historical_fictions)
    soup_category = BeautifulSoup(res.content, "html.parser")
    cur_page = soup_category.find("li", class_="next")
    cur_href = cur_page.find("a")["href"]
    next_pag = cur_href
    for i in range(1,3):
        next_pag = requests.compat.urljoin(historical_fictions, "page-" + str(i) +".html" )
        urls_pages = []
        urls_pages.append(next_pag)
        for urls in urls_pages:
            r = requests.get(urls)
            soup_category = BeautifulSoup(r.content, "html.parser")
            urls = get_all_books_urls()
            for urls_books_historical_fictions in urls:
                r = requests.get(urls_books_historical_fictions)
                soup = BeautifulSoup(r.content, "html.parser")
                urls_books_historical_fictions = [ urls_books_historical_fictions, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
                writer.writerow(urls_books_historical_fictions)
        
# def get sequential_art_category_url():
#     sequential_art_link = get_all_links_categories()
#     return sequential_art_link[4]

# # écrire les données pour la catégorie sequential art dans un fichier
# with open("sequential_art_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     sequential_arts = get_sequential_art_category_url()
#     res = requests.get(sequential_arts)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     cur_page = soup_category.find("li", class_="next")
#     cur_href = cur_page.find("a")["href"]
#     next_pag = cur_href
#     for i in range(1,5):
#         next_pag = requests.compat.urljoin(sequential_arts, "page-" + str(i) +".html" )
#         urls_pages = []
#         urls_pages.append(next_pag)
#         for urls in urls_pages:
#             r = requests.get(urls)
#             soup_category = BeautifulSoup(r.content, "html.parser")
#             sequential_arts = get_all_books_urls()
#             for sequential_art in sequential_arts:
#                 r = requests.get(sequential_art)
#                 soup = BeautifulSoup(r.content, "html.parser")
#                 sequential_art = [ sequential_art ,get_book_url(), get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#                 writer.writerow(sequential_art)
        
# def get_classic_category_url():
#     classic_link = get_all_links_categories()
#     return classic_link[5]

# # écrire les données pour la catégorie classic dans un fichier
# with open("classic_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     classics = get_classic_category_url()
#     res = requests.get(classics)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     classics = get_all_books_urls()
#     for classic in classics:
#         r = requests.get(classic)
#         soup = BeautifulSoup(r.content, "html.parser")
#         classic = [ get_book_url(), get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(classic)
        
# def get_philosophy_category_url():
#     philosophy_link = get_all_links_categories()
#     return philosophy_link[6]

# # écrire les données pour la catégorie philosophy dans un fichier
# with open("philosophy_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     philosophys = get_philosophy_category_url()
#     res = requests.get(philosophys)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     philosophys = get_all_books_urls()
#     for philosophy in philosophys:
#         r = requests.get(philosophy)
#         soup = BeautifulSoup(r.content, "html.parser")
#         philosophy = [ get_book_url(), get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(philosophy)
        
# def get_romance_category_url():
#     romance_link = get_all_links_categories()
#     return romance_link[7]

# # écrire les données pour la catégorie romance dans un fichier
# with open("romance_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     romances = get_romance_category_url()
#     res = requests.get(romances)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     romances = get_all_books_urls()
#     for romance in romances:
#         r = requests.get(romance)
#         soup = BeautifulSoup(r.content, "html.parser")
#         romance = [ get_book_url(), get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(romance)
        
# def womens_fiction_category_url():
#     womens_fiction_link = get_all_links_categories()
#     return womens_fiction_link[7]
# womens_fiction_category_url()    

# # écrire les données pour la catégorie womens fiction dans un fichier
# with open("womens_fiction_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     womens_fictions = womens_fiction_category_url()
#     res = requests.get(womens_fictions)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     womens_fictions = get_all_books_urls()
#     for womens_fiction in womens_fictions:
#         r = requests.get(womens_fiction)
#         soup = BeautifulSoup(r.content, "html.parser")
#         womens_fiction = [ get_book_url(), get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(womens_fiction)
        
# def fiction_category_url():
#     fiction_link = get_all_links_categories()
#     return fiction_link[9]
# fiction_category_url()    

# # écrire les données pour la catégorie fiction dans un fichier
# with open("fiction_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     fictions = fiction_category_url()
#     res = requests.get(fictions)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     fictions = get_all_books_urls()
#     for fiction in fictions:
#         r = requests.get(fiction)
#         soup = BeautifulSoup(r.content, "html.parser")
#         fiction = [ get_book_url(), get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(fiction)
        
# def children_category_url():
#     children_link = get_all_links_categories()
#     return children_link[10]
# children_category_url()    

# # écrire les données pour la catégorie children dans un fichier
# with open("children_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     childrens = children_category_url()
#     res = requests.get(childrens)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     childrens = get_all_books_urls()
#     for children in childrens:
#         r = requests.get(children)
#         soup = BeautifulSoup(r.content, "html.parser")
#         children = [ get_book_url(), get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(children)
        
# def travel_category_url():
#     travel_link = get_all_links_categories()
#     return travel_link[11]
# travel_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("travel_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     travels = travel_category_url()
#     res = requests.get(travels)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     travels = get_all_books_urls()
#     for travel in travels:
#         r = requests.get(travel)
#         soup = BeautifulSoup(r.content, "html.parser")
#         travel = [ get_book_url(), get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(travel)
        
# def travel_category_url():
#     travel_link = get_all_links_categories()
#     return travel_link[12]
# travel_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("travel_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     travels = travel_category_url()
#     res = requests.get(travels)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     travels = get_all_books_urls()
#     for travel in travels:
#         r = requests.get(travel)
#         soup = BeautifulSoup(r.content, "html.parser")
#         travel = [ get_book_url(), get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(travel)
        
# def travel_category_url():
#     travel_link = get_all_links_categories()
#     return travel_link[13]
# travel_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("travel_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     travels = travel_category_url()
#     res = requests.get(travels)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     travels = get_all_books_urls()
#     for travel in travels:
#         r = requests.get(travel)
#         soup = BeautifulSoup(r.content, "html.parser")
#         travel = [ get_book_url(), get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(travel)
        
# def travel_category_url():
#     travel_link = get_all_links_categories()
#     return travel_link[14]
# travel_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("travel_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     travels = travel_category_url()
#     res = requests.get(travels)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     travels = get_all_books_urls()
#     for travel in travels:
#         r = requests.get(travel)
#         soup = BeautifulSoup(r.content, "html.parser")
#         travel = [ get_book_url(), get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(travel)
        
# def travel_category_url():
#     travel_link = get_all_links_categories()
#     return travel_link[15]
# travel_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("travel_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     travels = travel_category_url()
#     res = requests.get(travels)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     travels = get_all_books_urls()
#     for travel in travels:
#         r = requests.get(travel)
#         soup = BeautifulSoup(r.content, "html.parser")
#         travel = [ get_book_url(), get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(travel)
        
# def travel_category_url():
#     travel_link = get_all_links_categories()
#     return travel_link[16]
# travel_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("travel_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     travels = travel_category_url()
#     res = requests.get(travels)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     travels = get_all_books_urls()
#     for travel in travels:
#         r = requests.get(travel)
#         soup = BeautifulSoup(r.content, "html.parser")
#         travel = [ get_book_url(), get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(travel)

# def travel_category_url():
#     travel_link = get_all_links_categories()
#     return travel_link[17]
# travel_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("travel_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     travels = travel_category_url()
#     res = requests.get(travels)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     travels = get_all_books_urls()
#     for travel in travels:
#         r = requests.get(travel)
#         soup = BeautifulSoup(r.content, "html.parser")
#         travel = [ get_book_url(), get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(travel)
        
# def travel_category_url():
#     travel_link = get_all_links_categories()
#     return travel_link[18]
# travel_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("travel_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     travels = travel_category_url()
#     res = requests.get(travels)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     travels = get_all_books_urls()
#     for travel in travels:
#         r = requests.get(travel)
#         soup = BeautifulSoup(r.content, "html.parser")
#         travel = [ get_book_url(), get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(travel)        








