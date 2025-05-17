import pandas as pd
import os

os.chdir("E:/7th Semester/Machine Learning/")

df = pd.read_csv('scrapes2.csv')

print(df.to_string())