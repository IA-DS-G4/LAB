import pandas as pd
import numpy as np
#import scikit-learn

data = pd.read_csv("../Unsorted/Data files/intermediate result pydiacom_25_10_2023/total_data_obliterationBackup.csv")
data = data.select_dtypes(include=[int, float])
pl_data = pd.read_csv("../Unsorted/Data files/intermediate result pydiacom_25_10_2023/pylidcBackup.csv")
pl_data= pl_data.select_dtypes(include=[int, float])
print(pl_data.columns.tolist())
df = pd.concat([pl_data, data], axis=1)
dft = df.copy() # make a test copy of the dataframe


#moving rows up after the 11th column because its how the feature extractor stores it
dft.iloc[:, 12:] = df.iloc[:, 11:].values

print(dft.iloc[:, 40:50])
#print(df)


def normalize_data(df):
    normalized_data = (df-df.min())/(df.max()-df.min())
    return normalized_data

fs_df = df
#fs_df = fs_df.drop(fs_df[fs_df['Malignancy'] == 3].index)


df_norm = normalize_data(df)