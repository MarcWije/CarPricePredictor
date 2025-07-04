**9th May 2025** *4:21pm*

Beginning scrape of **ikman.lk.** For the sake of conciseness, only 4-wheeled vehicles (cars, vans, etc.) were considered. Heavy vehicles and special vehicles were also ignored for this. 

*4:33 pm* 

Created **GitHub** repository. Excluded promoted ads from the scrape. 

**12th May 2025** *2:03pm*

Decided to automate scrape using **BeautifulSoup** and a python script.

**16th May 2025** *5:24pm* 

As the **BeautifulSoup** python script seemed to be working well for my purposes, I modified the script further to extract links from each page of **ikman.lk**'s car ads itself. It does this by finding each element with the *"card-link--3ssYv gtm-ad-item"* class, extracting the href from each element, and saving it into a list. This list is then passed into the program created previously. 

*11:00pm*

Added all body types, removed invalid entries. Merged *scraper2.py* with *scraper.py*

**17th May 2025** *4:58pm*

Removed duplicates from *scrapes2.csv*

*7:52pm* 

Began using the **pandas** library in python to import the csv and convert it to a dataframe. Read through **pandas** documentation

*8:40pm*

Removed commas from *Engine Capacity, Mileage,* and *Price* Columns in order for **pandas** to read it as floats

**19th May 2025** *11:03am*

Converted object classes to numerical values that **RandomForestRegressor** can handle, using one-hot encoding

*12:31pm* 

Experimented with different filters *(< Rs. 100 million, < Rs. 150 million, < Rs. 200 million)* to test the impact of the high end vehicles on the accuracy of the system. Removed data entries with obviously invalid price entries.

>Under Rs. 100 Million = RMSE = 5,195,997, 4669 entries
>Under Rs. 50 Million = RMSE = 3,878,609, 4290 entries

*2:28pm*

Began work on *scraper2.py* (subsequently renamed to *scraper-riya.py*), for scraping **riyasewana.com**, in order to diversify the dataset

**20th May 2025** *11:59am*

Finalized the **Riyasewana** dataset, cleaning up data entries and combining them in the model
Switched to logs for price values, as data was heavily right-skewed

*1:30pm*

Switched back to normal values, as this did not make a significant change in prediction accuracy

**25th May 2025** *4:00pm*

Did another round of **ikman** scrapes and cleaned up the dataset 

**26th May 2025** *1:02pm*

Tested using label encoding instead of one-hot encoding

Since label encoding ~~was better~~ showed better performance based on evaluation metrics, stuck with that

**27th May 2025** *9:07am* 

Set random_state to specific values to repeat performance

*12:22pm* 

Tuned Hyperparams of *Random Forest, XGBoost*, and *LGBM*

>Random Forest Regressor : 
>R² Score: 0.9426187041815014
>RMSE: 3500956.5900161876

>XGBoost Regressor : 
>R² Score: 0.9448541013747201
>RMSE: 3432085.979238174

>LGBM Regressor : 
>R² Score: 0.9451881134624761
>RMSE: 3421676.3264146997
>with random_state = 47

*1:27pm*

After testing multiple iterations, it was decided to go with LGBM as it had the overall lowest RMSE
Added model_predictions.csv to test which values are outliers

*2:41pm*

Removed some false data from the scrapes

**28th June 2025** *1:36pm*

Added comments to python scripts and updated the README to be more comprehensive

**4th July 2025** *2:06pm*

Added a comparison of all 3 models side by side

> Under Rs. 100 Million: 14128 entries total, LGBM RMSE: 3,437,160.7, R2 Score: 0.9450
> No Filter:  14266 entries total, LGBM RMSE: 6,848,711.4, R2 Score: 0.9003

*4:41pm*

Results of Grid Search:

>Best Random Forest Params: {'max_depth': 30, 'min_samples_leaf': 1, 'n_estimators': 600}
>Best RMSE Score: 3989102.748922088
>Training Time (RF): 646.28 seconds
>Cross-validated R²: 0.9278063202403288

>Best XGBoost Params: {'learning_rate': 0.1, 'max_depth': 5, 'n_estimators': 700}
>Best RMSE: 3874663.0912041427
>Training Time (XGB): 304.64 seconds
>Cross-validated R²: 0.9320513439566709

>Best LightGBM Params: {'learning_rate': 0.1, 'max_depth': 12, 'n_estimators': 700}
>Best RMSE Score: -3812577.860418172
>Training Time (LGBM): 91.16 seconds
>Cross-validated R²: 0.9340429427762142