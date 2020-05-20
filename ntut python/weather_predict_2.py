import numpy as np
import csv
#from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn import metrics
import pydotplus
import pandas as pd

# def drawTree(tennis, clf):
#     # sklearn.tree.export_graphviz(decision_tree, out_file=None, 
#     # max_depth=None, feature_names=None, class_names=None, 
#     # label=’all’, filled=False, leaves_parallel=False, 
#     # impurity=True, node_ids=False, proportion=False, 
#     # rotate=False, rounded=False, special_characters=False, precision=3)
#     #https://scikit-learn.org/…/sklearn.tree.export_graphviz.html
#     #將 Tree導出為 graphviz
#     dot_data = tree.export_graphviz(clf, out_file=None,
#     feature_names= data_te[0,:-1],
#     class_names= ['No','Yes'],
#     filled=True, rounded=True,
#     special_characters=True)
#     #使用 pydotplus 產生 pdf 檔案
#     graph = pydotplus.graph_from_dot_data(dot_data)
#     graph.write_pdf('d:\\Play_tennis.pdf')

def decisionTree():
    with open('Tennis_data_num.csv',newline = '') as data_t:
        list_t = list(csv.reader(data_t))
        data_te = np.array(list_t).reshape(len(list_t),len(list_t[0]))
        print(list_t)
        print((data_te))

        dataframe_te = pd.DataFrame(data_te[1:,:], columns = data_te[0])
        print(dataframe_te.head())

        x_tennis = data_te[1:,0:3]
        y_tennis = data_te[1:,-1]

        x_train,x_test,y_train,y_test = train_test_split(x_tennis, y_tennis, test_size = 0.3)

        clf = tree.DecisionTreeClassifier(criterion='entropy')
        tennis_clf = clf.fit(x_tennis, y_tennis)

        y_test_predicted = tennis_clf.predict(x_test)
        print(y_test_predicted)
        # 標準答案
        print(y_test)
        # 績效 - 精確度
        accuracy = metrics.accuracy_score(y_test, y_test_predicted)
        print(accuracy)
        #drawTree(tennis, tennis_clf)
        dot_data = tree.export_graphviz(clf, out_file=None,
        feature_names= data_te[0,0:3],
        class_names= ['No','Yes'],
        filled=True, rounded=True,
        special_characters=True)
        #使用 pydotplus 產生 pdf 檔案
        graph = pydotplus.graph_from_dot_data(dot_data)
        graph.write_pdf('d:\\Play_tennis.pdf')

decisionTree()