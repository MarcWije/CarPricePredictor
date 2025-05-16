Documentation of the ET 4103 - Machine Learning Module, as conducted in the 7th Semester of the ET Engineering Degree at KDU

Included is a log of the scraping and data classification of the data for the final assignment, which is a Car Price predictor.

BACKGROUND TO THE DATASET

Ikman.lk is a famous Sri Lankan website, with a reputation as a second hand online marketplace. Many car ads are posted on the site daily, at a rate of roughly 6 - 7 an hour during the course of data gathering for this module. For this reason, it was chosen as an ideal source for data. 

Ikman stores roughly 2 months worth of car listings, which amounted to about 5400 listings. However, as the price of listings may be updated, using the time of posting as a time label would not be suitable for analysis of the price variation over time. Suggestions would be to run the scripts every month or so and gather different datasets and compare. 

The data was cleaned by fixing typos, removing duplicate entries, as well as entries that had been removed from the site in the short interval between retrieving the URL and scraping the data from the HTML. 

Roughly 20% of cars did not have a Body Type specified. These were manually entered subsequently, based on publicly available information about the car model. Certain liberties were taken in categorising specific car models into body types, especially between the Crossover and SUV categories. 

Other potential issues with the data may include typos and mistakes on the part of the individual posting the listing. These are rare, but do occur (for example in the case of the Rs. 5 Million Land Cruiser)
