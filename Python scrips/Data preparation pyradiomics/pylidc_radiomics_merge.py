import pandas as pd

df = pd.read_csv("../../pylidc/pylidc_csv.csv")
df_sorted = df.sort_values('Patient_id',ignore_index=True)

data = pd.read_csv("../../Unsorted/Data files/CSV DATA FILES/backup 29_10/pyradiomicsBackup.csv")
print(df_sorted)
print(data)

df3 = pd.concat([df_sorted, data], axis=1)

print(df3)