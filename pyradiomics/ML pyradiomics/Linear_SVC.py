import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from matplotlib import pyplot as plt

X = pd.read_csv("X.csv")
Y = pd.read_csv("y.csv")
Y = Y.values.ravel()

#The model
def LSVC(X,Y,epochs, test_size):
    e = np.arange(0, epochs)
    acc_array = np.array([])
    for i in e:
        # divide training and test data
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size)
        model = LinearSVC()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        acc_array = np.append(acc_array, accuracy)
        print("Accuracy:", accuracy)


    #calculate average accurcy
    mean_acc = np.mean(acc_array)

    #make a plot
    plt.plot(e, acc_array)
    plt.rcParams['font.size'] = '11'
    #plt.figure(figsize=(8, 6), dpi=1000)
    plt.title('Accuracy per epoch ' + "Dataset size: " + str(len(X)) + ' Nodules')
    plt.legend()
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.ylim(-0.05, 1.05)
    plt.axhline(mean_acc, color='red', linestyle='dashed', label='Mean accuracy')
    plt.show()
    return

#LSVC(X,Y,100, 0.1)


X_all = pd.read_csv("X_all_cleaned.csv")
Y = pd.read_csv("y_alt.csv")
Y = Y.values.ravel()
first_30 = np.arange(1, 30, 1)
last = np.arange(35, 100, 5)
feature_prop = np.concatenate(first_30,last)
print(feature_prop)
acc_array = []
test_size = 0.2
for p in feature_prop:
    X_new, f_statistic, p_values = f_selection_Percentile(X_all, Y, p)
    X_train, X_test, y_train, y_test = train_test_split(X_new, Y, test_size=test_size, random_state=1)
    model = LinearSVC()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    acc_array = np.append(acc_array, accuracy)
plt.plot(feature_prop, acc_array, label='Amout features used vs accuracy {}'.format(feature_prop))
plt.legend
plt.ylim(0, 1)
plt.show()
