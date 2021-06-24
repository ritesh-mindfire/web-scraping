import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger('web_scrap')

def scrap_amazon_books_data():
    scrap_data = []
    url = "https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_1?ie=UTF8&pg=1"
    
    req = requests.get(url)
    
    # Simple check to check if page was blocked (Usually 503)
    if req.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in req.text:
            print("Page %s was blocked by Amazon. Please try again\n"%url)
            logger.error('Page was blocked by Amazon')

        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,req.status_code))
            logger.error('Page was blocked by Amazon')
        return None
    else:
        webdata = req.text
    
    soup = BeautifulSoup(webdata,'lxml')
    # print(soup.prettify())

    books_selector = soup.findAll("li", attrs={'class':'zg-item-immersion'})
    # print(books_selector[0].prettify())

    for book in books_selector:
        anchor_ele = book.find('a', attrs={'class':'a-link-normal'})

        title = anchor_ele.find('div', attrs={'class': 'p13n-sc-truncate'}).text.strip('\n ')
        img_src = anchor_ele.find('img').get('src', '')
        price_ele = book.find('span', attrs={'class': 'p13n-sc-price'})
        if not price_ele:
            price = None
        else:
            price = price_ele.text.strip('₹')

        kwargs = {'title': title, 'price': price, 'link': img_src, 'desc': 'N/A'}
        scrap_data.append(kwargs)
    
    return scrap_data


if __name__ == '__main__':
    scrap_data_lst = scrap_amazon_books_data()
    # print(scrap_data_lst)
