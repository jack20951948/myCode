import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sympy
import math
from scipy import signal
import sys
import time
import statistics

Nowfile = 2 ###從幾號檔案開始import
fileTotal = 5 ###import幾組資料

def dataConbining():
    u_data = None
    s_data = None
    for i in range(fileTotal):
        tmpdata = np.loadtxt("Lab_random_motion/randomData/head_u_{}.txt".format(i+Nowfile), delimiter="\t", dtype=float, skiprows=2)
        if u_data is None:
            u_data = tmpdata
        else:
            u_data = np.vstack((u_data, tmpdata))
    for i in range(fileTotal):
        tmpdata = np.loadtxt("Lab_random_motion/randomData/head_s_{}.txt".format(i+Nowfile), delimiter="\t", dtype=float, skiprows=2)
        if s_data is None:
            s_data = tmpdata
        else:
            s_data = np.vstack((s_data, tmpdata))
    data = dataProcessing(u_data, s_data)
    print("data:\n", data)
    return data

def dataProcessing(uData, sData):
    ul = uData.tolist()
    sl = sData.tolist()
    for i in range(len(ul)):
        ul[i][0] = i
        ul[i].append(sl[i][2])
    Data = np.asarray(ul)
    return Data

def plotData(data):
    plt.figure()
    plt.subplot(311)
    plt.plot([x[0] for x in data], [x[1] for x in data], color='b', label="Time - x")
    plt.ylabel('x(m)')
    plt.title("data Step - xy plot")
    plt.subplot(312)
    plt.plot([x[0] for x in data], [x[2] for x in data], color='g', label="Time - y")
    plt.ylabel('y(m)')
    plt.subplot(313)
    plt.plot([x[0] for x in data], [x[3] for x in data], color='r', label="Time - z")
    plt.xlabel('Time(sec.)')
    plt.ylabel('z(m)')
    plt.legend()
    # plt.show()

def plotRoute(data):
    plt.figure()
    plt.plot([x[1] for x in data], [x[2] for x in data], label="Motion Route",color='b')
    plt.xlabel('x(m)')
    plt.ylabel('y(m)')
    plt.title("Motion Route")
    plt.legend()
    # plt.show()

def plot3dRoute(Data):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot([x[1] for x in Data],[x[2] for x in Data], [x[3] for x in Data], color='r')
    ax.set_xlabel('x(m)')
    ax.set_xlim(-0.64, 0.58)
    ax.set_ylabel('y(m)')
    ax.set_ylim(-0.31, 0.27)
    ax.set_zlabel('z(m)')
    ax.set_zlim(-0.016, 0.82)
    plt.title("3D Route")
    # plt.show()

def filter(data, axix, fs=1000, fc=30, order=5 ,plotData=False ,returnValue=True): #fs=>Sampling frequency, fc=>Cut-off frequency of the filter
    w = fc / (fs / 2) # Normalize the frequency
    b, a = signal.butter(order, w, 'low')
    output = signal.filtfilt(b, a, [x[axix] for x in data])
    if plotData == True:
        plt.plot([x[0] for x in data], output, label='filtered')
        plt.legend()
    if returnValue == True:
        return output
    else:
        pass

def gradient1by1(data):
    data_li = []
    for i in range(len(data)):
        data_li.append(data[i])
    data_n = np.asarray(data_li)
    dataDiff = np.gradient(data_n)
    return dataDiff

def Gradient(data):
    dataDiff = gradient1by1(data[:,1])
    dataDiff2 = gradient1by1(data[:,2])
    dataDiff3 = gradient1by1(data[:,3])
    difData = conbine3toOne(dataDiff, dataDiff2, dataDiff3)
    return difData

def filteTheData(data):
    filtedDataX = filter(data, 1, fc=70)
    filtedDataY = filter(data, 2, fc=70)
    filtedDataZ = filter(data, 3, fc=70)
    filtedData = conbine3toOne(filtedDataX, filtedDataY, filtedDataZ)
    return filtedData

def conbine3toOne(data1, data2, data3):
    Data = [[] * 4] * len(data1)
    for i in range(len(data1)):
        Data[i] = [i]
        Data[i].append(data1[i])
        Data[i].append(data2[i])
        Data[i].append(data3[i])
        Data_np = np.asarray(Data)
    return Data_np

def findCritical(data, bios=0.0005):
    peaks = []
    troughs = []
    for idx in range(1, len(data)-1):
        if data[idx-1] < data[idx] > data[idx+1]:
            if abs(data[idx]) >= bios:
                peaks.append(idx)
        if data[idx-1] > data[idx] < data[idx+1]:
            if abs(data[idx]) >= bios:
                troughs.append(idx)
    return peaks, troughs

def getCritical(data):
    peak1, troughs1 = findCritical(data[:,1])
    peak2, troughs2 = findCritical(data[:,2])
    peak3, troughs3 = findCritical(data[:,3])
    critical = peak1 + peak2 + peak3 + troughs1 + troughs2 + troughs3
    critical = np.unique(critical).tolist()
    critical.sort()
    print("criticalByOrder(step):\n", critical)

    peakvalue1 = []
    for i in peak1:
        peakvalue1.append(data[i,1])
    print("meanofP1:\n",statistics.mean(peakvalue1))



    return critical

def data2Direction(step, data, bias=0.001):
    action = []
    for i in range(len(data)):
        checkstep = 0
        for j in range(len(step)):
            if data[i,0] == step[j]:
                checkstep = 1
                if data[i,3] > bias:
                    if -bias < abs(data[i,1]) < bias and data[i,2] > bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 1, speed])
                        continue
                    if data[i,1] > bias and data[i,2] > bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 2, speed])
                        continue
                    if data[i,1] > bias and -bias < abs(data[i,2]) <(bias):
                        speed = data2Speed(data[i])
                        action.append([step[j], 3, speed])
                        continue
                    if data[i,1] > bias and data[i,2] < -bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 4, speed])
                        continue
                    if -bias < abs(data[i,1]) < bias and data[i,2] < bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 5, speed])
                        continue
                    if data[i,1] < -bias and data[i,2] < bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 6, speed])
                        continue
                    if data[i,1] < -bias and -bias < abs(data[i,2]) < bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 7, speed])
                        continue
                    if data[i,1] < -bias and data[i,2] > bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 8, speed])
                        continue
                    if -bias < abs(data[i,1]) < bias and -bias < abs(data[i,2]) < bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 25, speed])
                        continue
                if -bias < abs(data[i,3]) < bias:
                    if -bias < abs(data[i,1]) < bias and data[i,2] > bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 9, speed])
                        continue
                    if data[i,1] > bias and data[i,2] > bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 10, speed])
                        continue
                    if data[i,1] > bias and -bias < abs(data[i,2]) <(bias):
                        speed = data2Speed(data[i])
                        action.append([step[j], 11, speed])
                        continue
                    if data[i,1] > bias and data[i,2] < -bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 12, speed])
                        continue
                    if -bias < abs(data[i,1]) < bias and data[i,2] < bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 13, speed])
                        continue
                    if data[i,1] < -bias and data[i,2] < bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 14, speed])
                        continue
                    if data[i,1] < -bias and -bias < abs(data[i,2]) < bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 15, speed])
                        continue
                    if data[i,1] < -bias and data[i,2] > bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 16, speed])
                        continue
                if data[i,3] < bias:
                    if -bias < abs(data[i,1]) < bias and data[i,2] > bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 17, speed])
                        continue
                    if data[i,1] > bias and data[i,2] > bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 18, speed])
                        continue
                    if data[i,1] > bias and -bias < abs(data[i,2]) <(bias):
                        speed = data2Speed(data[i])
                        action.append([step[j], 19, speed])
                        continue
                    if data[i,1] > bias and data[i,2] < -bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 20, speed])
                        continue
                    if -bias < abs(data[i,1]) < bias and data[i,2] < bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 21, speed])
                        continue
                    if data[i,1] < -bias and data[i,2] < bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 22, speed])
                        continue
                    if data[i,1] < -bias and -bias < abs(data[i,2]) < bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 23, speed])
                        continue
                    if data[i,1] < -bias and data[i,2] > bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 24, speed])
                        continue
                    if -bias < abs(data[i,1]) < bias and -bias < abs(data[i,2]) < bias:
                        speed = data2Speed(data[i])
                        action.append([step[j], 26, speed])
                        continue
            else:
                pass
        if checkstep == 0:
            action.append([i, 0, 0])
    actionWithoutStep = []
    for x in action:
        actionWithoutStep.append(x[1])
    return action, actionWithoutStep

def data2Speed(data, bias1=0.0015,bias2=0.003 ,bias3=0.0045):
    if (pow(data[1], 2) + pow(data[2], 2) + pow(data[3], 2)) > pow(bias3, 2):
        return 2
    elif (pow(data[1], 2) + pow(data[2], 2) + pow(data[3], 2)) >= pow(bias2, 2) and (pow(data[1], 2) + pow(data[2], 2) + pow(data[3], 2)) <= pow(bias3, 2):
        return 1
    else:
        return 0

def num_to_string(num):
    numbers = {
        0 : "pass",
        1 : "NU",
        2 : "ENU",
        3 : "EU",
        4 : "ESU",
        5 : "SU",
        6 : "WSU",
        7 : "WU",
        8 : "WNU",
        9 : "N",
        10 : "EN",
        11 : "E",
        12 : "ES",
        13 : "S",
        14 : "WS",
        15 : "W",
        16 : "WN",
        17 : "ND",
        18 : "END",
        19 : "ED",
        20 : "ESD",
        21 : "SD",
        22: "WSD",
        23 : "WD",
        24 : "WND",
        25 : "U",
        26 : "D"
    }
    return numbers.get(num, None)

def transition_matrix(transitions):
    n = 1+ max(transitions) #number of states

    M = [[0]*n for _ in range(n)]

    for (i,j) in zip(transitions,transitions[1:]):
        M[i][j] += 1

    #now convert to probabilities:
    for row in M:
        s = sum(row)
        if s > 0:
            row[:] = [f/s for f in row]
    return M

def speed_probabilities(data):
    M = [[0]*3 for _ in range(27)]
    N = [[0]*3 for _ in range(27)]
    for i in data:
        if i[2] == 0:
            M[i[1]][0] += 1
        if i[2] == 1:
            M[i[1]][1] += 1
        if i[2] == 2:
            M[i[1]][2] += 1
    for i in range(len(M)):
        if sum(M[i][:]) != 0:
            N[i][0] = M[i][0]/sum(M[i][:])
            N[i][1] = M[i][1]/sum(M[i][:])
            N[i][2] = M[i][2]/sum(M[i][:])
    return N


def motionForecast(steps, transitionName, transitionMatrix):   ####馬爾可夫鏈預測模型
    # 選擇初始狀態 
    activityToday = "Sleep" 
    print("Start state: " + activityToday) 

    # 應該記錄選擇的狀態序列。這裡現在只有初始狀態。 
    activityList = [activityToday] 
    i = 0 

    # 計算 activityList 的機率 
    prob = 1 
    while i != steps: 
        if activityToday == "Sleep": 
            change = np.random.choice(transitionName[0],replace=True,p=transitionMatrix[0]) 
            if change == "SS": 
                prob = prob * 0.2 
                activityList.append("Sleep") 
                pass 
            elif change == "SR": 
                prob = prob * 0.6 
                activityToday = "Run" 
                activityList.append("Run") 
            else: 
                prob = prob * 0.2 
                activityToday = "Icecream" 
                activityList.append("Icecream") 
        elif activityToday == "Run": 
            change = np.random.choice(transitionName[1],replace=True,p=transitionMatrix[1]) 
            if change == "RR": 
                prob = prob * 0.5 
                activityList.append("Run") 
                pass 
            elif change == "RS": 
                prob = prob * 0.2 
                activityToday = "Sleep" 
                activityList.append("Sleep") 
            else: 
                prob = prob * 0.3 
                activityToday = "Icecream" 
                activityList.append("Icecream") 
        elif activityToday == "Icecream": 
            change = np.random.choice(transitionName[2],replace=True,p=transitionMatrix[2]) 
            if change == "II": 
                prob = prob * 0.1 
                activityList.append("Icecream") 
                pass 
            elif change == "IS": 
                prob = prob * 0.2 
                activityToday = "Sleep" 
                activityList.append("Sleep") 
            else: 
                prob = prob * 0.7 
                activityToday = "Run" 
                activityList.append("Run") 
        i += 1 
    print("Possible states: " + str(activityList)) 
    print("End state after "+ str(steps) + " steps: " + activityToday) 
    print("Probability of the possible sequence of states: " + str(prob)) 
    # 預測 2 天后的可能狀態 

    return activityList

if __name__ == "__main__":
    data = dataConbining()
    graData = Gradient(data)
    gradata2 = Gradient(graData)

    filtedData = filteTheData(data)
    graFilData = Gradient(filtedData)
    graFilData2 = Gradient(graFilData)

    plotRoute(data)
    plotData(data)
    plotData(filtedData)
    # plotData(graData)
    plotData(graFilData)
    # plotData(gradata2)
    plotData(graFilData2)

    critical = getCritical(graFilData2)
    action, actionWithoutStep = data2Direction(critical, graFilData2)

    print("action(step, action, speed):\n", action)
    print("actionWithoutStep:\n", actionWithoutStep)

    listAction = []
    [listAction.append(i) for i in actionWithoutStep if not i in listAction]
    listAction.sort()
    print("listAction:\n", listAction)

    # plot3dRoute(data)
    # plotRoute(filtedData)
    plot3dRoute(filtedData)
    plt.show()

    m = transition_matrix(actionWithoutStep)
    print("Posibitity:")
    for row in m: print(' '.join('{0:.2f}'.format(x) for x in row))
    # print(m)

    n = speed_probabilities(action)
    print("speed_Posibitity:")
    for row in n: print(' '.join('{0:.2f}'.format(x) for x in row))



#############################################馬爾可夫鏈範例#####################################
    # states = ["Sleep","Icecream","Run"]
    # # 可能的事件序列 
    # transitionName = [["SS","SR","SI"],["RS","RR","RI"],["IS","IR","II"]] 
    # # 機率矩陣（轉移矩陣） 
    # transitionMatrix = [[0.2,0.6,0.2],[0.1,0.6,0.3],[0.2,0.7,0.1]] #    transitionMatrix = m
    # activityList = motionForecast(2, transitionName, transitionMatrix)


#############################################驗證馬爾可夫鏈#####################################

    # # 記錄每次的 activityList 
    # list_activity = [] 
    # count = 0 
    # # `range` 從第一個參數開始數起，一直到第二個參數（不包含） 
    # for iterations in range(1,10000): 
    #     list_activity.append(motionForecast(2, transitionName, transitionMatrix)) 
    # # 查看記錄到的所有 `activityList` 
    # #print(list_activity) 
    # # 遍歷列表，得到所有最終狀態是跑步的 activityList 
    # for smaller_list in list_activity: 
    #     if(smaller_list[2] == "Run"): 
    #         count += 1 
    # # 計算從睡覺狀態開始到跑步狀態結束的機率 
    # percentage = (count/10000) * 100 
    # print("The probability of starting at state:'Sleep' and ending at state:'Run'= " + str(percentage) + "%")


