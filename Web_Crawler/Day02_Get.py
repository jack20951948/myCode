import requests
from bs4 import BeautifulSoup 

url = "https://www.ptt.cc/bbs/joke/index.html"
f = open('Web_Crawler/Texts/ptt_joke.txt', 'w', encoding='UTF-8')

for i in range(3):
    page = requests.get(url)
    soup = BeautifulSoup(page.text,"html.parser")
    sel = soup.select("div.title a") #取HTML標中的 <div class="title"></div> 中的<a>標籤存入sel
    # print ("本頁的URL為"+url) # string+任意物件 => string
    f.write("本頁的URL為"+url)
    for s in sel:
        # print(s["href"], s.text) 
        f.write(str(s["href"]) + s.text +"\n")
    back_button = soup.select("div.btn-group.btn-group-paging a")#上一頁按鈕的a標籤
    url = "https://www.ptt.cc"+ back_button[1]["href"] #組合出上一頁的網址
    # print(str(back_button[1]["href"])) 需先轉成string才能print
f.close()

f2 = open('Web_Crawler/Texts/ptt_joke.txt', 'r', encoding='UTF-8')
r = f2.read()
print(r)
f2.close()