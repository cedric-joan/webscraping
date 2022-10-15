import requests
from bs4 import BeautifulSoup
import csv
import os
import shutil

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

# url du livre
def get_book_url():
    anchors = soup.find_all("a")
    book_links = []
    for anchor in anchors:
        link = anchor["href"]
        link = requests.compat.urljoin(page_book_url, link)
        book_links.append(link)
    return book_links[3]

# titre du livre
def get_title():
    book_title = soup.h1.string
    return book_title

# image du livre
# def create_dir():
#     name_dir = get_caterogy()
#     os.mkdir(os.path.join(os.getcwd(), name_dir))
#     return path
 
def get_image_url():
    image = soup.select("img")
    src = image[0]["src"]
    src = requests.compat.urljoin(page_book_url,src)
    img_url = src
    return img_url 

def download_picture():
    img_book = get_image_url()
    img_data = requests.get(img_book).content
    name_book = get_title()
    with open(name_book.replace(":", ",") + ".jpg", "wb") as handler:
        handler.write(img_data)

# description du livre

def get_description():
    description_none = "pas de description"
    product_desc = soup.select_one("article.product_page>p")
    if not product_desc:
        return description_none
    else:
        return product_desc.text
    

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

def get_price_excl():
    price_ex = get_informations()
    return price_ex[2]

def get_price_in():
    price_in = get_informations()
    return price_in[3]

def get_num_available():
    num_av = get_informations()
    return num_av[5]

def get_rev_rating():
    rev_rating = get_informations()
    return rev_rating[6]

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
one_book_data = [ get_book_url() , get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]

# écrire les données pour un livre et une catégorie dans un fichier csv
with open("data_book.csv", "w") as file_csv:
    writer = csv.writer(file_csv, delimiter=",")
    writer.writerow(headers_data)
    writer.writerow(one_book_data)
    musics = get_all_books_urls()
    for music in musics:
        r = requests.get(music)
        soup = BeautifulSoup(r.content, "html.parser")
        music = [ music , get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url(), download_picture()]
        writer.writerow(music)

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



# # écrire les données pour la catégorie  travel dans un fichier 
# categ = get_all_links_categories()
# for cate in categ :
#     cate_file_name = str(cate) + ".csv"
#     with open(cate_file_name, "w") as file_csv:
#         writer = csv.writer(file_csv, delimiter=",")
#         writer.writerow(headers_data)



        # travels = get_travel_category_url()
        # res = requests.get(travels)
        # soup_category = BeautifulSoup(res.content, "html.parser")
        # travels = get_all_books_urls()
        # for travel in travels:
        #     r = requests.get(travel)
        #     soup = BeautifulSoup(r.content, "html.parser")
        #     travel = [travel, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
        #     writer.writerow(travel)
    
# def get_travel_category_url():
#     travel_link = get_all_links_categories()
#     return travel_link[1]

# def get_mustery_category_url():
#     mustery_link = get_all_links_categories()
#     return mustery_link[2]

# # # # # écrire les données pour la catégorie  mytery dans un fichier 
# with open("mustery_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     musterys = get_mustery_category_url()
#     res = requests.get(musterys)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     cur_page = soup_category.find("li", class_="next")
#     cur_href = cur_page.find("a")["href"]
#     next_pag = cur_href
#     for i in range(1,3):
#         next_pag = requests.compat.urljoin(musterys, "page-" + str(i) +".html" )
#         urls_pages = []
#         urls_pages.append(next_pag)
#         for urls in urls_pages:
#             r = requests.get(urls)
#             soup_category = BeautifulSoup(r.content, "html.parser")
#             urls = get_all_books_urls()
#             for urls_books_mustery in urls:
#                 r = requests.get(urls_books_mustery)
#                 soup = BeautifulSoup(r.content, "html.parser")
#                 urls_books_mustery = [ urls_books_mustery, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#                 writer.writerow(urls_books_mustery)


# def get_historical_fiction_category_url():
#     historical_fiction_link = get_all_links_categories()
#     return historical_fiction_link[3]

# # # # # écrire les données pour la catégorie historical fiction dans un fichier
# with open("historical_fiction_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     historical_fictions = get_historical_fiction_category_url()
#     res = requests.get(historical_fictions)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     cur_page = soup_category.find("li", class_="next")
#     cur_href = cur_page.find("a")["href"]
#     next_pag = cur_href
#     for i in range(1,3):
#         next_pag = requests.compat.urljoin(historical_fictions, "page-" + str(i) +".html" )
#         urls_pages = []
#         urls_pages.append(next_pag)
#         for urls in urls_pages:
#             r = requests.get(urls)
#             soup_category = BeautifulSoup(r.content, "html.parser")
#             urls = get_all_books_urls()
#             for urls_books_historical_fictions in urls:
#                 r = requests.get(urls_books_historical_fictions)
#                 soup = BeautifulSoup(r.content, "html.parser")
#                 urls_books_historical_fictions = [ urls_books_historical_fictions, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#                 writer.writerow(urls_books_historical_fictions)
        
# def get_sequential_art_category_url():
#     sequential_art_link = get_all_links_categories()
#     return sequential_art_link[4]

# # # écrire les données pour la catégorie sequential art dans un fichier
# with open("sequential_art_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     sequential_arts = get_sequential_art_category_url()
#     res = requests.get(sequential_arts)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     cur_page = soup_category.find("li", class_="next")
#     cur_href = cur_page.find("a")["href"]
#     next_pag = cur_href
#     for i in range(1,5):
#         next_pag = requests.compat.urljoin("http://books.toscrape.com/catalogue/category/books/sequential-art_5/", "page-" + str(i) +".html" )
#         urls_pages = []
#         urls_pages.append(next_pag)
#         for urls in urls_pages:
#             r = requests.get(urls)
#             soup_category = BeautifulSoup(r.content, "html.parser")
#             urls = get_all_books_urls()
#             for urls_books_sequential in urls:
#                 r = requests.get(urls_books_sequential)
#                 soup = BeautifulSoup(r.content, "html.parser")
#                 urls_books_sequential = [ urls_books_sequential, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#                 writer.writerow(urls_books_sequential)

# def get_classic_category_url():
#     classic_link = get_all_links_categories()
#     return classic_link[5]

# # # # # écrire les données pour la catégorie classic dans un fichier
# with open("classic_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     classics = get_classic_category_url()
#     res = requests.get(classics)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     classics = get_all_books_urls()
#     for classic in classics:
#         r = requests.get(classic)
#         soup = BeautifulSoup(r.content, "html.parser")
#         classic = [ classic, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(classic)
        
# def get_philosophy_category_url():
#     philosophy_link = get_all_links_categories()
#     return philosophy_link[6]

# # # écrire les données pour la catégorie philosophy dans un fichier
# with open("philosophy_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     philosophys = get_philosophy_category_url()
#     res = requests.get(philosophys)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     philosophys = get_all_books_urls()
#     for philosophy in philosophys:
#         r = requests.get(philosophy)
#         soup = BeautifulSoup(r.content, "html.parser")
#         philosophy = [ philosophy, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(philosophy)
        
# def get_romance_category_url():
#     romance_link = get_all_links_categories()
#     return romance_link[7]

# # # écrire les données pour la catégorie romance dans un fichier
# with open("romance_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     romances = get_romance_category_url()
#     res = requests.get(romances)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     cur_page = soup_category.find("li", class_="next")
#     cur_href = cur_page.find("a")["href"]
#     next_pag = cur_href
#     for i in range(1,3):
#         next_pag = requests.compat.urljoin(romances, "page-" + str(i) +".html" )
#         urls_pages = []
#         urls_pages.append(next_pag)
#         for urls in urls_pages:
#             r = requests.get(urls)
#             soup_category = BeautifulSoup(r.content, "html.parser")
#             urls = get_all_books_urls()
#             for urls_books_romance in urls:
#                 r = requests.get(urls_books_romance)
#                 soup = BeautifulSoup(r.content, "html.parser")
#                 urls_books_romance = [ urls_books_romance, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#                 writer.writerow(urls_books_romance)
        
# def womens_fiction_category_url():
#     womens_fiction_link = get_all_links_categories()
#     return womens_fiction_link[8]
# womens_fiction_category_url()    

# # # écrire les données pour la catégorie womens fiction dans un fichier
# with open("womens_fiction_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     womens_fictions = womens_fiction_category_url()
#     res = requests.get(womens_fictions)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     womens_fictions = get_all_books_urls()
#     for womens_fiction in womens_fictions:
#         r = requests.get(womens_fiction)
#         soup = BeautifulSoup(r.content, "html.parser")
#         womens_fiction = [ womens_fiction, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(womens_fiction)
        
# def fiction_category_url():
#     fiction_link = get_all_links_categories()
#     return fiction_link[9]
# fiction_category_url()    

# # écrire les données pour la catégorie fiction dans un fichier
# with open("fiction_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     fictions = fiction_category_url()
#     res = requests.get(fictions)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     cur_page = soup_category.find("li", class_="next")
#     cur_href = cur_page.find("a")["href"]
#     next_pag = cur_href
#     for i in range(1,5):
#         next_pag = requests.compat.urljoin("http://books.toscrape.com/catalogue/category/books/fiction_10/", "page-" + str(i) +".html" )
#         urls_pages = []
#         urls_pages.append(next_pag)
#         for urls in urls_pages:
#             r = requests.get(urls)
#             soup_category = BeautifulSoup(r.content, "html.parser")
#             urls = get_all_books_urls()
#             for fiction in urls:
#                 r = requests.get(fiction)
#                 soup = BeautifulSoup(r.content, "html.parser")
#                 fiction = [ fiction, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#                 writer.writerow(fiction)
        
# def children_category_url():
#     children_link = get_all_links_categories()
#     return children_link[10]
# children_category_url()    

# # # écrire les données pour la catégorie children dans un fichier
# with open("children_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     childrens = children_category_url()
#     res = requests.get(childrens)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     cur_page = soup_category.find("li", class_="next")
#     cur_href = cur_page.find("a")["href"]
#     next_pag = cur_href
#     for i in range(1,3):
#         next_pag = requests.compat.urljoin(childrens, "page-" + str(i) +".html" )
#         urls_pages = []
#         urls_pages.append(next_pag)
#         for urls in urls_pages:
#             r = requests.get(urls)
#             soup_category = BeautifulSoup(r.content, "html.parser")
#             urls = get_all_books_urls()
#             for children in urls:
#                 r = requests.get(children)
#                 soup = BeautifulSoup(r.content, "html.parser")
#                 children = [ children, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#                 writer.writerow(children)
        
# def religion_category_url():
#     religion_link = get_all_links_categories()
#     return religion_link[11]
# religion_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("religion_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     religions = religion_category_url()
#     res = requests.get(religions)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     religions = get_all_books_urls()
#     for religion in religions:
#         r = requests.get(religion)
#         soup = BeautifulSoup(r.content, "html.parser")
#         religion = [ religion, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(religion)

# def non_fiction_category_url():
#     non_fiction_link = get_all_links_categories()
#     return non_fiction_link[12]
# non_fiction_category_url()    

# # écrire les données pour la catégorie non_fiction dans un fichier
# with open("non_fiction_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     non_fictions = non_fiction_category_url()
#     res = requests.get(non_fictions)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     cur_page = soup_category.find("li", class_="next")
#     cur_href = cur_page.find("a")["href"]
#     next_pag = cur_href
#     for i in range(1,7):
#         next_pag = requests.compat.urljoin("http://books.toscrape.com/catalogue/category/books/nonfiction_13/", "page-" + str(i) +".html" )
#         urls_pages = []
#         urls_pages.append(next_pag)
#         for urls in urls_pages:
#             r = requests.get(urls)
#             soup_category = BeautifulSoup(r.content, "html.parser")
#             urls = get_all_books_urls()
#             for non_fiction in urls:
#                 r = requests.get(non_fiction)
#                 soup = BeautifulSoup(r.content, "html.parser")
#                 non_fiction = [ non_fiction, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#                 writer.writerow(non_fiction)

# def default_category_url():
#     default_link = get_all_links_categories()
#     return default_link[14]
# default_category_url()    

# # écrire les données pour la catégorie default dans un fichier
# with open("default_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     defaults = default_category_url()
#     res = requests.get(defaults)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     cur_page = soup_category.find("li", class_="next")
#     cur_href = cur_page.find("a")["href"]
#     next_pag = cur_href
#     for i in range(1,9):
#         next_pag = requests.compat.urljoin("http://books.toscrape.com/catalogue/category/books/default_15/", "page-" + str(i) +".html" )
#         urls_pages = []
#         urls_pages.append(next_pag)
#         for urls in urls_pages:
#             r = requests.get(urls)
#             soup_category = BeautifulSoup(r.content, "html.parser")
#             urls = get_all_books_urls()
#             for default in urls:
#                 r = requests.get(default)
#                 soup = BeautifulSoup(r.content, "html.parser")
#                 default = [ default, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#                 writer.writerow(default)

# def science_fiction_category_url():
#     science_fiction_link = get_all_links_categories()
#     return science_fiction_link[15]
# science_fiction_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("science_fiction_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     science_fictions = science_fiction_category_url()
#     res = requests.get(science_fictions)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     science_fictions = get_all_books_urls()
#     for science_fiction in science_fictions:
#         r = requests.get(science_fiction)
#         soup = BeautifulSoup(r.content, "html.parser")
#         science_fiction = [ science_fiction, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(science_fiction)
        
# def sport_and_game_category_url():
#     sport_and_game_link = get_all_links_categories()
#     return sport_and_game_link[16]
# sport_and_game_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("sport_and_game_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     sport_and_games = sport_and_game_category_url()
#     res = requests.get(sport_and_games)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     sport_and_games = get_all_books_urls()
#     for sport_and_game in sport_and_games:
#         r = requests.get(sport_and_game)
#         soup = BeautifulSoup(r.content, "html.parser")
#         sport_and_game = [ sport_and_game, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(sport_and_game)

# def add_a_comment_category_url():
#     add_a_comment_link = get_all_links_categories()
#     return add_a_comment_link[17]
# add_a_comment_category_url()    

# # écrire les données pour la catégorie add_a_comment dans un fichier
# with open("add_a_comment_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     add_a_comments = add_a_comment_category_url()
#     res = requests.get(add_a_comments)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     cur_page = soup_category.find("li", class_="next")
#     cur_href = cur_page.find("a")["href"]
#     next_pag = cur_href
#     for i in range(1,5):
#         next_pag = requests.compat.urljoin("http://books.toscrape.com/catalogue/category/books/add-a-comment_18/", "page-" + str(i) +".html" )
#         urls_pages = []
#         urls_pages.append(next_pag)
#         for urls in urls_pages:
#             r = requests.get(urls)
#             soup_category = BeautifulSoup(r.content, "html.parser")
#             urls = get_all_books_urls()
#             for add_a_comment in urls:
#                 r = requests.get(add_a_comment)
#                 soup = BeautifulSoup(r.content, "html.parser")
#                 add_a_comment = [ add_a_comment, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#                 writer.writerow(add_a_comment)

# def fantasy_category_url():
#     fantasy_link = get_all_links_categories()
#     return fantasy_link[18]
# fantasy_category_url()    

# # écrire les données pour la catégorie fantasy dans un fichier
# with open("fantasy_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     fantasys = fantasy_category_url()
#     res = requests.get(fantasys)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     cur_page = soup_category.find("li", class_="next")
#     cur_href = cur_page.find("a")["href"]
#     next_pag = cur_href
#     for i in range(1,4):
#         next_pag = requests.compat.urljoin("http://books.toscrape.com/catalogue/category/books/fantasy_19/", "page-" + str(i) +".html" )
#         urls_pages = []
#         urls_pages.append(next_pag)
#         for urls in urls_pages:
#             r = requests.get(urls)
#             soup_category = BeautifulSoup(r.content, "html.parser")
#             urls = get_all_books_urls()
#             for fantasy in urls:
#                 r = requests.get(fantasy)
#                 soup = BeautifulSoup(r.content, "html.parser")
#                 fantasy = [ fantasy, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#                 writer.writerow(fantasy)


# def new_adult_category_url():
#     new_adult_link = get_all_links_categories()
#     return new_adult_link[19]
# new_adult_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("new_adult_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     new_adults = new_adult_category_url()
#     res = requests.get(new_adults)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     new_adults = get_all_books_urls()
#     for new_adult in new_adults:
#         r = requests.get(new_adult)
#         soup = BeautifulSoup(r.content, "html.parser")
#         new_adult = [ new_adult, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(new_adult)

# def young_adult_category_url():
#     young_adult_link = get_all_links_categories()
#     return young_adult_link[20]
# young_adult_category_url()    

# # écrire les données pour la catégorie young_adult dans un fichier
# with open("young_adult_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     young_adults = young_adult_category_url()
#     res = requests.get(young_adults)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     cur_page = soup_category.find("li", class_="next")
#     cur_href = cur_page.find("a")["href"]
#     next_pag = cur_href
#     for i in range(1,4):
#         next_pag = requests.compat.urljoin("http://books.toscrape.com/catalogue/category/books/young-adult_21/", "page-" + str(i) +".html" )
#         urls_pages = []
#         urls_pages.append(next_pag)
#         for urls in urls_pages:
#             r = requests.get(urls)
#             soup_category = BeautifulSoup(r.content, "html.parser")
#             urls = get_all_books_urls()
#             for young_adult in urls:
#                 r = requests.get(young_adult)
#                 soup = BeautifulSoup(r.content, "html.parser")
#                 young_adult = [ young_adult, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#                 writer.writerow(young_adult)

# def science_category_url():
#     science_link = get_all_links_categories()
#     return science_link[21]
# science_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("science_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     sciences = science_category_url()
#     res = requests.get(sciences)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     sciences = get_all_books_urls()
#     for science in sciences:
#         r = requests.get(science)
#         soup = BeautifulSoup(r.content, "html.parser")
#         science = [ science, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(science)
        
# def poetry_category_url():
#     poetry_link = get_all_links_categories()
#     return poetry_link[22]
# poetry_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("poetry_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     poetrys = poetry_category_url()
#     res = requests.get(poetrys)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     poetrys = get_all_books_urls()
#     for poetry in poetrys:
#         r = requests.get(poetry)
#         soup = BeautifulSoup(r.content, "html.parser")
#         poetry = [ poetry, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(poetry)

# def paranormal_category_url():
#     paranormal_link = get_all_links_categories()
#     return paranormal_link[23]
# paranormal_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("paranormal_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     paranormals = paranormal_category_url()
#     res = requests.get(paranormals)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     paranormals = get_all_books_urls()
#     for paranormal in paranormals:
#         r = requests.get(paranormal)
#         soup = BeautifulSoup(r.content, "html.parser")
#         paranormal = [ paranormal, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(paranormal)
        
# def art_category_url():
#     art_link = get_all_links_categories()
#     return art_link[24]
# art_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("art_category.csv", "w") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     arts = art_category_url()
#     res = requests.get(arts)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     arts = get_all_books_urls()
#     for art in arts:
#         r = requests.get(art)
#         soup = BeautifulSoup(r.content, "html.parser")
#         art = [ art, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(art)        

# def psychology_category_url():
#     psychology_link = get_all_links_categories()
#     return psychology_link[25]
# psychology_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("psychology_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     psychologys = psychology_category_url()
#     res = requests.get(psychologys)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     psychologys = get_all_books_urls()
#     for psychology in psychologys:
#         r = requests.get(psychology)
#         soup = BeautifulSoup(r.content, "html.parser")
#         psychology = [ psychology, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(psychology)

# def autobiography_category_url():
#     autobiography_link = get_all_links_categories()
#     return autobiography_link[26]
# autobiography_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("autobiography_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     autobiographys = autobiography_category_url()
#     res = requests.get(autobiographys)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     autobiographys = get_all_books_urls()
#     for autobiography in autobiographys:
#         r = requests.get(autobiography)
#         soup = BeautifulSoup(r.content, "html.parser")
#         autobiography = [ autobiography, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(autobiography)

# def parenting_category_url():
#     parenting_link = get_all_links_categories()
#     return parenting_link[27]
# parenting_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("parenting_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     parentings = parenting_category_url()
#     res = requests.get(parentings)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     parentings = get_all_books_urls()
#     for parenting in parentings:
#         r = requests.get(parenting)
#         soup = BeautifulSoup(r.content, "html.parser")
#         parenting = [ parenting, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(parenting)

# def adult_fiction_category_url():
#     adult_fiction_link = get_all_links_categories()
#     return adult_fiction_link[28]
# adult_fiction_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("adult_fiction_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     adult_fictions = adult_fiction_category_url()
#     res = requests.get(adult_fictions)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     adult_fictions = get_all_books_urls()
#     for adult_fiction in adult_fictions:
#         r = requests.get(adult_fiction)
#         soup = BeautifulSoup(r.content, "html.parser")
#         adult_fiction = [ adult_fiction, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(adult_fiction)

# def humor_category_url():
#     humor_link = get_all_links_categories()
#     return humor_link[29]
# humor_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("humor_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     humors = humor_category_url()
#     res = requests.get(humors)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     humors = get_all_books_urls()
#     for humor in humors:
#         r = requests.get(humor)
#         soup = BeautifulSoup(r.content, "html.parser")
#         humor = [ humor, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(humor)

# def horror_category_url():
#     horror_link = get_all_links_categories()
#     return horror_link[30]
# horror_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("horror_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     horrors = horror_category_url()
#     res = requests.get(horrors)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     horrors = get_all_books_urls()
#     for horror in horrors:
#         r = requests.get(horror)
#         soup = BeautifulSoup(r.content, "html.parser")
#         horror = [ horror, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(horror)


# def history_category_url():
#     history_link = get_all_links_categories()
#     return history_link[31]
# history_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("history_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     historys = history_category_url()
#     res = requests.get(historys)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     historys = get_all_books_urls()
#     for history in historys:
#         r = requests.get(history)
#         soup = BeautifulSoup(r.content, "html.parser")
#         history = [ history, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(history)

# def food_and_drink_category_url():
#     food_and_drink_link = get_all_links_categories()
#     return food_and_drink_link[32]
# food_and_drink_category_url()    

# # # écrire les données pour la catégorie food_and_drink dans un fichier
# with open("food_and_drink_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     food_and_drinks = food_and_drink_category_url()
#     res = requests.get(food_and_drinks)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     cur_page = soup_category.find("li", class_="next")
#     cur_href = cur_page.find("a")["href"]
#     next_pag = cur_href
#     for i in range(1,3):
#         next_pag = requests.compat.urljoin(food_and_drinks, "page-" + str(i) +".html" )
#         urls_pages = []
#         urls_pages.append(next_pag)
#         for urls in urls_pages:
#             r = requests.get(urls)
#             soup_category = BeautifulSoup(r.content, "html.parser")
#             urls = get_all_books_urls()
#             for food_and_drink in urls:
#                 r = requests.get(food_and_drink)
#                 soup = BeautifulSoup(r.content, "html.parser")
#                 food_and_drink = [ food_and_drink, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#                 writer.writerow(food_and_drink)


# def christian_fiction_category_url():
#     christian_fiction_link = get_all_links_categories()
#     return christian_fiction_link[33]
# christian_fiction_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("christian_fiction_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     christian_fictions = christian_fiction_category_url()
#     res = requests.get(christian_fictions)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     christian_fictions = get_all_books_urls()
#     for christian_fiction in christian_fictions:
#         r = requests.get(christian_fiction)
#         soup = BeautifulSoup(r.content, "html.parser")
#         christian_fiction = [ christian_fiction, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(christian_fiction)

# def business_category_url():
#     business_link = get_all_links_categories()
#     return business_link[34]
# business_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("business_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     businesss = business_category_url()
#     res = requests.get(businesss)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     businesss = get_all_books_urls()
#     for business in businesss:
#         r = requests.get(business)
#         soup = BeautifulSoup(r.content, "html.parser")
#         business = [ business, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(business)

# def biography_category_url():
#     biography_link = get_all_links_categories()
#     return biography_link[35]
# biography_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("biography_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     biographys = biography_category_url()
#     res = requests.get(biographys)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     biographys = get_all_books_urls()
#     for biography in biographys:
#         r = requests.get(biography)
#         soup = BeautifulSoup(r.content, "html.parser")
#         biography = [ biography, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(biography)

# def thriller_category_url():
#     thriller_link = get_all_links_categories()
#     return thriller_link[36]
# thriller_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("thriller_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     thrillers = thriller_category_url()
#     res = requests.get(thrillers)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     thrillers = get_all_books_urls()
#     for thriller in thrillers:
#         r = requests.get(thriller)
#         soup = BeautifulSoup(r.content, "html.parser")
#         thriller = [ thriller, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(thriller)

# def contemporary_category_url():
#     contemporary_link = get_all_links_categories()
#     return contemporary_link[37]
# contemporary_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("contemporary_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     contemporarys = contemporary_category_url()
#     res = requests.get(contemporarys)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     contemporarys = get_all_books_urls()
#     for contemporary in contemporarys:
#         r = requests.get(contemporary)
#         soup = BeautifulSoup(r.content, "html.parser")
#         contemporary = [ contemporary, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(contemporary)

# def spirituality_category_url():
#     spirituality_link = get_all_links_categories()
#     return spirituality_link[38]
# spirituality_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("spirituality_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     spiritualitys = spirituality_category_url()
#     res = requests.get(spiritualitys)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     spiritualitys = get_all_books_urls()
#     for spirituality in spiritualitys:
#         r = requests.get(spirituality)
#         soup = BeautifulSoup(r.content, "html.parser")
#         spirituality = [ spirituality, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(spirituality)

# def academic_category_url():
#     academic_link = get_all_links_categories()
#     return academic_link[39]
# academic_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("academic_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     academics = academic_category_url()
#     res = requests.get(academics)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     academics = get_all_books_urls()
#     for academic in academics:
#         r = requests.get(academic)
#         soup = BeautifulSoup(r.content, "html.parser")
#         academic = [ academic, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(academic)

# def self_help_category_url():
#     self_help_link = get_all_links_categories()
#     return self_help_link[40]
# self_help_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("self_help_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     self_helps = self_help_category_url()
#     res = requests.get(self_helps)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     self_helps = get_all_books_urls()
#     for self_help in self_helps:
#         r = requests.get(self_help)
#         soup = BeautifulSoup(r.content, "html.parser")
#         self_help = [ self_help, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(self_help)

# def historical_category_url():
#     historical_link = get_all_links_categories()
#     return historical_link[41]
# historical_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("historical_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     historicals = historical_category_url()
#     res = requests.get(historicals)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     historicals = get_all_books_urls()
#     for historical in historicals:
#         r = requests.get(historical)
#         soup = BeautifulSoup(r.content, "html.parser")
#         historical = [ historical, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(historical)

# def christian_category_url():
#     christian_link = get_all_links_categories()
#     return christian_link[42]
# christian_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("christian_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     christians = christian_category_url()
#     res = requests.get(christians)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     christians = get_all_books_urls()
#     for christian in christians:
#         r = requests.get(christian)
#         soup = BeautifulSoup(r.content, "html.parser")
#         christian = [ christian, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(christian)

# def suspense_category_url():
#     suspense_link = get_all_links_categories()
#     return suspense_link[43]
# suspense_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("suspense_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     suspenses = suspense_category_url()
#     res = requests.get(suspenses)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     suspenses = get_all_books_urls()
#     for suspense in suspenses:
#         r = requests.get(suspense)
#         soup = BeautifulSoup(r.content, "html.parser")
#         suspense = [ suspense, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(suspense)

# def short_storie_category_url():
#     short_storie_link = get_all_links_categories()
#     return short_storie_link[44]
# short_storie_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("short_stories_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     short_stories = short_storie_category_url()
#     res = requests.get(short_stories)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     short_stories = get_all_books_urls()
#     for short_storie in short_stories:
#         r = requests.get(short_storie)
#         soup = BeautifulSoup(r.content, "html.parser")
#         short_storie = [ short_storie, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(short_storie)

# def novel_category_url():
#     novel_link = get_all_links_categories()
#     return novel_link[45]
# novel_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("novels_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     novels = novel_category_url()
#     res = requests.get(novels)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     novels = get_all_books_urls()
#     for novel in novels:
#         r = requests.get(novel)
#         soup = BeautifulSoup(r.content, "html.parser")
#         novel = [ novel, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(novel)

# def health_category_url():
#     health_link = get_all_links_categories()
#     return health_link[46]
# health_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("health_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     healths = health_category_url()
#     res = requests.get(healths)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     healths = get_all_books_urls()
#     for health in healths:
#         r = requests.get(health)
#         soup = BeautifulSoup(r.content, "html.parser")
#         health = [ health, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(health)

# def politic_category_url():
#     politic_link = get_all_links_categories()
#     return politic_link[47]
# politic_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("politics_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     politics = politic_category_url()
#     res = requests.get(politics)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     politics = get_all_books_urls()
#     for politic in politics:
#         r = requests.get(politic)
#         soup = BeautifulSoup(r.content, "html.parser")
#         politic = [ politic, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(politic)

# def cultural_category_url():
#     cultural_link = get_all_links_categories()
#     return cultural_link[48]
# cultural_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("cultural_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     culturals = cultural_category_url()
#     res = requests.get(culturals)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     culturals = get_all_books_urls()
#     for cultural in culturals:
#         r = requests.get(cultural)
#         soup = BeautifulSoup(r.content, "html.parser")
#         cultural = [ cultural, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(cultural)

# def erotica_category_url():
#     erotica_link = get_all_links_categories()
#     return erotica_link[49]
# erotica_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("erotica_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     eroticas = erotica_category_url()
#     res = requests.get(eroticas)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     eroticas = get_all_books_urls()
#     for erotica in eroticas:
#         r = requests.get(erotica)
#         soup = BeautifulSoup(r.content, "html.parser")
#         erotica = [ erotica, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(erotica)

# def crime_category_url():
#     crime_link = get_all_links_categories()
#     return crime_link[50]
# crime_category_url()    

# # écrire les données pour chaque catégorie dans un fichier
# with open("crime_category.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     crimes = crime_category_url()
#     res = requests.get(crimes)
#     soup_category = BeautifulSoup(res.content, "html.parser")
#     crimes = get_all_books_urls()
#     for crime in crimes:
#         r = requests.get(crime)
#         soup = BeautifulSoup(r.content, "html.parser")
#         crime = [ crime, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#         writer.writerow(crime)


# def get_all_data_urls():
#     all_categories = get_all_links_categories()
#     return all_categories

# with open("all_data_books.csv", "w", encoding="utf-8") as file_csv:
#     writer = csv.writer(file_csv, delimiter=",")
#     writer.writerow(headers_data)
#     categories = get_all_data_urls()
#     for categos in categories:
#         res = requests.get(categos)
#         soup_category = BeautifulSoup(res.content, "html.parser")
#         cur_page = soup_category.select_one("li.next>a")
#         if not cur_page:
#             break
#         else:
#             cur_href = cur_page["href"]
#             next_pag = cur_href
#             for i in range(1,51):
#                 next_pag = requests.compat.urljoin(categos, "page-" + str(i) +".html" )
#                 next_url = None
#                 if next_url:
#                     break
#                 else:
#                     urls_pages = []
#                     urls_pages.append(next_pag)
#                     for urls_pag in urls_pages:
#                         resp = requests.get(urls_pag)
#                         soup_category = BeautifulSoup(resp.content, "html.parser")
#                         urls = get_all_books_urls()
#                         for uls in urls_pag:
#                             r = requests.get(uls)
#                             sp = BeautifulSoup(r.content, "html.parser")
#                             uls = [uls, get_caterogy(), get_title(), get_description(), get_upc(), get_price_excl(), get_price_in(), get_num_available(), get_rev_rating(), get_image_url()]
#                             print(uls)

# essayer writerows