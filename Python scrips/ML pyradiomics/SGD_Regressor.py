import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import accuracy_score
from matplotlib import pyplot as plt

X = pd.read_csv("X.csv")
Y = pd.read_csv("y_alt.csv")

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


def LSVC(X,Y,epochs, test_size):
    e = np.arange(0, epochs)
    acc_array = np.array([])
    for i in e:
        # divide training and test data
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        predictions_rounded = [round(num) for num in predictions]
        accuracy = accuracy_score(y_test, predictions_rounded)
        acc_array = np.append(acc_array, accuracy)
        print("Accuracy:", accuracy)

    #make a plot
    plt.plot(e, acc_array)
    plt.rcParams['font.size'] = '11'
    #plt.figure(figsize=(8, 6), dpi=1000)
    plt.title('Accuracy per epoch ' + "Dataset size: " + str(len(X)))
    plt.legend()
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    mean_acc = np.mean(acc_array)
    plt.axhline(mean_acc, color='red', linestyle='dashed', label='Mean accuracy')
    plt.show()
    return

LSVC(X,Y,100, 0.1)