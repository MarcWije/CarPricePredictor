import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

os.chdir("E:/7th Semester/Machine Learning/")

file_path = 'scrapes.csv'
all_data = []
write_header = not os.path.exists(file_path)

urls = [
"https://ikman.lk/en/ad/suzuki-baleno-2016-for-sale-colombo-264"
"https://ikman.lk/en/ad/toyota-prius-2nd-generation-2009-for-sale-gampaha",
"https://ikman.lk/en/ad/toyota-aqua-2015-x-urban-for-sale-colombo-1",
"https://ikman.lk/en/ad/toyota-land-cruiser-prado-txl-limited-2023-for-sale-gampaha-1",
"https://ikman.lk/en/ad/mitsubishi-lancer-box-1983-for-sale-anuradhapura",
"https://ikman.lk/en/ad/honda-civic-fd1-2007-for-sale-colombo-152",
"https://ikman.lk/en/ad/suzuki-wagon-r-fz-safety-2018-for-sale-colombo-859",
"https://ikman.lk/en/ad/toyota-aqua-2015-x-urban-for-sale-colombo-1",
"https://ikman.lk/en/ad/mercedes-benz-e200-facelift-premium-2023-for-sale-colombo-1",
"https://ikman.lk/en/ad/toyota-land-cruiser-sahara-lc300-zx-2023-for-sale-colombo-6",
"https://ikman.lk/en/ad/toyota-land-cruiser-prado-txl-2023-for-sale-colombo-4",
"https://ikman.lk/en/ad/toyota-land-cruiser-prado-txl-2023-for-sale-colombo-5",
"https://ikman.lk/en/ad/honda-crv-2018-for-sale-galle-6",
"https://ikman.lk/en/ad/suzuki-celerio-vxi-auto-2015-for-sale-gampaha-223",
"https://ikman.lk/en/ad/renault-kwid-rxt-air-bag-2017-for-sale-gampaha",
"https://ikman.lk/en/ad/ssang-yong-rexton-2009-for-sale-colombo-4",
"https://ikman.lk/en/ad/mercedes-benz-e200-cabriolet-2023-for-sale-colombo-3",
"https://ikman.lk/en/ad/land-rover-defender-110-p300e-s-auto-4wd-2024-for-sale-colombo",
"https://ikman.lk/en/ad/toyota-rush-s-grade-2019-for-sale-colombo",
"https://ikman.lk/en/ad/bajaj-qute-2019-for-sale-colombo-80",
"https://ikman.lk/en/ad/daihatsu-mira-2019-for-sale-jaffna",
"https://ikman.lk/en/ad/ssang-yong-actyon-2007-for-sale-kandy",
"https://ikman.lk/en/ad/hyundai-grand-i10-2025-for-sale-colombo-2",
"https://ikman.lk/en/ad/toyota-hilux-vigo-2007-for-sale-monaragala-1",
"https://ikman.lk/en/ad/toyota-land-cruiser-sahara-zx-fully-loaded-2023-for-sale-colombo",
"https://ikman.lk/en/ad/mazda-6-gt-2500cc-2014-for-sale-colombo-4",
"https://ikman.lk/en/ad/toyota-vitz-2019-for-sale-colombo-303"
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
