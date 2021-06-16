import requests
from requests.api import get
from bs4 import BeautifulSoup


def scrap_amazon_books_data():
    scrap_data = []
    url = "https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_1?ie=UTF8&pg=1"
    
    webdata = requests.get(url).text
    soup = BeautifulSoup(webdata,'lxml')
    # print(soup.prettify())

    books_selector = soup.findAll("li", attrs={'class':'zg-item-immersion'})
    # print(books_selector[0].prettify())

    for book in books_selector:
        anchor_ele = book.find('a', attrs={'class':'a-link-normal'})

        title = anchor_ele.find('div', attrs={'class': 'p13n-sc-truncate'}).text.strip('\n ')
        img_src = anchor_ele.find('img').get('src', '')

        kwargs = {'title': title, 'price': 100, 'link': img_src, 'desc': 'N/A'}
        scrap_data.append(kwargs)
    
    return scrap_data


if __name__ == '__main__':
    scrap_data_lst = scrap_amazon_books_data()
    print(scrap_data_lst)
