import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import sklearn.metrics as skm
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV


os.chdir("E:/7th Semester/Machine Learning/")

df = pd.read_csv('data/ikman-scrapes.csv')

# Drops columns that seemingly do not contribute to the accuracy of the model
df.drop(columns=["Negotiable", "Edition", "Body Type"], inplace=True)


df2 = pd.read_csv('data/riya-scrapes.csv')
df = pd.concat([df, df2], ignore_index=True)
df = df[df["Fuel Type"] != "Electric"]

df["Brand"] = df["Brand"].fillna("Other")
df["Model"] = df["Model"].fillna("Other")

average_price = df['Price Rs.'].mean()
print("Average Price:", average_price)

average_mileage = df['Mileage (km)'].mean()
print("Mileage (km): ", average_mileage)

df["Brand Model"] = df["Brand"] + " " + df["Model"]
df.drop(columns=["Brand", "Model"], inplace=True)
df['Brand Model'] = df['Brand Model'].str.split().str[:2].str.join(" ")
df['Brand Model'] = df['Brand Model'].str.title()

# List of categorical columns
categorical_cols = ["Brand Model", "Fuel Type", "Transmission"]
encoders = {}

# Label encoding
for l in categorical_cols:
    encoder = LabelEncoder()
    classes = list(df[l].unique())
    if "Other Other" not in classes:
        classes.append("Other Other")
    encoder.fit(classes)
    # Transform and store encoded values
    
    df[l + "_E"]=encoder.transform(df[l].astype(str))
    encoders[l] = encoder
df.drop(columns=categorical_cols, inplace=True)

# One-hot encoding
#df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

df = df.astype(int)

df = df[df["Price Rs."] <= 20000000]
y = df["Price Rs."]  
X = df.drop(columns=["Price Rs."])
print(df)
# Optimal random_state is 47
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

'''
# max depth = 29 ideally, min_samples_leaf = 2 , n_estimators = 106
rf = RandomForestRegressor(oob_score=True, random_state = 51)

rf.fit(X_train, y_train)
y_pred1 = rf.predict(X_test)

print("RandomForest")
print("R² Score:", skm.r2_score(y_test, y_pred1))
print("RMSE:", skm.root_mean_squared_error(y_test, y_pred1))

# max_depth = 9 seems ideal so far, learning_Rate = 0.009, n_estimators = 1320
xgb = XGBRegressor(random_state = 51)

xgb.fit(X_train, y_train)
y_pred2 = xgb.predict(X_test)

print("XGBoost")
print("R² Score:", skm.r2_score(y_test, y_pred2))
print("RMSE:", skm.root_mean_squared_error(y_test, y_pred2))
'''
r2l = []
rmsel =[]
est = [] 


#model = learning_rate = 0.06,n_estimators = 613

lgbm = LGBMRegressor(verbose = -1, learning_rate = 0.06, n_estimators= 613, random_state = 42)

lgbm.fit(X_train, y_train)
y_pred3 = lgbm.predict(X_test)

r2 = skm.r2_score(y_test, y_pred3)
rmse = skm.root_mean_squared_error(y_test, y_pred3)

print("R² Score:", r2)
print("RMSE:", rmse)


with open("app/encoders.pkl", "wb") as f:
    pickle.dump(encoders, f)

with open("app/car-predict.pkl", "wb") as f:
    pickle.dump(lgbm, f)


#plt.scatter(y_test, y_pred1, alpha=0.3, label='Random Forest', color='blue')
#plt.scatter(y_test, y_pred2, alpha=0.3, label='XGBoost', color='green')
plt.scatter(y_test, y_pred3, alpha=0.3, label='LightGBM', color='orange')

plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label='Ideal Prediction')

plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Actual vs Predicted Car Prices")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


results_df = pd.DataFrame({'Actual Price': y_test, 'Predicted Price (LightGBM)': y_pred3})
results_df.to_csv('model_predictions.csv', index=False)

