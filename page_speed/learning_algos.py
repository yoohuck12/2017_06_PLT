print(__doc__)

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
import math

class LearningAlgorithms:

    def __init__(self, data,  target):
        self.data = data
        self.target = target

    def linear_regression(self):
        data_X = self.data
        target_y = self.target

        # Split the data into training/testing sets
        n_rows = data_X.shape[0]
        train_index = math.ceil(n_rows * 0.7)
        test_index = n_rows - train_index
        data_X_train = data_X[:train_index, :]
        data_X_test = data_X[test_index:, :]

        target_y_train = target_y[:train_index]
        target_y_test = target_y[test_index:]
        print(data_X)
        print('----------------------------------------------------------------------------------------------------')
        print(data_X_train)
        print('----------------------------------------------------------------------------------------------------')
        print(data_X_test)
        # Create linear regression object
        regr = linear_model.LinearRegression()

        # Train the model using the training sets
        regr.fit(data_X_train, target_y_train)

        # The coefficients
        print('Coefficients: \n', regr.coef_)
        # The mean square error
        print("Residual sum of squares: %.2f"
              % np.mean((regr.predict(data_X_test) - target_y_test) ** 2))
        # Explained variance score: 1 is perfect prediction
        print('Variance score: %.2f' % regr.score(data_X_test, target_y_test))

        # Plot outputs
        plt.scatter(data_X_test[:, 1], target_y_test,  color='black')
        plt.plot(data_X_test[:, 1], regr.predict(data_X_test), color='blue', linewidth=3)

        plt.xticks(())
        plt.yticks(())

        plt.show()