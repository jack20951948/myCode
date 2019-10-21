import tensorflow as tf 
import numpy as np  
import matplotlib.pyplot as plt  
import pandas as pd  
import networkx as nx
from apyori import apriori 
#pip install apriori
from wordcloud import WordCloud 
#pip install wordcloud

def testTensorflow():
    hello = tf.constant('hello tensorflow!') 
    sess = tf.Session()
    print("hello") 
    print(sess.run(hello))

#conda install -c conda-forge wordcloud
#pip install wordcloud
def wordCloud():
#畫圖套件，圖案大小
    plt.figure(figsize=(9,6))
    #numpy套件矩陣/陣列資料型態 
    data=np.array([
        ['Milk','Bread','Apple'],
        ['Milk','Bread'],
        ['Milk','Bread','Apple', 'Banana'],
        ['Milk', 'Banana','Rice','Chicken'],
        ['Apple','Rice','Chicken'],
        ['Milk','Bread', 'Banana'],
        ['Rice','Chicken'],
        ['Bread','Apple', 'Chicken'],
        ['Bread','Chicken'],
        ['Apple', 'Banana']])
    #convert the array to list's text
    #設定空的 list 
    text_data=[]
    for i in data:
        for j in i:
        #將np陣列得字串一個個加入 list
            text_data.append(j) 
    #map: 將 text_data當成 function str 的參數運算
    #回傳後串起來，以 " "隔開 
    products=' '.join(map(str, text_data))
    print(products)
    print(type(products))
    # generate 可對全部文字自動分詞
    # 可透過font_path參數設定字體集
    #background_color參數為設定背景顏色，預設顏色為黑色
    # 設定停用詞stopwords
    wordcloud = WordCloud(relative_scaling = 1.0,stopwords = {}).generate(products)
    #產生圖片
    plt.imshow(wordcloud)
    #關閉座標軸
    plt.axis("off")
    #顯示圖
    plt.show()

testTensorflow()
wordCloud()