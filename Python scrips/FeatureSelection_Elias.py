import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold

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
    return df
def normalize_data(df):
    normalized_data = (df-df.min())/(df.max()-df.min())
    return normalized_data

def create_category_column(df):
    # Create a new "Category" column based on the "Malignancy" values
    df["Category"] = df["Malignancy"].apply(lambda x: 1 if x in [4, 5] else 0)
    # drop all categories which are not numerical
    df = df.select_dtypes(include=[int, float])
    return df

def get_malignancy_column_dtype(df):
    # Check if the "Malignancy" column exists in the DataFrame
    if "Malignancy" in df.columns:
        malignancy_dtype = df["Malignancy"].dtype
        return malignancy_dtype
    else:
        return "Column 'Malignancy' not found in the DataFrame."

df = cleaning_data(df)
get_malignancy_column_dtype(df)
df = create_category_column(df)
df_norm = normalize_data(df)
print(df["Malignancy"])
print(df["Category"])
print(df_norm)

#getting rid of features with low variance
#sel = VarianceThreshold(threshold=0)
#sel.fit_transform(tot_data)
#print(tot_data)


