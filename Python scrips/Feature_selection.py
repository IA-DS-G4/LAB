import pandas as pd
import numpy as np
#import scikit-learn


column_header = pd.read_csv("../pylidc/pyradiomicsBackup_25_10_2023.csv",nrows=1)
column_names = column_header.columns[]
print(column_names)
data = pd.read_csv("../pylidc/pyradiomicsBackup_25_10_2023.csv", usecols=column_names, header= 0)
data = data.select_dtypes(include=[int, float])

normalized_data = (data- data.min())