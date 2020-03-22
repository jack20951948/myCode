from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras import regularizers
from keras import optimizers
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error 
from matplotlib import pyplot as plt
import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings 
warnings.filterwarnings('ignore')
warnings.filterwarnings('ignore', category=DeprecationWarning)
from xgboost import XGBRegressor
import time

# random seed
np.random.seed(0)

def get_data():
    raw_data = pd.read_csv(r"paperCreater\final_all_zscore\final_all_zscore.csv")
    raw_data.hist(figsize = (12,10))

    return raw_data

def data_process(data):
    X = data[['wbc', 'temp', 'cre', 'total', 'resp_rate', 'alb', 'hr', 'sys_bp', 'hematocrit', 'pH', 'glucose_blood', 'platelets', 'lactate', 'bun', 'sodium', 'potassium', 'nlr', 'bcd', 'DISCHARGE_LOCATION', 'age', 'GENDER', 'Neoplastic_disease', 'intubation', 'CONGESTIVE_HEART_FAILURE', 'OTHER_NEUROLOGICAL', 'LIVER_DISEASE', 'RENAL_FAILURE', 'glucose_pleural', 'final_O2']]
    y = data[['duration']] # np.ravel(raw_data[['duration']])

    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2, random_state=42)
    # print(len(Xtrain), len(Xtest), len(ytrain), len(ytest))
    ytrain = np.ravel(ytrain[['duration']])

    X['Target'] = y

    C_mat = X.corr()
    plt.figure(figsize = (15,15))

    sb.heatmap(C_mat, vmax = .8, square = True)

    return Xtrain, Xtest, ytrain, ytest

def get_cols_with_no_nans(df,col_type):
    '''
    Arguments :
    df : The dataframe to process
    col_type : 
          num : to only get numerical columns with no nans
          no_num : to only get nun-numerical columns with no nans
          all : to get any columns with no nans    
    '''
    if (col_type == 'num'):
        predictors = df.select_dtypes(exclude=['object'])
    elif (col_type == 'no_num'):
        predictors = df.select_dtypes(include=['object'])
    elif (col_type == 'all'):
        predictors = df
    else :
        print('Error : choose a type (num, no_num, all)')
        return 0
    cols_with_no_nans = []
    for col in predictors.columns:
        if not df[col].isnull().any():
            cols_with_no_nans.append(col)
    return cols_with_no_nans

def oneHotEncode(df,colNames):
    for col in colNames:
        if( df[col].dtype == np.dtype('object')):
            dummies = pd.get_dummies(df[col],prefix=col)
            df = pd.concat([df,dummies],axis=1)

            #drop the encoded column
            df.drop([col],axis = 1 , inplace=True)
    return df

def neural_network(train, target):
    x_train = np.array(train)
    y_train = target

    NN_model = Sequential()

    # The Input Layer :
    NN_model.add(Dense(29, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),input_dim = x_train.shape[1], activation='relu'))

    # The Hidden Layers :
    NN_model.add(Dense(58, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),activation='relu'))
    NN_model.add(Dense(58, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),activation='relu'))
    NN_model.add(Dense(58, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),activation='relu'))
    NN_model.add(Dense(58, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),activation='relu'))
    NN_model.add(Dense(29, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),activation='relu'))



    # The Output Layer :
    NN_model.add(Dense(1, kernel_initializer='normal',activation='linear'))

    # Compile the network :
    sgd = optimizers.Adadelta(lr=0.33, decay=1e-6)
    NN_model.compile(loss='mean_absolute_error', optimizer=sgd, metrics=['accuracy'])
    NN_model.summary()

    checkpoint_name = "paperCreater/model/Weights-{epoch:03d}--{val_loss:.5f}.hdf5"
    earlystop = EarlyStopping(monitor="val_loss", patience=10)
    checkpoint = ModelCheckpoint(checkpoint_name, monitor='val_loss', verbose = 1, save_best_only = True, mode ='auto')
    callbacks_list = [earlystop, checkpoint]

    history = NN_model.fit(x_train, y_train, epochs=5000, batch_size=5, validation_split = 0.25, callbacks=callbacks_list)

    return history

def train_result(history):
    training_loss = history.history["loss"]
    test_loss = history.history["val_loss"]

    epoch_count = range(1, len(training_loss) + 1)

    plt.figure()
    plt.plot(epoch_count, training_loss, "r--")
    plt.plot(epoch_count, test_loss, "b-")
    plt.legend(["Training Loss", "Test Loss"])
    plt.xlabel("Epoch")
    plt.ylabel("Loss")

    training_accuracy = history.history["acc"]
    test_accuracy = history.history["val_acc"]

    plt.figure()
    plt.plot(epoch_count, training_accuracy, "r--")
    plt.plot(epoch_count, test_accuracy, "b-")
    plt.legend(["Training Accuracy", "Test Accuracy"])
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy Score")

def main():
    # load data and target
    df_data = get_data()
    df_data = df_data.fillna(-1)
    # print(df_data.isnull().any())

    # split train, test
    X_train, X_test, y_train, y_test = data_process(df_data)

    history = neural_network(X_train, y_train)

    train_result(history)
    

if __name__ == "__main__":
    startTime = time.time()
    main()
    print('\n###### Programe End / Process time: %.2f seconds ######' % (time.time() - startTime))

    plt.show()