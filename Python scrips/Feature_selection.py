import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold

#-loading data-> backup of 29/10/2023
#pyradiomics data
pr_data = pd.read_csv("../Unsorted/Data files/CSV DATA FILES/backup 29_10/pyradiomicsBackup.csv")

#total obliteration data
tot_data = pd.read_csv("../Unsorted/Data files/CSV DATA FILES/backup 29_10/total_data_obliterationBackup.csv")



#formtting of dataframe
#drop row where malignancy is 3
tot_data = tot_data.drop(tot_data[tot_data['Malignancy'] == 3].index)
#code for dropping columns manually
# 0-17, 19,20,21,22,23,27,28,29,30,31
columns_to_drop = np.arange(0,11)
columns_to_drop2 = np.arange(12,30)
columns_to_drop = np.append(columns_to_drop,  columns_to_drop2)
columns_to_drop = np.append(columns_to_drop,  [32,33,34,35,36,39,40,41,44,45])
tot_data.drop(columns=tot_data.columns[columns_to_drop],inplace=True)
#tot_data = pr_data.select_dtypes(include=[int, float])
tot_data.to_csv(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\backup 29_10\filewip.csv", index=False)

#normalizing data
def normalize_data(df):
    header = df.iloc[0]
    df.drop()
    normalized_data = (df-df.min())/(df.max()-df.min())
    return normalized_data

tot_data_norm = normalize_data(tot_data)

#getting rid of features with low variance
sel = VarianceThreshold(threshold=0)
sel.fit_transform(tot_data)
print(tot_data)




