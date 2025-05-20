import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import sklearn.metrics as skm
import seaborn as sns

os.chdir("E:/7th Semester/Machine Learning/")

df = pd.read_csv('ikman-scrapes.csv')

df["Brand Model"] = df["Brand"] + " " + df["Model"]

df.drop(columns=["Brand", "Model", "Edition"], inplace=True)


# List of categorical columns
categorical_cols = ["Brand Model", "Fuel Type", "Transmission", "Negotiable", "Body Type"]
df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

df = df.astype(int)

df = df[df["Price Rs."] <= 100000000]

print(df)

y = df["Price Rs."]
X = df.drop(columns=["Price Rs."])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)

model = RandomForestRegressor(n_estimators=300, max_depth=20, min_samples_split=4, min_samples_leaf=2, oob_score=True, random_state=2)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

#sns.boxplot(df["Price Rs."])
#plt.title("Price Distribution")
#plt.xlabel("Price (Rs.)")
#plt.show()

print("R² Score:", skm.r2_score(y_test, y_pred))
print("RMSE:", skm.root_mean_squared_error(y_test, y_pred))

