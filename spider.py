import requests
from pyquery import PyQuery as pq
from urllib import request
from urllib import parse
from http import cookiejar
from selenium import webdriver
import re

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

def get_cookie(url):
    cookie = cookiejar.CookieJar()
    handler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(handler)
    opener.open(url)
    return cookie

def get_html(url):
    # login_page = "https://stackoverflow.com/users/login?ssrc=head&returnurl=https%3a%2f%2fstackoverflow.com%2fsearch%3fq%3dweka"
    # data = parse.urlencode({"email":'13012478865@163.com',"password":'zhangchen1997+'}).encode("utf-8")
    # cookie = cookiejar.CookieJar()
    # handler = request.HTTPCookieProcessor(cookie)
    # opener = request.build_opener(handler)
    # opener.open(login_page,data)
    # op = opener.open(url)
    # html = op.read()
    wd = webdriver.Chrome()
    login_url = 'https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent'
    wd.get(login_url)
    wd.find_element_by_name('display-name').send_keys('test')
    wd.find_element_by_name('email').send_keys('13012478865@163.com')
    wd.find_element_by_name('password').send_keys('zhangchen1997+')
    wd.find_element_by_xpath('.mt16.s-btn.s-btn__primary.s-btn__md').click()
    req = requests.Session()
    cookie = wd.get_cookies()
    req.cookies.update(cookie)
    html = req.get(url,headers = headers)
    return html



def spider_comment(url):
    html = get_html(url)
    doc = pq(html)
    author_name = doc('.question')('.user-details')('a')
    author_name = re.findall(r'<a\shref=.*>([^<]+)</a>', str(author_name))
    print('---------------------------question-----------------------------')
    print('author:'+" ".join(author_name))
    print(doc('.question')('.post-text').text())
    print('----------------------------------------------------------------')
    comment = doc('#answers')('.post-text')#('p')
    #comment = re.findall(r'')
    #print(re.findall(r'\s*<div\sclass="post-text"\sitemprop="text">&#13;\n?([\s\S]*)\s*</div>&#13;',str(comment)))
    name = doc('#answers')('.user-details')('a')#.text()
    name = re.findall(r'<a\shref=.*>([^<]+)</a>',str(name))
    a = (str(comment).split('</div>&#13;\n'))
    a.pop()
    count = 0
    for i in a:
        print('--------------------------answers%d------------------------------' % (count+1))
        print('author:'+name[count])
        print(pq(i)('p').text())
        pic = pq(i)('img')
        if pic:
           for i in re.findall(r'<img\ssrc="(https://.*.png)"', str(pic)):
                print(i)
        else:
           pass
        count = count + 1
    print('----------------------------------------------------------------')


def spider_url(url):
    html = get_html(url)
    doc = pq(html.text)
    print(doc)
    a = doc('.flush-left.js-search-results')('.result-link')
    question_url = re.findall(r'/questions/\d*',str(a.xhtml_to_html()))
    question_url = ['https://stackoverflow.com'+i for i in question_url]
    question_url = sorted(set(question_url), key=question_url.index)
    for i in question_url:
        print(i)
    print('now we have all the Urls ..hah..')
    # for i in question_url:
    #     print('loading \'%s\' ' % i)
    #     spider_comment(i)


PAGE = 453
search = 'weka'

for npage in range(1,PAGE):
    # try:
    #     url = 'https://stackoverflow.com/search?page=%d&tab=Relevance&q=%s' % (npage,search)
    #     print('crawling %s ' % url)
    #     spider_url(url)
    # except:
    #     print('page %d crawl failure...' % npage)
    #     pass
    # break
    url = 'https://stackoverflow.com/search?page=%d&tab=Relevance&q=%s' % (npage, search)
    print('crawling page %d... ' % npage)
    spider_url(url)
    break

