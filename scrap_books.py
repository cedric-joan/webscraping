import requests
from bs4 import BeautifulSoup

# url de la page
book_page_url = "http://books.toscrape.com/catalogue/the-dirty-little-secrets-of-getting-your-dream-job_994/index.html"

# requête pour accéder à la page
def get_url(book_page_url):
    reponse = requests.get(book_page_url)
    page = reponse.content
    return page
get_url(book_page_url)

# parser la page
soup = BeautifulSoup(get_url(book_page_url), "html.parser")

