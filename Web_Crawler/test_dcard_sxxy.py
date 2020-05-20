#藉由首頁取得所有文章的URL
# -*- coding: utf8 -*- 
import requests
from bs4 import BeautifulSoup
import json

# test = open("Web_Crawler/Texts/AutoGetSxxy.txt", "w", encoding='UTF-8')

post_data_18={
    "id": 449235211937226,
    "ev": "SubscribedButtonClick",
    "dl": "https://www.dcard.tw/f/sex",
    "rl": "",
    "if": "false",
    "ts": "1569163592593",
    "cd[buttonFeatures]": {"classList":"Button_primary_3KkkPH Button_button_2uDT-a","destination":"","id":"","imageUrl":"","innerText":"是，我已滿十八歲。","numChildButtons":0,"tag":"button","name":"","value":""},
    "cd[buttonText]": "是，我已滿十八歲。",
    "cd[formFeatures]": "",
    "cd[pageFeatures]": {"title":"西斯板 | Dcard"},
    "cd[parameters]": "",
    "sw": "1280",
    "sh": "720",
    "v": "2.9.4",
    "r": "stable",
    "ec": "2",
    "o": "30",
    "fbc": "fb.1.1560162825068.IwAR0rvRNnRmjBNs5lXXRVof0Kib-IqsUBSOcqJ_g3QBcsmEi8MWOO-QfPuqM",
    "fbp": "fb.1.1556538313516.2105255715",
    "it": "1569163578839",
    "coo": "false",
    "es": "automatic",
    "rqm": "GET"
}

p = requests.Session()
url=requests.get("https://www.dcard.tw/_api/forums/sex",data = post_data_18 , headers = { "Referer": "https://www.dcard.tw/f/sex", "User-Agent": "Mozilla/5.0" })
soup = BeautifulSoup(url.text,"html.parser")
sel = soup.select("PostList_entry_1rq5Lf a.PostEntry_root_V6g0rd")
print(sel)
a=[]
for s in sel:
    a.append(s["href"])
print(a[2])
url = "https://www.dcard.tw"+ a[2]

# for k in range(0,10):
#         post_data={
#             "before":a[-1][9:18], #取a最後篇的id，id為每個元素的9-17位
#             "limit":"30",
#             "popular":"true"
#         }
#         r = p.get("https://www.dcard.tw/_api/forums/pet/posts",params=post_data, headers = { "Referer": "https://www.dcard.tw/", "User-Agent": "Mozilla/5.0" })
#         data2 = json.loads(r.text) #Get到的檔案為Json, 我們轉成python
#         for u in range(len(data2)):
#             Temporary_url = "/f/pet/p/"+ str(data2[u]["id"]) + "-" + str(data2[u]["title"].replace(" ","-")) #在標題上的space轉成網址會變成'-'
#             a.append(Temporary_url)
# print(a)
# j=0 #為了印頁數
# q=0 #為了印張數
# for i in a[2:]:
#     url = "https://www.dcard.tw"+i
#     j+=1
#     print ("第",j,"頁的URL為:"+url)
#     #file.write("temperature is {} wet is {}%\n".format(temperature, humidity))
#     test.write("第 {} 頁的URL為: {} \n".format(j,url))
#     url=requests.get(url)
#     soup = BeautifulSoup(url.text,"html.parser")
#     sel_jpg = soup.select("div.Post_content_NKEl9d div div div img.GalleryImage_image_3lGzO5")
#     for c in sel_jpg:
#         q+=1
#         print("第",q,"張:",c["src"])
#         test.write("%\n""第 {} 張: {} \n".format(q,c["src"])) 
#         try:
#             pic=requests.get(c["src"])
#             img2 = pic.content
#             pic_out = open('Web_Crawler/Images/'+str(q)+".png",'wb')
#             pic_out.write(img2)
#             pic_out.close()
#         except requests.exceptions.ConnectionError as e:
#             print('網路地址無法訪問，請檢查')
#             print(e)
#         except requests.exceptions.RequestException as e: #若圖片連結錯誤則會發生exception
#             print('訪問異常：')
#             print(e)

# test.close()
# print("爬蟲結束")