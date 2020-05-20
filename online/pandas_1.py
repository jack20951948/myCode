import pandas as pd

df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', header = None)
print(df.tail())

df1 = pd.read_csv('MI_INDEX.csv', encoding = 'big5')
print(df1.head())