import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

os.chdir("E:/7th Semester/Machine Learning/")

file_path = 'scrapes.csv'
all_data = []
write_header = not os.path.exists(file_path)

urls = [
"https://ikman.lk/en/ad/toyota-axio-2017-for-sale-colombo-316",
"https://ikman.lk/en/ad/alfa-romeo-giulietta-2013-for-sale-colombo",
"https://ikman.lk/en/ad/toyota-land-cruiser-prado-250-vx-2024-for-sale-gampaha-5",
"https://ikman.lk/en/ad/ssang-yong-korando-diesel-2012-for-sale-colombo-1",
"https://ikman.lk/en/ad/audi-a5-2018-for-sale-colombo-178",
"https://ikman.lk/en/ad/suzuki-maruti-800-2007-for-sale-kalutara-1",
"https://ikman.lk/en/ad/mitsubishi-outlander-2013-for-sale-colombo-217",
"https://ikman.lk/en/ad/mazda-demio-2009-for-sale-colombo-216",
"https://ikman.lk/en/ad/mercedes-benz-s400-2014-for-sale-colombo-30",
"https://ikman.lk/en/ad/mercedes-benz-gle-400-2016-for-sale-colombo",
"https://ikman.lk/en/ad/jonway-a380-2012-for-sale-colombo-4",
"https://ikman.lk/en/ad/honda-civic-rs-turbo-2025-for-sale-colombo-1",
"https://ikman.lk/en/ad/toyota-raize-2023-for-sale-colombo-17",
"https://ikman.lk/en/ad/toyota-starlet-ep82-1997-for-sale-anuradhapura",
"https://ikman.lk/en/ad/land-rover-range-autobiography-2019-for-sale-gampaha",
"https://ikman.lk/en/ad/toyota-land-cruiser-prado-lc250-first-edition-2024-for-sale-colombo-1",
"https://ikman.lk/en/ad/toyota-land-cruiser-sahara-lc-300-facelift-2008-for-sale-gampaha",
"https://ikman.lk/en/ad/honda-fit-2012-for-sale-colombo-1215",
"https://ikman.lk/en/ad/toyota-corolla-wxb-2023-for-sale-colombo-2"
]

for url in urls:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        print(url)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        data = {}

        price_element = soup.find('div', class_='amount--3NTpl')
        if price_element:
            data['Price (Rs.)'] = price_element.get_text(strip=True)
        else:
            data['Price (Rs.)'] = None

        data['Negotiable'] = 'Yes' if 'Negotiable' in soup.get_text() else 'No'

        details = soup.find_all('div', class_='full-width--XovDn justify-content-flex-start--1Xozy align-items-normal--vaTgD flex-wrap-nowrap--3IpfJ flex-direction-row--27fh1 flex--3fKk1')

        for detail in details:
            label_element = detail.find('div', class_='word-break--2nyVq label--3oVZK')
            value_element = detail.find('div', class_='word-break--2nyVq value--1lKHt')
            if label_element and value_element:
                label = label_element.get_text(strip=True).rstrip(':')
                value = value_element.get_text(strip=True)
                data[label] = value

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

# Save everything to CSV
df = pd.DataFrame(all_data)
df.to_csv(file_path, mode='a', header=write_header, index=False)

print("Data has been successfully scraped and saved to car_scrapes.csv.")
