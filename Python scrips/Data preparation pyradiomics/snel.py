import pandas as pd

pl1 = pd.read_csv(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\backup_03_11_2023_total\pylidc1-566.csv")
pl2 = pd.read_csv(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\backup_03_11_2023_total\pylidc566-1012.csv")
pr1 = pd.read_csv(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\backup_03_11_2023_total\pyradiomics1-566.csv")
pr2 = pd.read_csv(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\backup_03_11_2023_total\pyradiomics566-1012.csv")

pl1 = pl1.reset_index(drop=True)
pl2 = pl2.reset_index(drop=True)
pr1 = pr1.reset_index(drop=True)
pr2 = pr2.reset_index(drop=True)

df1 = pd.concat([pl1, pl2], axis=0)
df2 = pd.concat([pr1, pr2], axis=0)

#df = pd.concat([df1, df2], axis=0)

df1.to_csv(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\backup_03_11_2023_total\pylidc_total.csv", index=False)
df2.to_csv(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\backup_03_11_2023_total\pyradiomics_total.csv", index=False)