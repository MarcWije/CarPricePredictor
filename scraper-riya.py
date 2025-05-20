import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

os.chdir("E:/7th Semester/Machine Learning/")

file_path = 'riya-scrapes.csv'
write_header = not os.path.exists(file_path)


for i in range(215, 233): 
    all_data = []
    urls = []
    link = "https://riyasewana.com/search/cars?page=" + str(i)
    print(link)
    try:
        header = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(link, headers=header)
        soupint = BeautifulSoup(response.content, 'html.parser')

        adlinks = soupint.find_all('h2', class_ ='more')

        for adlink in adlinks:
            a_tag = adlink.find('a')
            truelink = a_tag['href']
            print(truelink)
            urls.append(truelink)

    except Exception as e:
        print(f"Failed to do anything")

    for url in urls:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            print(url)
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

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

    df = pd.DataFrame(all_data)
    df.to_csv(file_path, mode='a', header=write_header, index=False)

    print("Data has been successfully scraped and saved to riya-scrapes.csv.")
