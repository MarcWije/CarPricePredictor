import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import sklearn.metrics as skm
from sklearn.preprocessing import LabelEncoder
import seaborn as sns


os.chdir("E:/7th Semester/Machine Learning/")

df = pd.read_csv('ikman-scrapes.csv')

# Drops columns that seemingly do not contribute to the accuracy of the model
df.drop(columns=["Negotiable", "Edition", "Body Type"], inplace=True)


df2 = pd.read_csv('riya-scrapes.csv')
df = pd.concat([df, df2], ignore_index=True)
df = df[df["Fuel Type"] != "Electric"]

df["Brand Model"] = df["Brand"] + " " + df["Model"]
df.drop(columns=["Brand", "Model"], inplace=True)
df['Brand Model'] = df['Brand Model'].str.split().str[:2].str.join(" ")
df['Brand Model'] = df['Brand Model'].str.title()

# List of categorical columns
categorical_cols = ["Brand Model", "Fuel Type", "Transmission"]

# One-hot encoding
#df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Label encoding
for l in categorical_cols:
    encoder = LabelEncoder()
    df[l + "_E"]=encoder.fit_transform(df[l].astype(str))
df.drop(columns=categorical_cols, inplace=True)

df = df.astype(int)

#df = df[df["Price Rs."] <= 100000000]
y = df["Price Rs."]  
X = df.drop(columns=["Price Rs."])
print(df)
# Optimal random_state is 47
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


# max depth = 29 ideally, min_samples_leaf = 2 , n_estimators = 106
model1 = RandomForestRegressor(n_estimators=613, oob_score=True, random_state = 51, max_depth = 29, min_samples_leaf = 2)

# max_depth = 9 seems ideal so far, learning_Rate = 0.009, n_estimators = 1320
model2 = XGBRegressor(n_estimators= 613, learning_rate= 0.057, max_depth= 9)

#model = learning_rate = 0.06,n_estimators = 613
model3 = LGBMRegressor(n_estimators= 613, learning_rate= 0.057, verbose = -1)

model1.fit(X_train, y_train)
y_pred1 = model1.predict(X_test)

print("RandomForest")
print("R² Score:", skm.r2_score(y_test, y_pred1))
print("RMSE:", skm.root_mean_squared_error(y_test, y_pred1))

model2.fit(X_train, y_train)
y_pred2 = model2.predict(X_test)

print("XGBoost")
print("R² Score:", skm.r2_score(y_test, y_pred2))
print("RMSE:", skm.root_mean_squared_error(y_test, y_pred2))

model3.fit(X_train, y_train)
y_pred3 = model3.predict(X_test)

print("LightGBM")
print("R² Score:", skm.r2_score(y_test, y_pred3))
print("RMSE:", skm.root_mean_squared_error(y_test, y_pred3))

plt.scatter(y_test, y_pred1, alpha=0.3, label='Random Forest', color='blue')
plt.scatter(y_test, y_pred2, alpha=0.3, label='XGBoost', color='green')
plt.scatter(y_test, y_pred3, alpha=0.3, label='LightGBM', color='orange')

plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label='Ideal Prediction')

plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Actual vs Predicted Car Prices")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

results_df = pd.DataFrame({'Actual Price': y_test, 'Predicted Price (Random Forest)': y_pred1, 'Predicted Price (XGBoost)': y_pred2, 'Predicted Price (LightGBM)': y_pred3})
results_df.to_csv('model_predictions.csv', index=False)