import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold

#-loading data-> backup of 29/10/2023
#pyradiomics data
pr_data = pd.read_csv(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\backup 29_10\pyradiomicsBackup.csv")

#pylidc data
pl_data = pd.read_csv("../pylidc/pylidc_csv.csv")

#total obliteration data
df = pd.read_csv(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\backup 29_10\total_data_obliterationBackup.csv")


#code for dropping columns manually
# 0-17, 19,20,21,22,23,27,28,29,30,31
#columns_to_drop = np.arange(0,7)
#columns_to_drop = np.append(columns_to_drop, [])
#print(columns_to_drop)

#tot_data.drop(columns=tot_data.columns[columns_to_drop],inplace=True)
#tot_data.to_csv(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\backup 29_10\filewip.csv", index=False)
#print(tot_data)

#drop row where malignancy is 3

df = df.drop(tot_data[tot_data['malignancy'] == 3].index)

#normalizing data
def normalize_data(df):
    normalized_data = (df-df.min())/(df.max()-df.min())
    return normalized_data

def create_category_column(df):
    # Remove rows with NaN values in the "Malignancy" column
    df.dropna(subset=["Malignancy"], inplace=True)

    # Create a new "Category" column based on the "Malignancy" values
    df["Category"] = df["Malignancy"].apply(lambda x: 1 if x in [4, 5] else 0)
    # drop all categories which are not numerical
    df = pr_data.select_dtypes(include=[int, float])

    return df

df = create_category_column(df)
df_norm = normalize_data(df)
print(df_norm)

#getting rid of features with low variance
#sel = VarianceThreshold(threshold=0)
#sel.fit_transform(tot_data)
#print(tot_data)


