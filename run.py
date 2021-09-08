import sys
from typing import final 
from bs4 import BeautifulSoup
from numpy import lib
from numpy.lib.shape_base import tile
import requests
from selenium import webdriver
import time
import numpy as np

class Book:
    def __init__(self, title, link, author, price):
        self.title = title
        self.link = link
        self.price = price
        self.author = author

def create_search_url(title, author, webpage):

    if webpage == 'libraccio':
        title_libraccio = title.replace("'", '%27').replace(' ', '+')
        libraccio_template = f'https://www.libraccio.it/src/?FT={title_libraccio}+{author}&ch=libraccio'
        return(libraccio_template)    
    elif webpage == 'ebay':
        title_ebay = title.replace(' ', '+').replace("'", '%27')
        template_ebay = f'https://www.ebay.it/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={title_ebay}+{author}&_sacat=0'
        return(template_ebay)
def libraccio(title, author):

    webpage = create_search_url(title, author, 'libraccio')
    driver = webdriver.PhantomJS(executable_path='.\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    driver.get(webpage)

    html = driver.page_source
    html = BeautifulSoup(html, "html.parser")
    list_authors = list(map(lambda x: x.contents[0], html.select("div[class = 'attr author'] > span > a")))
    list_titles = list(map(lambda x: x.contents[0], html.select("div.title > a")))
    list_prices = list(map(lambda x: x.contents[0], html.select("span.sellpr:nth-child(1)")))
    list_prices = [float(x.replace('€', '').replace(',', '.')) for x in list_prices]
    list_links = list(map(lambda x: 'https://www.libraccio.it' + x['href'], html.select("div.title > a")))

    list_of_books = [Book(title, link, author, price) for title, link, author, price in zip(list_titles, list_links, list_authors, list_prices)]
    list_of_books = [book for book in list_of_books if book.author.lower().__contains__(author) and book.title.lower().__contains__(title)]


    # Check if there are more than one page 
    list_of_pages = [element['href'] for element in html.select('div.boxprodlist > div:nth-child(2) > a[class = "item number"]')]
    if list_of_pages:
        for page in list_of_pages:
            current_webpage = ('https://www.libraccio.it' + page)

            driver.get(current_webpage)

            html = driver.page_source
            html = BeautifulSoup(html, "html.parser")
            list_authors = list(map(lambda x: x.contents[0], html.select("div[class = 'attr author'] > span > a")))
            list_titles = list(map(lambda x: x.contents[0], html.select("div.title > a")))
            list_prices = list(map(lambda x: x.contents[0], html.select("span.sellpr:nth-child(1)")))
            list_prices = [float(x.replace('€', '').replace(',', '.')) for x in list_prices]
            list_links = list(map(lambda x: 'https://www.libraccio.it' + x['href'], html.select("div.title > a")))
            list_of_current_books = [Book(title, link, author, price) for title, link, author, price in zip(list_titles, list_links, list_authors, list_prices)]
            list_of_current_books = [book for book in list_of_books if book.author.lower().__contains__(author) and book.title.lower().__contains__(title)]
            list_of_books += list_of_current_books


    
    return(list_of_books)
    

def run():
    """ Script to perform book search in websites"""
    
    arg_len = len(sys.argv)

    if arg_len not in [2,3,4]:
        print(
            f"""
            Error: Insufficient number of arguments: {arg_len}.\n
            Use one of the following syntaxes:
            * To search for a book using its title and author:
                >> run.py book_title author website
            With parameters:
                * book_title: The title of the book.
                * author: The author of the book.
                * website: The website in which we want to perform our research.
            """)
        return
    
    title = sys.argv[1]
    author = sys.argv[2]
    website = sys.argv[3]

    webpage = create_search_url(title, author, 'ebay')
    print(webpage)
    driver = webdriver.PhantomJS(executable_path='.\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    driver.get(webpage)
    html = driver.page_source
    html = BeautifulSoup(html, "html.parser")
    print(html.select('h3'))
    # libraccio_elements = libraccio(title, author)
    # print(f'Ho estratto {len(libraccio_elements)} libri\n')
    # if libraccio_elements:
    #     prices = [book.price for book in libraccio_elements]
    #     mean_price = np.mean(prices)
    #     res = [i for i, j in enumerate(prices) if j == np.min(prices)][0]
    #     best_link = libraccio_elements[res].link
    #     best_price = libraccio_elements[res].price
    #     best_title = libraccio_elements[res].title
    #     print(f'Il libro si intitola {best_title} e costa {best_price} Euro. Lo puoi trovare al link {best_link}\n')
    #     print(f'Per tua informazione il prezzo medio è {mean_price} Euro\n')

    return 



if __name__ == '__main__':
    run()