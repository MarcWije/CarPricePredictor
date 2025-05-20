import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import sklearn.metrics as skm
import seaborn as sns
from scipy.stats import skew

os.chdir("E:/7th Semester/Machine Learning/")

df = pd.read_csv('ikman-scrapes.csv')
df.drop(columns=["Negotiable", "Edition", "Body Type"], inplace=True)

df2 = pd.read_csv('riya-scrapes.csv')
df = pd.concat([df, df2], ignore_index=True)


df["Brand Model"] = df["Brand"] + " " + df["Model"]
df.drop(columns=["Brand", "Model"], inplace=True)
df['Brand Model'] = df['Brand Model'].str.split().str[:2].str.join(" ")
df['Brand Model'] = df['Brand Model'].str.title()

# List of categorical columns
categorical_cols = ["Brand Model", "Fuel Type", "Transmission"]
df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

df = df.astype(int)

df = df[df["Price Rs."] <= 100000000]
df['Price_log'] = np.log1p(df['Price Rs.'])

y = df["Price_log"]
X = df.drop(columns=["Price_log"])

X_train, X_test, y_train, y_test_log = train_test_split(X, y, test_size=0.2, random_state=4)

model = RandomForestRegressor(n_estimators=200, oob_score=True, random_state=2)
model.fit(X_train, y_train)
y_pred_log = model.predict(X_test)
y_pred = np.expm1(y_pred_log)
y_test = np.expm1(y_test_log)

print("R² Score:", skm.r2_score(y_test, y_pred))
print("RMSE:", skm.root_mean_squared_error(y_test, y_pred))
mae = skm.mean_absolute_error(y_test, y_pred)
print("MAE:", mae)
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
print("MAPE:", mape, "%")

plt.hist(df['Price Rs.'], bins=100, color='skyblue', edgecolor='black')
plt.title("Vehicle Price Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.show()

plt.scatter(y_test, y_pred, alpha=0.3)
plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Actual vs Predicted Price")
plt.plot([0, 100_000_000], [0, 100_000_000], 'r--')  # 45-degree line
plt.show()
