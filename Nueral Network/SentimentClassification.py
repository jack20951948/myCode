import numpy as np
from keras.datasets import imdb
from keras.preprocessing.text import Tokenizer
from keras import models
from keras import layers
from keras import regularizers
from keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt

# random seed
np.random.seed(0)

# define number of features
number_of_features = 1000

# load data and target
(data_train, target_train), (data_test, target_test) = imdb.load_data(
	num_words=number_of_features)

# transform the data to feature matrixs
tokenizer = Tokenizer(num_words=number_of_features)
feature_train = tokenizer.sequences_to_matrix(data_train, mode="binary")
feature_test = tokenizer.sequences_to_matrix(data_test, mode="binary")

# activate the neural network engine
network = models.Sequential()

# add activation function "relu"
network.add(layers.Dense(units=16, activation="relu", kernel_regularizer=regularizers.l2(0.01), input_shape=(number_of_features,)))

# add activation function "relu"
network.add(layers.Dense(units=16, activation="relu", kernel_regularizer=regularizers.l2(0.01)))

# add activation function "sigmoid"
network.add(layers.Dense(units=1, activation="sigmoid"))

# compile neural network
network.compile(loss="binary_crossentropy",
				optimizer="rmsprop",
				metrics=["accuracy"])

# stop early and save the best epoch's model
callbacks = [EarlyStopping(monitor="val_loss", patience=2), # check for more 2 epochs
			ModelCheckpoint(filepath="best_model.h5",       # save the best through checkpoint
							monitor="val_loss",
							save_best_only=True)]

# train neural network
history = network.fit(feature_train,
					  target_train,
					  epochs=15,
					  #callbacks=callbacks,
					  verbose=1,
					  batch_size=1000,
					  validation_data=(feature_test, target_test))


training_loss = history.history["loss"]
test_loss = history.history["val_loss"]

epoch_count = range(1, len(training_loss) + 1)

plt.figure()
plt.plot(epoch_count, training_loss, "r--")
plt.plot(epoch_count, test_loss, "b-")
plt.legend(["Training Loss", "Test Loss"])
plt.xlabel("Epoch")
plt.ylabel("Loss")

training_accuracy = history.history["accuracy"]
test_accuracy = history.history["val_accuracy"]

plt.figure()
plt.plot(epoch_count, training_accuracy, "r--")
plt.plot(epoch_count, test_accuracy, "b-")
plt.legend(["Training Accuracy", "Test Accuracy"])
plt.xlabel("Epoch")
plt.ylabel("Accuracy Score")
plt.show()