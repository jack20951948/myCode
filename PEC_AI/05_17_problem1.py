import random
import math
import matplotlib.pyplot as plt
import time

def stepFunction(y):
    return 0 if y <= 0 else 1

def isStopCriterionMet(testingList):
    misClassifiedCount = 0
    for testingData in testingList:
        yHat = stepFunction(wi * testingData[0] + wj * testingData[1] + w0)
        if yHat != testingData[2]:
            misClassifiedCount += 1
    # print (misClassifiedCount)
    # return True if misClassifiedCount <= 10 else False
    return misClassifiedCount

def PredictClass(testingList):
    PredictionResult=[]
    for testingData in testingList:
        yHat = stepFunction(wi * testingData[0] + wj * testingData[1] + w0)
        PredictionResult.append(yHat)
    return PredictionResult

startTime = time.time()

# read file
file = open("raw.txt", "r", encoding = "utf-8")

# 0 = not stressed, 1 = stressed
data = [(each.replace("\n", "").split("\t")) for each in file]
data = [(float(each[0]), float(each[1]), 0) if data.index(each) < 200 else (float(each[0]), float(each[1]), 1) for each in data]

plt.scatter([x[0] for x in data[0:199]], [x[1] for x in data[0:199]])
plt.scatter([x[0] for x in data[199:]], [x[1] for x in data[199:]])
plt.show()


# the first 199 are not stressed, remaining 200 are stressed
notStressed = data[:199]
stressed = data[199:]

random.shuffle(notStressed)
random.shuffle(stressed)
trainingList = notStressed[:99] + stressed[:100]
random.shuffle(trainingList)
testingList = notStressed[99:] + stressed[100:]



learningRate = 0.0004
wi = random.random()
wj = random.random()
w0 = random.randint(-1, 1)

misClassifiedList = []
iteration = 0
# while not isStopCriterionMet(testingList):
while True:
    misClassifiedCount = isStopCriterionMet(testingList)
    misClassifiedList.append(misClassifiedCount)
    if misClassifiedCount < 30:
        print ("converged")
        break
    if iteration > 1000:
        break
    for trainingData in trainingList:
        yHat = stepFunction(wi * trainingData[0] + wj * trainingData[1] + w0)
        wi += learningRate * (trainingData[2] - yHat) * trainingData[0]
        wj += learningRate * (trainingData[2] - yHat) * trainingData[1]
        w0 += learningRate * (trainingData[2] - yHat)
    iteration += 1

runningTime = time.time() - startTime
print ("time: {}".format(runningTime))
print (wi)
print (wj)
print (w0)

Result = PredictClass(data)
print(Result)
plt.scatter([x[0] for x in data], [x[1] for x in data], c=Result)
plt.show()


result_s = []
result_n = []
for testingData in testingList:
    yHat = stepFunction(wi * testingData[0] + wj * testingData[1] + w0)
    if yHat==1:
        result_s.append(testingData)
    else:
        result_n.append(testingData)

plt.plot([(-w0)/wi, 0],[0, (-w0)/wj])
plt.scatter([x[0] for x in result_n], [x[1] for x in result_n])
plt.scatter([x[0] for x in result_s], [x[1] for x in result_s])
# plt.xlim(0, 25)
plt.ylim(0, 25)
plt.show()


plt.plot(misClassifiedList)
plt.show()
