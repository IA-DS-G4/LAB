import pandas as pd
import numpy as np
import sklearn

df = pd.read_csv("../Unsorted/Data files/intermediate result pydiacom_25_10_2023/total_data_obliterationBackup.csv")
df = df.select_dtypes(include=[int, float])

Y = df["Category"]
X = df

sklearn.svm.LinearSVC()