9th May 2025 4:21pm
Beginning scrape of ikman.lk. For the sake of conciseness, only 4-wheeled vehicles (cars, vans, etc.) were considered. Heavy vehicles and special vehicles were also ignored for this. 

4:33 pm 
Created GitHub repository. Excluded promoted ads from the scrape. 

12th May 2025 2:03pm
Decided to automate scrape using BeautifulSoup and a python script.

16th May 2025 5:24pm 
As the BeautifulSoup python script seemed to be working well for my purposes, I modified the script further to extract links from each page of ikman.lk's car ads itself. It does this by finding each element with the "card-link--3ssYv gtm-ad-item" class, extracting the href from each element, and saving it into a list. This list is then passed into the program created previously. 

11:00pm
Added all body types, removed invalid entries. Merged scraper2.py with scraper.py

17th May 2025 4:58pm
Removed duplicates