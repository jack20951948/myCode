from bs4 import BeautifulSoup
from urllib.request import urlopen

# if has Chinese, apply decode()
html = urlopen("https://morvanzhou.github.io/static/scraping/list.html").read().decode('utf-8')
print(html)

soup = BeautifulSoup(html, features='lxml')

# use class to narrow search
month = soup.find_all('li', {"class": "month"}) #把class考慮進去
for m in month:
    print(m.get_text())  #get_text只顯示文字
    
jan = soup.find('ul', {"class": 'jan'})
d_jan = jan.find_all('li')              # use jan as a parent
for d in d_jan:
    print(d.get_text())