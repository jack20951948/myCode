#藉由首頁取得所有文章的URL
import requests
from bs4 import BeautifulSoup
import json

test = open("Web_Crawler/Texts/AutoGetImg.txt", "w", encoding='UTF-8')

p = requests.Session()
url=requests.get("https://www.dcard.tw/f/pet")
soup = BeautifulSoup(url.text,"html.parser")
sel = soup.select("div.PostList_entry_1rq5Lf a.PostEntry_root_V6g0rd")
a=[]
for s in sel:
    a.append(s["href"])
print(a[0])
url = "https://www.dcard.tw"+ a[0]

for k in range(0,10):
        post_data={
            "before":a[-1][9:18], #取a最後篇的id，id為每個元素的9-17位
            "limit":"30",
            "popular":"true"
        }
        r = p.get("https://www.dcard.tw/_api/forums/pet/posts",params=post_data, headers = { "Referer": "https://www.dcard.tw/", "User-Agent": "Mozilla/5.0" })
        data2 = json.loads(r.text) #Get到的檔案為Json, 我們轉成python
        for u in range(len(data2)):
            Temporary_url = "/f/pet/p/"+ str(data2[u]["id"]) + "-" + str(data2[u]["title"].replace(" ","-")) #在標題上的space轉成網址會變成'-'
            a.append(Temporary_url)
print(a)
j=0 #為了印頁數
q=0 #為了印張數
for i in a:
    url = "https://www.dcard.tw"+i
    j+=1
    print ("第",j,"頁的URL為:"+url)
    #file.write("temperature is {} wet is {}%\n".format(temperature, humidity))
    test.write("第 {} 頁的URL為: {} \n".format(j,url))
    url=requests.get(url)
    soup = BeautifulSoup(url.text,"html.parser")
    sel_jpg = soup.select("div.Post_content_NKEl9d div div div img.GalleryImage_image_3lGzO5")
    for c in sel_jpg:
        q+=1
        print("第",q,"張:",c["src"])
        test.write("%\n""第 {} 張: {} \n".format(q,c["src"])) 
        try:
            pic=requests.get(c["src"])
            img2 = pic.content
            pic_out = open('Web_Crawler/Images/'+str(q)+".png",'wb')
            pic_out.write(img2)
            pic_out.close()
        except requests.exceptions.ConnectionError as e:
            print('網路地址無法訪問，請檢查')
            print(e)
        except requests.exceptions.RequestException as e: #若圖片連結錯誤則會發生exception
            print('訪問異常：')
            print(e)

test.close()
print("爬蟲結束")