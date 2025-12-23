# Car Price Predictor 

## Video Demo: https://youtu.be/4D_xyEVkiPM

This repository serves as documentation of the Car Price Prediction Model created for the final assignment of the course **ET 4103 - Machine Learning** , as conducted in the 7th Semester of the Electronics and Telecommunications Engineering Degree at KDU.
A Web App implementation of this model was also submitted as the final Project for Harvard's CS50x course.

Included is a log of the scraping and data classification of the data for the final assignment, which is a Car Price predictor.

## Introduction to the Problem

An issue that is becoming increasingly recognizable as being a familiar feature of the Sri Lankan experience is the state of the Vehicle Market. Forced to halt imports over the COVID-19 pandemic and subsequent economic crisis, the market has suffered from a lack of fresh goods along with the drastic depreciation of the Sri Lankan Rupee (LKR). With vehicle imports gradually opening up in the year 2025, the market is unmaginably changed compared to the market that existed 6 years ago. As brand-new vehicles are out of reach for the majority of the population, the highest demand is found in the used car market.

The Used Car market in Sri Lanka is highly volatile, and prices may fluctuate by roughly 30% within the span of a few months. In order to aid citizens in understanding what the value of a given vehicle may be, it was decided to use Machine Learning trained on commonly available data of the used car market, in order to predict the value of a vehicle based on key parameters commonly considered when purchasing a car. 

Included in this repository are the scripts to generate new datasets from **ikman.lk** and **riyasewana.com**, ensuring that the model can be easily trained on new data.

## Background to the Dataset

**Ikman.lk** is a famous Sri Lankan website, with a reputation as a second hand online marketplace. Many car ads are posted on the site daily, at a rate of roughly **6 - 7 an hour** during the course of data gathering for this module. For this reason, it was chosen as an ideal source for data.

Ikman stores roughly 2 months worth of car listings, which amounted to about **5400 listings**. However, as the price of listings may be updated, using the time of posting as a time label would not be suitable for analysis of the price variation over time. Suggestions would be to run the scripts every month or so and gather different datasets and compare. 

The data was scraped using the scraper.py program in the repository. It utilised python's **requests** library along with **BeautifulSoup**, to parse the retrieved HTML pages of each car ad and extract all the relevant fields of data from the site. This was all then compiled into a csv for checking and cleaning.

Additionally, in order to give the dataset higher diversity, another popular Sri Lankan car website - **Riyasewana.com** -  was scraped in a similar manner to ikman. The model utilizes these combined datasets for training. 

## Modifications to the compiled dataset 

The data was cleaned by fixing typos, removing duplicate entries, as well as entries that had been removed from the site in the short interval between retrieving the URL and scraping the data from the HTML. 

Roughly **20% of cars** did not have a *Body Type* specified. These were manually entered subsequently, based on publicly available information about the car model. Certain liberties were taken in categorising specific car models into body types, especially between the Crossover and SUV categories. 

Subsequently it was discovered that certain factors such as *Edition, Body Type,* and *Negotiability* did not contribute positively to the model, and these categories were dropped.

The final model utilized the following inputs for training: *Year of Manufacture, Engine Capacity(cc), Mileage(km), Brand/Model* (combined into one category for ease of training)*, Fuel Type, and Transmission Type.*  

Other potential issues with the data may include typos and mistakes on the part of the individual posting the listing. These are rare, but do occur (for example in the case of the Rs. 5 Million Toyota Land Cruiser)

## Machine Learning Model

Initially, this task was determined to be a regression problem, as the output value needed to be more or less a continuous range of prices. However, it was quickly apparent that *Multivariable Linear Regression* was a poor choice for the model, as many of the factors had non-linear relationships with the Price of the car, which was the desired predicted output. 

Therefore three commonly used ensemble methods were chosen: sklearn's **RandomForestRegressor**, **XGBoost Regressor**, and **LightGBM Regressor**. XGBoost and LightGBM used Gradient Boosting techniques in order to fit data. The two main metrics used to evaluate these models' performance were *R<sup>2</sup> Score* and *RMSE (Root Mean Squared Error)*. 

After much hyperparameter fine-tuning, and dataset pruning, it became apparent that LGBM consistently outperformed the other two, both in terms of accuracy along with speed. 

## Flask App development 

In order to provide the outputs from this model in a way users could access, a flask app was developed. It has two main routes, the default and "/predict".

The default route enables users to enter the details of the vehicle they are trying to predict the price for (Brand, Model, Fuel Type, Transmission, Engine Capacity, Mileage, and Year of Manufacture). It reads the existing brands and models from the pickled encoders, and populates a drop-down list with them. 

The "/predict" route then displays these results, along with the predicted price