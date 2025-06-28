# ET 4103 - Machine Learning

Documentation of the ET 4103 - Machine Learning Module, as conducted in the 7th Semester of the ET Engineering Degree at KDU.
A Web App implementation of this model was also submitted as the final Project for Harvard's CS50x course.

Included is a log of the scraping and data classification of the data for the final assignment, which is a Car Price predictor.

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

Initially, this task was determined to be a regression problem, as the output value needed to be more or less a continuous range of prices.  