import numpy as np
import matplotlib.pyplot as plt

mu, sigma = 2, 0.5
v = np.random.normal(mu,sigma,10000)
plt.hist(v,bins = 500, normed = 1)  #hist=柱狀圖，bins=有幾條
plt.show()