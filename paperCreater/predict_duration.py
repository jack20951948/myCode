from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.models import Sequential, Model
from keras.layers import Dense, Input
from keras import regularizers
from keras import optimizers
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import seaborn as sb
import pandas as pd
import numpy as np
import warnings 
warnings.filterwarnings('ignore')
warnings.filterwarnings('ignore', category=DeprecationWarning)
import time

predictType = 'duration'

def get_data():
    raw_data = pd.read_csv(r"paperCreater\final_all_zscore\final_all_zscore.csv")
    raw_data = raw_data.fillna(0)
    raw_data.hist(figsize = (15,12))

    return raw_data

def get_mean_centering_data():
    raw_data = pd.read_csv(r"paperCreater\final_all_zscore\final_all_zscore.csv")
    raw_data = raw_data.fillna(0)
    mean_data = raw_data.mean()
    mean_centering_data = raw_data - mean_data
    mean_centering_data.hist(figsize = (15,12))
    
    return mean_centering_data

def get_normalization_data():
    raw_data = pd.read_csv(r"paperCreater\final_all_zscore\final_all_zscore.csv")
    raw_data = raw_data.fillna(0)
    raw_data = raw_data[raw_data[predictType] < 43]
    max_data = raw_data.max()
    min_data = raw_data.min()
    range_data = max_data - min_data
    normalization_data = (raw_data - min_data)/range_data
    normalization_data.hist(figsize = (15,12))

    return normalization_data, min_data, range_data, raw_data[[predictType]].min(), (raw_data[[predictType]].max()-raw_data[[predictType]].min())

def data_process(data):
    X = data[['wbc', 'temp', 'cre', 'total', 'resp_rate', 'alb', 'hr', 'sys_bp', 'hematocrit', 'pH', 'glucose_blood', 'platelets', 'lactate', 'bun', 'sodium', 'potassium', 'nlr', 'bcd', 'DISCHARGE_LOCATION', 'age', 'GENDER', 'Neoplastic_disease', 'intubation', 'CONGESTIVE_HEART_FAILURE', 'OTHER_NEUROLOGICAL', 'LIVER_DISEASE', 'RENAL_FAILURE', 'glucose_pleural', 'final_O2']]
    y = data[[predictType]]

    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.25, random_state=int(time.time()))
    ytrain = np.ravel(ytrain[[predictType]])
    ytest = np.ravel(ytest[[predictType]])

    X['Target'] = y

    C_mat = X.corr()
    plt.figure(figsize = (15,15))

    sb.heatmap(C_mat, vmax = .8, square = True)

    return Xtrain, Xtest, ytrain, ytest

def autoencoder(data, test, y_test):
    data = np.array(data)
    test = np.array(test)
    
    # this is our input placeholder
    input_img = Input(shape=(data.shape[1],))
    # encoder layers
    encoded = Dense(15, activation='relu')(input_img)
    encoded = Dense(8, activation='relu')(encoded)
    encoder_output = Dense(2)(encoded)
    
    # decoder layers
    decoded = Dense(8, activation='relu')(encoder_output)
    decoded = Dense(15, activation='relu')(decoded)
    decoded = Dense(data.shape[1], activation='linear')(decoded)
    
    # construct the autoencoder model
    autoencoder = Model(input=input_img, output=decoded)
    
    # construct the encoder model for plotting
    encoder = Model(input=input_img, output=encoder_output)
    
    # compile autoencoder
    autoencoder.compile(optimizer='adam', loss='mse')
    
    # training
    autoencoder.fit(data, data,
                    nb_epoch=200,
                    batch_size=64,
                    shuffle=True)
    
    # plotting
    encoded_data = encoder.predict(data)
    encoded_imgs = encoder.predict(test)
    plt.figure()
    plt.scatter(encoded_imgs[:, 0], encoded_imgs[:, 1], c=y_test)
    plt.colorbar()
    plt.show()

    return encoded_data, encoded_imgs

def neural_network(train, target, xtest, ytest):
    x_train = np.array(train)
    y_train = target
    x_test = np.array(xtest)
    y_test = ytest

    NN_model = Sequential()

    # The Input Layer :
    NN_model.add(Dense(x_train.shape[1], kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),input_dim = x_train.shape[1], activation='relu'))

    # The Hidden Layers :
    NN_model.add(Dense(58, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),activation='relu'))
    NN_model.add(Dense(58, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),activation='relu'))
    NN_model.add(Dense(58, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),activation='relu'))
    NN_model.add(Dense(58, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),activation='relu'))
    NN_model.add(Dense(29, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),activation='relu'))

    # The Output Layer :
    NN_model.add(Dense(1, kernel_initializer='normal',activation='linear'))

    # Compile the network :
    sgd = optimizers.Adadelta(lr=0.2, decay=1e-6)
    NN_model.compile(loss='mean_absolute_error', optimizer=sgd, metrics=['accuracy'])
    NN_model.summary()

    checkpoint_name = r"paperCreater/model/Weights-{epoch:03d}--{val_loss:.5f}.hdf5"
    earlystop = EarlyStopping(monitor="val_loss", patience=5) 
    checkpoint = ModelCheckpoint(checkpoint_name, monitor='val_loss', verbose = 1, save_best_only = True, mode ='auto')
    callbacks_list = [earlystop, checkpoint]

    history = NN_model.fit(x_train, y_train, epochs=5000, batch_size=64, validation_split=0.33, callbacks=callbacks_list)

    return history, NN_model

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
    '''
    training_accuracy = history.history["accuracy"]
    test_accuracy = history.history["val_accuracy"]

    plt.figure()
    plt.plot(epoch_count, training_accuracy, "r--")
    plt.plot(epoch_count, test_accuracy, "b-")
    plt.legend(["Training Accuracy", "Test Accuracy"])
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy Score")
    '''
    
def main():
    # load data and target
    # df_data = get_data()
    # df_data = get_mean_centering_data()
    df_data, min_data, range_data, m, r = get_normalization_data()

    # split train, test
    X_train, X_test, y_train, y_test = data_process(df_data)
    
    encoded_train, encoded_test = autoencoder(X_train, X_test, y_test)

    history, NN_model = neural_network(X_train, y_train, X_test, y_test)

    train_result(history)
    raw_data = pd.read_csv(r"paperCreater\test.csv")
    # print(raw_data)
    # raw_data = raw_data.fillna(0)
    # print(raw_data)
    # max_data = raw_data.max()
    # min_data = raw_data.min()
    # range_data = max_data - min_data
    normalization_data = (raw_data - min_data)/range_data
    print(normalization_data)

    A = normalization_data[['wbc', 'temp', 'cre', 'total', 'resp_rate', 'alb', 'hr', 'sys_bp', 'hematocrit', 'pH', 'glucose_blood', 'platelets', 'lactate', 'bun', 'sodium', 'potassium', 'nlr', 'bcd', 'DISCHARGE_LOCATION', 'age', 'GENDER', 'Neoplastic_disease', 'intubation', 'CONGESTIVE_HEART_FAILURE', 'OTHER_NEUROLOGICAL', 'LIVER_DISEASE', 'RENAL_FAILURE', 'glucose_pleural', 'final_O2']]
    print(raw_data[[predictType]])
    print(r[0])
    print((NN_model.predict(A)*r[0])+m[0])
    
    # history, NN_model = neural_network(encoded_train, y_train, encoded_test, y_test)

    # train_result(history)
    

if __name__ == "__main__":
    startTime = time.time()
    main()
    print('\n###### Programe End / Process time: %.2f seconds ######' % (time.time() - startTime))

    plt.show()