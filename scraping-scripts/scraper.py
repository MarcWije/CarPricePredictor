import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Change as needed
os.chdir("E:/7th Semester/Machine Learning/")

# CSV file to store the retrieved data
file_path = 'ikman-scrapes.csv'
write_header = not os.path.exists(file_path)

# Iterates over each webpage on the site to obtain all car listings. 
# range should be modified based on the current number of listings on the site.
for i in range(1, 50): 
    all_data = []
    urls = []

    # Base link over which to iterate
    link = "https://ikman.lk/en/ads/sri-lanka/cars?sort=date&order=desc&buy_now=0&urgent=0&page=" + str(i)
    print(link)
    try:
        header = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(link, headers=header)
        soupint = BeautifulSoup(response.content, 'html.parser')

        # List of all listings in a page
        adlinks = soupint.find_all('a', class_ ='card-link--3ssYv gtm-ad-item')

        # Adds each listings url to the urls list
        for adlink in adlinks:
            truelink = "https://ikman.lk" + adlink['href']
            print(truelink)
            urls.append(truelink)

    except Exception as e:
        print(f"Failed to do anything")

    # Scrapes the data in each listing
    for url in urls:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            print(url)
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            data = {}

            # Finds each Price based on the standard CSS class used by the page
            price_element = soup.find('div', class_='amount--3NTpl')
            if price_element:
                data['Price (Rs.)'] = price_element.get_text(strip=True)
            else:
                data['Price (Rs.)'] = None

            data['Negotiable'] = 'Yes' if 'Negotiable' in soup.get_text() else 'No'

            # Each data point is located in a div container with the following class
            details = soup.find_all('div', class_='full-width--XovDn justify-content-flex-start--1Xozy align-items-normal--vaTgD flex-wrap-nowrap--3IpfJ flex-direction-row--27fh1 flex--3fKk1')

            # Seperates the scraped data into label-value pairs
            for detail in details:
                label_element = detail.find('div', class_='word-break--2nyVq label--3oVZK')
                value_element = detail.find('div', class_='word-break--2nyVq value--1lKHt')
                if label_element and value_element:
                    label = label_element.get_text(strip=True).rstrip(':')
                    value = value_element.get_text(strip=True)
                    data[label] = value

            # Structures the final data
            final_data = {
                'Brand': data.get('Brand'),
                'Model': data.get('Model'),
                'Edition': data.get('Trim / Edition'),
                'Year of Manufacture': data.get('Year of Manufacture'),
                'Transmission': data.get('Transmission'),
                'Fuel Type': data.get('Fuel type'),
                'Body Type': data.get('Body type'),
                'Engine Capacity (cc)': data.get('Engine capacity'),
                'Mileage (km)': data.get('Mileage'),
                'Price (Rs.)': data.get('Price (Rs.)'),
                'Negotiable': data.get('Negotiable'),
                'Rs. Per km': None 
            }
            print(final_data)
            all_data.append(final_data)

        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    # Adds all the data into a DataFrame
    df = pd.DataFrame(all_data)
    df.to_csv(file_path, mode='a', header=write_header, index=False)

    print("Data has been successfully scraped and saved to ikman-scrapes.csv.")
