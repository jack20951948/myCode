import random
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
from sklearn.cluster import KMeans
from minisom import MiniSom
from pandas import DataFrame

def preprocess_data():
    data = pd.read_csv('nba_allPlayerData_1819.csv')
    # GP (Game played) set the minimum game played
    # MIN set the minimum play time per game
    # win, loss 先不看
    # FP (fantasy point) 先不看 [（得分）+（籃板）*1 +（助攻幫助隊友實得分數）+（抄截）*2 +（阻攻實際妨礙分數）-（失誤）*1 ]
    # Plus Minus先不看
    # DD2, TD3 先不看
    data = data.drop(columns=['W', 'L', 'FP', '+/-', 'DD2', 'TD3', 'OREB', 'DREB', 'TOV', 'PF'])
    ##set limit for GP and MIN
    data_list = data.values.tolist()

    return data_list

def main():
    data = preprocess_data()

    #SOM
    drop_name_data = []
    for item in data:
        drop_name_data.append(item[2:])
    
    som = MiniSom(6 ,6, 17, sigma=0.5, learning_rate=0.2)
    som.train_random(drop_name_data, 400)
    
    result1 = som.activation_response(drop_name_data)
    print('result1 are: \n', result1)
    qnt = som.quantization(drop_name_data)
    print(qnt)
    #K MEAN

main()