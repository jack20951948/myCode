import requests

pic = requests.get('https://imgur.dcard.tw/N2k5kV2m.jpg') #變數名稱為pic
# print(pic.content)
imContent = pic.content #圖片裡的內容

pic_out = open('Web_Crawler/Images/cat.png', 'wb') #cat.png為預存檔的圖片名稱
pic_out.write(imContent) #將get圖片存入cat.png
pic_out.close() #關閉檔案(很重要)