import pandas as pd
import numpy as np

df = pd.read_excel("data/MWG.xlsx",index_col=0)
df.to_csv('data/MWG.csv')
print (df.head(5))