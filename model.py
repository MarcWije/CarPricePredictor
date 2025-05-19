import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import sklearn.metrics as skm

os.chdir("E:/7th Semester/Machine Learning/")

df = pd.read_csv('scrapes2.csv')

df["Brand Model"] = df["Brand"] + " " + df["Model"]

df.drop(columns=["Brand", "Model", "Edition"], inplace=True)

print(df)

# List of categorical columns
categorical_cols = ["Brand Model", "Fuel Type", "Transmission",  "Body Type", "Negotiable"]
df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

X = df.drop(columns=["Price Rs."])
y = df["Price Rs."]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(X_train)


print(df.isna().sum())

model = RandomForestRegressor(n_estimators=100, max_depth=12, oob_score=True, random_state=24)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("R² Score:", skm.r2_score(y_test, y_pred))
print("RMSE:", skm.root_mean_squared_error(y_test, y_pred))




