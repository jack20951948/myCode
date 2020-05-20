from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html, 'html.parser')
images = bs.find_all('img', {'src':re.compile('\.\.\/img\/gifts/img.*\.jpg')})
for image in images: 
    print(image['src'])

x = bs.find_all(lambda tag: len(tag.attrs) == 2) #找出有兩個屬性的標籤
print("\nlen(tag.attrs) == 2:\n", x, "\n")

x = bs.find_all(lambda tag: tag.get_text() == 'Or maybe he\'s only resting?')
print("print'Or maybe he\'s only resting?':\n", x, "\n")

x = bs.find_all('', text='Or maybe he\'s only resting?')
print("print'Or maybe he\'s only resting?':\n", x, "\n")