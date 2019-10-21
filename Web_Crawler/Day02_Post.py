import requests
from bs4 import BeautifulSoup 

url = "https://www.ptt.cc/bbs/Gossiping/index.html"

r = requests.Session()
payload ={
    "from":"/bbs/Gossiping/index.html",
    "yes":"yes"
}
r1 = r.post("https://www.ptt.cc/ask/over18?from=%2Fbbs%2FGossiping%2Findex.html",payload)
# r2 = r.get("https://www.ptt.cc/bbs/Gossiping/index.html")
# print(r2.text)
for i in range(9):
    page = r.get(url)
    soup = BeautifulSoup(page.text,"html.parser")
    sel = soup.select("div.title a") #取HTML標中的 <div class="title"></div> 中的<a>標籤存入sel
    print ("本頁的URL為"+url) # string+任意物件 => string
    for s in sel:
        print(s["href"], s.text) 
    back_button = soup.select("div.btn-group.btn-group-paging a")#上一頁按鈕的a標籤
    url = "https://www.ptt.cc"+ back_button[1]["href"] #組合出上一頁的網址
    # print(str(back_button[1]["href"])) 需先轉成string才能print