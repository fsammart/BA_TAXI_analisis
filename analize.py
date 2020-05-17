import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
from sklearn.linear_model import LinearRegression

data = pd.read_csv('bataxi.csv')  # load data set
duration = data.iloc[:, 4].values.reshape(-1, 1)  # values converts it into a numpy array
passengers = data.iloc[:, 9].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
id_taxista = data.iloc[:, 1].values.reshape(-1, 1)
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(id_taxista, duration)  # perform linear regression
Y_pred = linear_regressor.predict(id_taxista)  # make predictions

plt.scatter(id_taxista, duration)
plt.plot(id_taxista, Y_pred, color='red')
plt.show()