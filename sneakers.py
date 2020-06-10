from bs4 import BeautifulSoup
import requests
import sys,getopt
import datetime

JUMIA_SNEAKERS_MEN_URL = 'https://www.jumia.dz/baskets-de-ville/?page={0}'

all_sneaker = []

def is_last_page(page):
    next_page_btn = page.select_one(
        '#jm > main > div.row.-pbm > div.-pvs.col12 > section > div.pg-w.-pvxl > a:nth-child(6)')
    return next_page_btn.get('href')


def scrap_page(page):
    print('scraping page ',page,' .....')
    url = JUMIA_SNEAKERS_MEN_URL.format(page)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    articles = soup.find_all('article', class_='prd')
    for article in articles:
        price = article.select_one('div.prc')
        discount = article.select_one('div._dsct')
        link = article.select_one('a.core')
        name = article.select_one('div.info > h3')
        #print( article,'::: ')
        if name.text and price.text and link.text:
            sneaker = {
                'name':name.text if name else 'nothing',
                'price':price.text if price else 0,
                'discount':int(discount.text.split('%')[0]) if discount else 0,
                'link':'https://www.jumia.dz'+link.get('href') if link else 'none'
            }
            all_sneaker.append(sneaker)

    return is_last_page(soup)




page = 1
while(True):
    is_next = scrap_page(page)
    page = page + 1
    if not is_next:
        break

all_sneaker.sort( key=lambda x : x['discount'],reverse=True)
print('found ',len(all_sneaker),' articles ')

file_name = 'sneakers_'+str(datetime.datetime.now())+'.text'



n=10

try:
    opts,args = getopt.getopt(sys.argv[1:],"n:")
except getopt.GetoptError:
    print('sneaker.py -n <int:number of sneaker>')
for opt,arg in opts:
    if opt == '-n':
        n = int(arg) 



for i in range (0,n):
    f = open(file_name,'a')
    f.write(all_sneaker[i]['name']+', '+all_sneaker[i]['price']+', '+str(all_sneaker[i]['discount'])+'%, '+all_sneaker[i]['link']+'\n')
