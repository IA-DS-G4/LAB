import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import accuracy_score
from matplotlib import pyplot as plt

X = pd.read_csv("../../Unsorted/Data files/CSV DATA FILES/ML_Data/X.csv")
Y = pd.read_csv("../../Unsorted/Data files/CSV DATA FILES/ML_Data/y_alt.csv")

#divide training and test data
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)

model = SGDRegressor()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
predictions_rounded = [round(num) for num in predictions]
print(predictions)
print(predictions_rounded)
accuracy = accuracy_score(y_test, predictions_rounded)
print(accuracy)