"""
Helper script to generate dummy models that can be used to test the solution.
The script fits different models on a random data.

"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from model import TrainedModel


def run():
    input_data = pd.read_csv('data/input.csv')
    input_features = ['age', 'sex', 'bmi', 'bp', 's1', 's2',
                      's3', 's4', 's5', 's6']
    X = input_data[input_features]
    y = input_data['target']

    # Train LinearRegression and save it as TrainedModel
    model = LinearRegression()
    model.fit(X, y)

    metadata = {
        "name": "Linear Regression",
        "version": "1"
    }
    trained_model = TrainedModel(model=model, metadata=metadata)
    trained_model.save("data/linear_regression.bin")

    # Train NeuralNetwork Regressor and save it as TrainedModel
    model = MLPRegressor(max_iter=1000, hidden_layer_sizes=(100, 50,))
    model.fit(X, y)

    metadata = {
        "name": "Neural Network Regression",
        "version": "1"
    }
    trained_model = TrainedModel(model=model, metadata=metadata)
    trained_model.save("data/neural_network_regression.bin")


if __name__ == "__main__":
    run()
