from bs4 import BeautifulSoup
from http import  cookiejar
from urllib import request
from pyquery import PyQuery
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
def get_cookie(url):
    cookie = cookiejar.CookieJar()
    handler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(handler)
    opener.open(url)
    return cookie

def get_html(url):
    cookie = get_cookie(url)
    session = requests.Session()
    session.cookies.update(cookie)
    html = session.get(url, headers=headers)

    return html

url = 'https://stackoverflow.com/search?page=1&tab=Relevance&q=weka'
html = get_html(url)
soup = BeautifulSoup(html.text)
#print(soup.prettify())
qurl = soup.find_all('a',class_='question-hyperlink')
print(soup)
#print(qurl['data-searchsession'])