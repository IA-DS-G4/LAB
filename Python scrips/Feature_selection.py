import pandas as pd
import numpy as np
#import scikit-learn

#-loading data-> backup of 29/10/2023
#pyradiomics data
pr_data = pd.read_csv(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\backup 29_10\pyradiomicsBackup.csv")

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

pr_data_norm = normalize_data(pr_data)
print(pr_data_norm)

#drop row where malignancy is 3
#fs_df = fs_df.drop(fs_df[fs_df['malignancy'] == 3].index)