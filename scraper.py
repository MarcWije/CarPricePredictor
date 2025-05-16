import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

os.chdir("E:/7th Semester/Machine Learning/")

file_path = 'scrapes.csv'
all_data = []
write_header = not os.path.exists(file_path)

urls = [
"https://ikman.lk/en/ad/toyota-hilux-vigo-smart-cab-2010-for-sale-colombo-3",
"https://ikman.lk/en/ad/toyota-vitz-2015-for-sale-galle-16",
"https://ikman.lk/en/ad/bmw-520d-2013-for-sale-colombo-812",
"https://ikman.lk/en/ad/suzuki-wagon-r-fz-2014-for-sale-colombo-2280",
"https://ikman.lk/en/ad/honda-crv-master-piece-2018-for-sale-colombo-7",
"https://ikman.lk/en/ad/mercedes-benz-e250-2016-for-sale-colombo",
"https://ikman.lk/en/ad/kia-sportage-4wd-2011-for-sale-colombo",
"https://ikman.lk/en/ad/honda-fit-2014-for-sale-colombo-1009",
"https://ikman.lk/en/ad/toyota-yaris-cross-z-grade-2025-for-sale-colombo-1",
"https://ikman.lk/en/ad/suzuki-wagon-r-stingray-2014-for-sale-colombo-2453",
"https://ikman.lk/en/ad/toyota-carina-2000cc-diesel-1997-for-sale-colombo-27",
"https://ikman.lk/en/ad/toyota-prius-2nd-generation-2007-for-sale-monaragala-1",
"https://ikman.lk/en/ad/micro-rexton-7-seater-diesel-auto-2015-for-sale-colombo-21",
"https://ikman.lk/en/ad/toyota-chr-black-top-body-kit-2017-for-sale-colombo-23",
"https://ikman.lk/en/ad/toyota-yaris-g-grade-2023-for-sale-colombo-30",
"https://ikman.lk/en/ad/toyota-allion-g-grade-2012-for-sale-colombo-3",
"https://ikman.lk/en/ad/toyota-hilux-double-cab-2007-for-sale-colombo-59",
"https://ikman.lk/en/ad/suzuki-celerio-2016-for-sale-colombo-431",
"https://ikman.lk/en/ad/mitsubishi-lancer-station-wagon-1979-for-sale-kandy",
"https://ikman.lk/en/ad/toyota-land-cruiser-prado-250-vx-2024-for-sale-gampaha-5",
"https://ikman.lk/en/ad/alfa-romeo-giulietta-2013-for-sale-colombo",
"https://ikman.lk/en/ad/toyota-prius-4th-gen-zvw50-safty-2016-for-sale-kurunegala-1",
"https://ikman.lk/en/ad/daihatsu-boon-cliq-g-passo-moda-2019-for-sale-badulla-3",
"https://ikman.lk/en/ad/ssang-yong-korando-diesel-2012-for-sale-colombo-1"
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
