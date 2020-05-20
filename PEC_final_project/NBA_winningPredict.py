import random
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
from sklearn import preprocessing
from sklearn.cluster import KMeans
from minisom import MiniSom
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn import linear_model
from sklearn import svm
from sklearn import neighbors
from sklearn import ensemble
from sklearn.metrics import accuracy_score

k = 3
def preprocess_data():
    data = pd.read_csv('PEC_final_project/nba_Player_1819.csv')
    # GP (Game played) set the minimum game played
    # MIN set the minimum play time per game
    # win, loss 先不看
    # FP (fantasy point) 先不看 [（得分）+（籃板）*1 +（助攻幫助隊友實得分數）+（抄截）*2 +（阻攻實際妨礙分數）-（失誤）*1 ]
    # Plus Minus先不看
    # DD2, TD3 先不看
    data = data.drop(columns=['W', 'L', 'FP', '+/-', 'DD2', 'TD3']) #21 columns
    data_list = data.values.tolist()
    for index, item in enumerate(data_list):
        if item[3] <= 3 or item[6] <= 3:
            del data_list[index]
    
    # data.to_csv("nba.csv")

    ##set limit for GP and MIN

    return data_list

def plot_3d(data, color):
    # plt.scatter([x[11] for x in data], [x[17] for x in data], c=color)  #REB14,AST18
    # plt.show()
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter([x[1] for x in data],[x[3] for x in data],[x[5] for x in data],c=color)#GP,PTS,FGA
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter([x[6] for x in data],[x[9] for x in data],[x[12] for x in data],c=color)#FG%,3P%,FT%
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter([x[3] for x in data],[x[15] for x in data],[x[16] for x in data],c=color)#PTS,REB,AST
    plt.show()
    
def analysis_data(data, labels):
    for h in range(k):
        globals()['class_{}'.format(h)] = []
        for item in data:
            if item[21] == h:
                globals()['class_{}'.format(h)].append(item)
    avg = [] #avg data of each class
    for h in range(k):
        globals()['avg_{}'.format(h)] = []
        for i in range(21):
            average = sum(x[i] for x in globals()['class_{}'.format(h)])/len(globals()['class_{}'.format(h)])
            globals()['avg_{}'.format(h)].append(average)
        avg.append(globals()['avg_{}'.format(h)])
    
    df = pd.DataFrame(avg)
    # print(df)
    df.to_csv("PEC_final_project/nbaPlayerClass_1819.csv", index=True)

def count_type(data):
    winrate = pd.read_csv('PEC_final_project/nba_team_winrate.csv')
    winrate_list = winrate.values.tolist()
    print('winrate', winrate_list)
    le = preprocessing.LabelEncoder()
    for i in range(len(data)):
        team_list = le.fit_transform([x[1] for x in data])
    for i in range(30):
        globals()['team_{}'.format(i)] = [0]*(k+2)
    
    for index, item in enumerate(data):
        print(team_list[index])
        for h in range(k):
            if item[23] == h:
                globals()['team_{}'.format(team_list[index])][0] = data[index][1]
                globals()['team_{}'.format(team_list[index])][h+1] += 1
                globals()['team_{}'.format(team_list[index])][4] = winrate_list[team_list[index]][1]
                
            else:
                continue
    team = []
    for i in range(30):
        team.append(globals()['team_{}'.format(i)])
    print('team',team_0)
    print('team',team_1)
    df2 = pd.DataFrame(team, columns=['TEAM', 'TypeA', 'TypeB','TypeC', 'WinRate'])
    df2.to_csv('PEC_final_project/teamData_1819.csv',index=True)
    return team

def try_different_method(model,x_train,x_test,y_train,y_test):
    model.fit(x_train,y_train)
    score = model.score(x_test, y_test)
    result = model.predict(x_test)
    print('model:',model)
    print('score:',score)
    plt.figure()
    plt.plot(np.arange(len(result)), y_test,'go-',label='true value')
    plt.plot(np.arange(len(result)),result,'ro-',label='predict value')
    plt.title('score: %f'%score)
    plt.legend()
    plt.show()

def main():
    data_withTeam = preprocess_data()
    data = []
    for item in data_withTeam:
        data.append(item[2:])
    data_array = np.array(data)

    #SOM
    som = MiniSom(2 ,2, 21, sigma=0.3, learning_rate=0.2)
    som.random_weights_init(data_array)
    starting_weights = som.get_weights().copy()
    # print('weight:',starting_weights)
    som.train_random(data_array, 100000, verbose=True)
    qnt = som.quantization(data_array)
    # print('qnt:',qnt)
    # map = som.distance_map(data)
    result1 = som.activation_response(data_array)
    print('result1 are: \n', result1)
    #plot
    plt.figure(figsize=(10, 10))
    plt.pcolor(som.distance_map(), cmap='bone_r')
    plt.show()

    kmeans = KMeans(n_clusters=k, init = 'random', n_init = 1)
    kmeans = kmeans.fit(data)

    labels = kmeans.predict(data)
    for i in range(len(labels)):
        data[i].append(labels[i])
        data_withTeam[i].append(labels[i])
    analysis_data(data, labels)
    teamData_list = count_type(data_withTeam)
    # centroids = kmeans.cluster_centers_ 
    # print(centroids)
    plot_3d(data, labels)

    x_team = []
    y_team = []
    for i in range(len(teamData_list)):
        x_team.append(teamData_list[i][1:3])
        y_team.append(teamData_list[i][-1])

    x_train,x_test,y_train,y_test = train_test_split(x_team, y_team, test_size = 0.3)

    model_DecisionTreeRegressor = tree.DecisionTreeRegressor()
    model_LinearRegression = linear_model.LinearRegression()
    model_SVR = svm.SVR()
    model_KNeighborsRegressor = neighbors.KNeighborsRegressor()
    model_RandomForestRegressor = ensemble.RandomForestRegressor(n_estimators=20) #使用20個決策數

    try_different_method(model_DecisionTreeRegressor,x_train,x_test,y_train,y_test)
    try_different_method(model_LinearRegression,x_train,x_test,y_train,y_test)
    try_different_method(model_SVR,x_train,x_test,y_train,y_test)
    try_different_method(model_KNeighborsRegressor,x_train,x_test,y_train,y_test)
    try_different_method(model_RandomForestRegressor,x_train,x_test,y_train,y_test)

main()