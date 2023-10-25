import pandas as pd
import numpy as np
#import scikit-learn

data = pd.read_csv("../Unsorted/Data files/CSV DATA FILES/pyradiomicsBackup_25_10_2023.csv")
data = data.select_dtypes(include=[int, float])
pl_data = pd.read_csv("../pylidc/pylidc_csv.csv")
pl_data= pl_data.select_dtypes(include=[int, float])
print(pl_data.columns.tolist())
df = pd.concat([pl_data, data], axis=1)

def normalize_data(df):
    normalized_data = (df-df.min())/(df.max()-df.min())
    return normalized_data

#fs_df = df
#fs_df = fs_df.drop(fs_df[fs_df['malignancy'] == 3].index)



df_norm = normalize_data(df)