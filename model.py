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

print(df)
df = df.astype(int)

df = df[df["Price Rs."] <= 100000000]
y = df["Price Rs."]
X = df.drop(columns=["Price Rs."])

# Optimal random_state is 47
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

for j in range (1,100):
    
    i = (j + 2)%3 

    if i == 0:
        # max depth = 29 ideally, min_samples_leaf = 2 , n_estimators = 106
        model = RandomForestRegressor(n_estimators=106, oob_score=True, random_state = 51, max_depth = 29, min_samples_leaf = 2)
        print("\n" + "Iteration : " + str((j-1)/3))
        print("Random Forest Regressor : ")

    elif i == 1:    
        # max_depth = 9 seems ideal so far, learning_Rate = 0.009, n_estimators = 1320
        model = XGBRegressor(n_estimators= 1320, learning_rate= 0.009, max_depth= 9)
        print("XGBoost Regressor : ")

    elif i == 2:
        #model = learning_rate = 0.06,n_estimators = 613
        model = LGBMRegressor(n_estimators= 613, learning_rate= 0.057, verbose = -1)
        print("LGBM Regressor : ")

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("R² Score:", skm.r2_score(y_test, y_pred))
    print("RMSE:", skm.root_mean_squared_error(y_test, y_pred))

plt.scatter(y_test, y_pred, alpha=0.3)
plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Actual vs Predicted Price")
plt.plot([0, 100_000_000], [0, 100_000_000], 'r--')  # 45-degree line
plt.show()

