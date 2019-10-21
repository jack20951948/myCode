import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
from minisom import MiniSom
import numpy as np

def main():
    img = plt.imread('house.jpg')
    print(img.shape)
    plt.imshow(img)
    plt.show()
    pixels = np.reshape(img, (img.shape[0]*img.shape[1], 3))/255   #the data give to som should be normalized to 0~1
    print(pixels.shape)

    #forming the model
    som2 = MiniSom(3,3,3,sigma=0.1, learning_rate=0.2)
    
    som2.random_weights_init(pixels)
    starting_weights = som2.get_weights().copy()

    som2.train_random(pixels, 500)

    print("activation \n", som2.activation_response(pixels))

    qnt = som2.quantization(pixels)

    print('q_Error ', som2.quantization_error(pixels))

    clustered = np.zeros(img.shape)

    for i, q in enumerate(qnt):
        clustered[np.unravel_index(i, (img.shape[0], img.shape[1]))] = q
    
    plt.figure

main()