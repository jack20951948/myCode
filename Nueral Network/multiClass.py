import numpy as np
from keras.datasets import reuters
from keras.utils.np_utils import to_categorical
from keras.preprocessing.text import Tokenizer
from keras import models
from keras import layers
import matplotlib.pyplot as plt

# random seed
np.random.seed(0)

# define number of features
number_of_features = 5000

# load data and target
data = reuters.load_data(num_words=number_of_features)
(data_train, target_vector_train), (data_test, target_vector_test) = data
# print(data_train)
# print(target_vector_train)

# transform the data to feature matrixs
tokenizer = Tokenizer(num_words=number_of_features)
feature_train = tokenizer.sequences_to_matrix(data_train, mode="binary")
feature_test = tokenizer.sequences_to_matrix(data_test, mode="binary")

# one-hot encoding
target_train = to_categorical(target_vector_train)
target_test = to_categorical(target_vector_test)

# activate the neural network engine
network = models.Sequential()

# add activation function "relu"
network.add(layers.Dense(units=100, activation="relu", input_shape=(number_of_features,)))

# add activation function "relu"
network.add(layers.Dense(units=100, activation="relu"))

# add activation function "softmax"
network.add(layers.Dense(units=46, activation="softmax"))

# compile neural network
network.compile(loss="categorical_crossentropy",
				optimizer="rmsprop",
				metrics=["accuracy"])


# train neural network
history = network.fit(feature_train,
					  target_train,
					  epochs=15,
					  verbose=1,
					  batch_size=100,
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