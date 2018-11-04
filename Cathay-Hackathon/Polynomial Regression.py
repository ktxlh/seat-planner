import numpy as np
from sklearn.linear_model import LinearRegression
import random 

rows = 20
num_of_features = 8
dataset = []
for i in range(rows):
    arr = []
    for j in range(4):
        arr.append(random.uniform(0, 1))
        arr.append(arr[-1] ** 2)
    arr.append(random.uniform(0, 1))
    dataset.append(arr)
dataset = np.array(dataset)    

def linear_regression(dataset):
    X_train = dataset[:, :8]
    y_train = dataset[:, 8]
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    weights = []
    for i in range(num_of_features):
        weights.append(regressor.coef_[i])
    return weights

# linear_regression(dataset)