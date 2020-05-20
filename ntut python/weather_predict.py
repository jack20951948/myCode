import numpy as np
from sklearn import tree
from sklearn.model_selection import train_test_split
import pydotplus
def outlook_type(s):
    it = {'sunny':1, 'overcast':2, 'rainy':3}
    return it[s]
def temperature(s):
    it = {'hot':1, 'mild':2, 'cool':3}
    return it[s]
def humidity(s):
    it = {'high':1, 'normal':0}
    return it[s]
def windy(s):
    it = {'TRUE':1, 'FALSE':0}
    return it[s]
def play_type(s):
    it = {'yes': 1, 'no': 0}
    return it[s]
play_feature_E = 'outlook', 'temperature', 'humidity', 'windy'
play_class = 'yes', 'no'
# 1、讀入資料，並將原始資料中的資料轉換為數字形式
data = np.loadtxt("play.tennies.txt", delimiter=" ", dtype=str,  converters={0:outlook_type, 1:temperature, 2:humidity, 3:windy,4:play_type})
x, y = np.split(data,(4,),axis=1)
# 2、拆分訓練資料與測試資料，為了進行交叉驗證
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3,random_state=2)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
# 3、使用資訊熵作為劃分標準，對決策樹進行訓練
clf = tree.DecisionTreeClassifier(criterion='entropy')
print(clf)
clf.fit(x_train, y_train)
# 4、把決策樹結構寫入檔案
dot_data = tree.export_graphviz(clf, out_file=None, feature_names=play_feature_E, class_names=play_class,
filled=True, rounded=True, special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf('play1.pdf')
# 係數反映每個特徵的影響力。越大表示該特徵在分類中起到的作用越大
print(clf.feature_importances_)
# 5、使用訓練資料預測，預測結果完全正確
answer = clf.predict(x_train)
y_train = y_train.reshape(-1)
print(answer)
print(y_train)
print(np.mean(answer == y_train))
# 6、對測試資料進行預測，準確度較低，說明過擬合
answer = clf.predict(x_test)
y_test = y_test.reshape(-1)
print(answer)
print(y_test)
print(np.mean(answer == y_test))