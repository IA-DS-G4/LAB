import pandas as pd
import numpy as np
#import scikit-learn

<<<<<<< HEAD
#-loading data-> backup of 29/10/2023
#pyradiomics data
pr_data = pd.read_csv(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\backup 29_10\pyradiomicsBackup.csv")
=======
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

>>>>>>> 92b85242f81cf8b467d99f150a81173a5ed87236

#pylidc data
pl_data = pd.read_csv("../pylidc/pylidc_csv.csv")

#total obliteration data
tot_data = pd.read_csv(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\backup 29_10\total_data_obliterationBackup.csv")


#some unsorte code line
#df = pd.concat([pl_data, data], axis=1)
#pr_data = pr_data.select_dtypes(include=[int, float])


#code for dropping columns manually
# 0-17, 19,20,21,22,23,27,28,29,30,31
#columns_to_drop = np.arange(0,18)
#columns_to_drop = np.append(columns_to_drop, [19,20,21,22,23,27,28,29,30,31])
#pr_data.drop(columns=pr_data.columns[columns_to_drop],inplace=True)
tot_data = pr_data.select_dtypes(include=[int, float])
print(tot_data)


#normalizing dat
def normalize_data(df):
    normalized_data = (df-df.min())/(df.max()-df.min())
    return normalized_data

<<<<<<< HEAD
pr_data_norm = normalize_data(pr_data)
print(pr_data_norm)

#drop row where malignancy is 3
#fs_df = fs_df.drop(fs_df[fs_df['malignancy'] == 3].index)
=======
fs_df = df
#fs_df = fs_df.drop(fs_df[fs_df['Malignancy'] == 3].index)


df_norm = normalize_data(df)
>>>>>>> 92b85242f81cf8b467d99f150a81173a5ed87236
