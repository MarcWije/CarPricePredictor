from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import random


# Change as needed
os.chdir("./data/")

# CSV file to store the retrieved data
file_path = 'riya-scrapes.csv'
write_header = not os.path.exists(file_path)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

# Iterates over each webpage on the site to obtain all car listings. 
# range should be modified based on the current number of listings on the site.
    for i in range(1, 233): 
        all_data = []
        urls = []
        link = f"https://riyasewana.com/search/cars?page={i}"
        print(link)

        try:
            page.goto(link, timeout=60000)
            page.wait_for_load_state("networkidle")
            time.sleep(2 + random.random() * 2)

            soupint = BeautifulSoup(page.content, 'html.parser')
            print(soupint.prettify()[:2000])

            # List of all listings in a page
            adlinks = soupint.find_all('h2', class_='more')

            # Adds each listings url to the urls list
            for adlink in adlinks:
                a_tag = adlink.find('a')
                truelink = a_tag['href']
                print(truelink)
                urls.append(truelink)

        except Exception as e:
            print(f"Failed to do anything")

        # Scrapes the data in each listing
        for url in urls:
            try:
                print(url)
                page.goto(url, timeout=60000)
                page.wait_for_load_state("networkidle")
                time.sleep(2 + random.random() * 2)
                soup = BeautifulSoup(page.content, 'html.parser')

                data = {}

                details = soup.find_all('td', class_='aleft')

                # Go through all td elements
                for i in range(0, len(details) - 1, 2):  # step by 2 to process label-value pairs
                    label_element = details[i].find('p', class_='moreh')
                    value_element = details[i + 1]

                    if label_element and value_element:
                        label = label_element.get_text(strip=True)
                        value = value_element.get_text(strip=True)
                        data[label] = value

                # Structures the final data
                final_data = {
                    'Brand': data.get('Make'),
                    'Model': data.get('Model'),
                    'Year of Manufacture': data.get('YOM'),
                    'Transmission': data.get('Gear'),
                    'Fuel Type': data.get('Fuel Type'),
                    'Engine Capacity (cc)': data.get('Engine (cc)'),
                    'Mileage (km)': data.get('Mileage (km)'),
                    'Price (Rs.)': data.get('Price'), 
                }
                print(final_data)
                all_data.append(final_data)

            except Exception as e:
                print(f"Failed to scrape {url}: {e}")

    # Adds all the data into a DataFrame
df = pd.DataFrame(all_data)
df.to_csv(file_path, mode='a', header=write_header, index=False)

print("Data has been successfully scraped and saved to riya-scrapes.csv.")
