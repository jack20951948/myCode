from urllib.request import urlopen
from bs4 import BeautifulSoup 
import datetime
import random
import re

html = urlopen('http://en.wikipedia.org/wiki/Kevin_Bacon')
bs = BeautifulSoup(html, 'html.parser')
for link in bs.find_all('a'):  #找所有連結
    if 'href' in link.attrs:
        print(link.attrs['href'])


##內部URL特徵
##1.都在id為bodyContext的div中
##2.URL中沒有冒號
##3.URL以/wiki/開頭

###使用正規表示式篩選
html = urlopen('http://en.wikipedia.org/wiki/Kevin_Bacon')
bs = BeautifulSoup(html, 'html.parser')
for link in bs.find('div', {'id':'bodyContent'}).find_all(
    'a', href=re.compile('^(/wiki/)((?!:).)*$')):
    if 'href' in link.attrs:
        print(link.attrs['href'])

###重新整理以上程式

random.seed(datetime.datetime.now()) #亂數種子使用系統時間
def getLinks(articleUrl):
    html = urlopen('http://en.wikipedia.org{}'.format(articleUrl))
    bs = BeautifulSoup(html, 'html.parser')
    return bs.find('div', {'id':'bodyContent'}).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$'))

links = getLinks('/wiki/Kevin_Bacon')
i = 0
while len(links) > 0:
    newArticle = links[random.randint(0, len(links)-1)].attrs['href']
    print(i, " ", "http://en.wikipedia.org" + newArticle)
    i += 1
    links = getLinks(newArticle)