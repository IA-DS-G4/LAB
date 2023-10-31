import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import SelectPercentile

#-loading data-> backup of 29/10/2023
#pyradiomics data
pr_data = pd.read_csv("../Unsorted/Data files/CSV DATA FILES/backup 29_10/pyradiomicsBackup.csv")

#pylidc data
pl_data = pd.read_csv("../Unsorted/Data files/CSV DATA FILES/backup 29_10/pylidcBackup.csv")

#total obliteration data
df = pd.read_csv("../Unsorted/Data files/CSV DATA FILES/backup 29_10/total_data_obliterationBackup.csv")

def cleaning_data(df):
    df = df.drop(df[df['Malignancy'] == 3].index)
    # Remove rows with NaN values in the "Malignancy" column
    df.dropna(subset=["Malignancy"], inplace=True)
    threshold = df.shape[1] - 10  # 10 or more NaN values to be dropped
    df = df.dropna(thresh=threshold)
    return df
def normalize_data(df):
    normalized_data = (df-df.min())/(df.max()-df.min())
    return normalized_data

def create_category_column(df):
    # Create a new "Category" column based on the "Malignancy" values
    df["Category"] = df["Malignancy"].apply(lambda x: 1 if x in [4, 5] else 0)
    # drop all categories which are not numerical
    df = df.select_dtypes(include=[int, float])
    constant_columns = [col for col in df.columns if df[col].nunique() == 1]
    df = df.drop(columns=constant_columns)
    return df

def get_malignancy_column_dtype(df):
    # Check if the "Malignancy" column exists in the DataFrame
    if "Malignancy" in df.columns:
        malignancy_dtype = df["Malignancy"].dtype
        return malignancy_dtype
    else:
        return "Column 'Malignancy' not found in the DataFrame."

def f_selection_KBest(X,y,k=100):
    X_new = SelectKBest(f_classif, k=k).fit_transform(X, y)
    f_statistic, p_values = f_classif(X, y)
    return X_new, f_statistic, p_values

def f_selection_Percentile(X,y,p=10):
    X_new = SelectPercentile(f_classif, percentile=p).fit_transform(X,y)
    f_statistic, p_values = sklearn.feature_selection.f_classif(X,y)
    return X_new, f_statistic, p_values

def feature_select_plot(f_stat,p_val):
    # Create a DataFrame to store and sort the F-statistic and p-values
    results_df = pd.DataFrame({'F-Statistic': f_stat, 'p-Value': p_val})
    results_df = results_df.sort_values(by='p-Value', ascending=True)
    x_values = np.arange(0, len(f_stat), 1)

    # Plot the sorted F-statistic and p-values
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.barh(x_values, results_df['F-Statistic'], color='b')
    plt.xlabel('F-Statistic')
    plt.title('F-Statistic')
    plt.subplot(1, 2, 2)
    plt.barh(x_values, -np.log10(results_df['p-Value']), color='g')
    plt.xlabel('-log10(p-Value)')
    plt.title('p-Values (log scale)')
    plt.tight_layout()
    plt.show()

df = cleaning_data(df)
get_malignancy_column_dtype(df)
df = create_category_column(df)
df_norm = normalize_data(df)


# Creating the ML Dataset
X = df_norm.drop(columns=["Category","Malignancy"])  # X contains all columns except "Category"
y = df["Category"]  # y is the "Category" column

X_new, f_statistic, p_values = f_selection_Percentile(X,y)

feature_select_plot(f_statistic,p_values)

X_new_df = pd.DataFrame(X_new)


#getting rid of features with low variance
#sel = VarianceThreshold(threshold=0)
#sel.fit_transform(tot_data)
#print(tot_data)

X_new_df.to_csv("../Unsorted/Data files/CSV DATA FILES/ML_Data/X.csv", index=False)
y.to_csv("../Unsorted/Data files/CSV DATA FILES/ML_Data/y.csv", index=False)
