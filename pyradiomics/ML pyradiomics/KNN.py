Y = pd.read_csv("ML pyradiomics/y.csv")
Y = Y.values.ravel()
X_all = pd.read_csv("ML pyradiomics/X_all_cleaned.csv")
first_30 = np.arange(1,30,1)
last = np.arange(35,100,5)
feature_prop = np.append(first_30,last)
test_size= 0.2
n_neighbors=5

def KNN(X,Y,iterations, test_size,n_neighbors,p=2):
    e = np.arange(0, iterations)
    acc_array = np.array([])
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    for i in e:
        # divide training and test data
        X, f_statistic, p_values = f_selection_Percentile(X_all,Y,p)
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        acc_array = np.append(acc_array, accuracy)
        #print("Accuracy:", accuracy)


    #calculate average accurcy
    mean_acc = np.mean(acc_array)

    #make a plot
    plt.plot(e, acc_array, label='Mean value {}'.format(mean_acc))
    plt.rcParams['font.size'] = '11'
    #plt.figure(figsize=(8, 6), dpi=1000)
    plt.title('Accuracy per iteration, ' + "Dataset size: " + str(len(X)) + ' Nodules')
    plt.xlabel('Iteration')
    plt.ylabel('accuracy')
    plt.ylim(-0.05, 1.05)
    plt.axhline(mean_acc, color='red', linestyle='dashed', label='Mean accuracy')
    plt.legend()
    plt.show()

def feature_amount(X,Y, feature_prop,test_size,n_neighbors,p=2):
    acc_array = []
    model =  KNeighborsClassifier(n_neighbors=n_neighbors)
    for p in feature_prop:
        X, f_statistic, p_values = f_selection_Percentile(X_all,Y,p)
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=1)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        acc_array = np.append(acc_array, accuracy)
    #plotting
    max_acc = np.argmax(acc_array)
    best_perf = feature_prop[max_acc] # print hyperparameter with best accuracy
    plt.plot(feature_prop,acc_array, label='Best accuracy for: {}% of features used'.format(best_perf))
    plt.ylim(0,1)
    plt.title('Accuracy vs percentage of features used')
    plt.legend()
    plt.show()

KNN(X,Y,100, test_size,14)
feature_amount(X,Y,feature_prop,test_size, n_neighbors)


def neighbors_test(X, Y, test_size, neighbors_test_set, p=2):
    acc_array = []

    X, f_statistic, p_values = f_selection_Percentile(X_all, Y, p)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=1)
    for n in neighbors_test_set:
        model = KNeighborsClassifier(n_neighbors=n)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        acc_array = np.append(acc_array, accuracy)
    # plotting
    max_acc = np.argmax(acc_array)
    best_perf = feature_prop[max_acc]  # print the hyperparameter with best accuracy
    plt.plot(neighbors_test_set, acc_array, label='Best accuracy for n={}'.format(best_perf))
    plt.ylim(0, 1)
    plt.xlabel("n neighbors")
    plt.ylabel("Accuracy")
    plt.title('Accuracy vs amount of neighbors')
    # plt.figure(figsize=(10, 5))  # width=10 inches, height=5 inches
    plt.legend()
    plt.show()


neighbors_test_set = np.arange(1, 400)
neighbors_test(X, Y, test_size, neighbors_test_set)