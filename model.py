import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
import os
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import sklearn.metrics as skm
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV


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

df = df[df["Price Rs."] <= 100000000]
y = df["Price Rs."]  
X = df.drop(columns=["Price Rs."])
print(df)
# Optimal random_state is 47
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


param_grid_rf = {
    'n_estimators': [100, 300, 600],
    'max_depth': [10, 20, 30],
    'min_samples_leaf': [1, 2, 4]
}

param_grid_xgb = {
    'n_estimators': [500, 700, 900],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [5, 9, 12]
}

param_grid_lgbm = {
    'n_estimators': [500, 700, 900],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [5, 9, 12]
}

scoring = {
    'rmse': 'neg_root_mean_squared_error',
    'r2': 'r2'
}

# max depth = 29 ideally, min_samples_leaf = 2 , n_estimators = 106
rf = RandomForestRegressor(oob_score=True, random_state = 51)

# max_depth = 9 seems ideal so far, learning_Rate = 0.009, n_estimators = 1320
xgb = XGBRegressor(random_state = 51)

#model = learning_rate = 0.06,n_estimators = 613
lgbm = LGBMRegressor(random_state = 51, verbose = -1)

start = time.time()
grid_rf = GridSearchCV(estimator=rf, param_grid=param_grid_rf, cv=5, scoring=scoring, refit='rmse', n_jobs=-1)
grid_rf.fit(X_train, y_train)
rf_time = time.time() - start

print("Best Random Forest Params:", grid_rf.best_params_)
print("Best RMSE Score:", -grid_rf.best_score_)
print(f"Training Time (RF): {rf_time:.2f} seconds\n")
print("Cross-validated R²:", grid_rf.cv_results_['mean_test_r2'][grid_rf.best_index_])

start = time.time()
grid_xgb = GridSearchCV(estimator=xgb, param_grid=param_grid_xgb, cv=5, scoring=scoring, refit='rmse', n_jobs=-1)
grid_xgb.fit(X_train, y_train)
xgb_time = time.time() - start

print("Best XGBoost Params:", grid_xgb.best_params_)
print("Best RMSE:", -grid_xgb.best_score_)
print(f"Training Time (XGB): {xgb_time:.2f} seconds\n")
print("Cross-validated R²:", grid_xgb.cv_results_['mean_test_r2'][grid_xgb.best_index_])

start = time.time()
grid_lgbm = GridSearchCV(estimator=lgbm, param_grid=param_grid_lgbm, cv=5, scoring=scoring, refit='rmse', n_jobs=-1)
grid_lgbm.fit(X_train, y_train)
lgbm_time = time.time() - start

print("Best LightGBM Params:", grid_lgbm.best_params_)
print("Best RMSE Score:", grid_lgbm.best_score_)
print(f"Training Time (LGBM): {lgbm_time:.2f} seconds")
print("Cross-validated R²:", grid_lgbm.cv_results_['mean_test_r2'][grid_lgbm.best_index_])

'''plt.scatter(y_test, y_pred1, alpha=0.3, label='Random Forest', color='blue')
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
results_df.to_csv('model_predictions.csv', index=False)'''