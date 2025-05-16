import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

os.chdir("E:/7th Semester/Machine Learning/")

file_path = 'scrapes2.csv'
all_data = []
write_header = not os.path.exists(file_path)


for i in range(1, 200): 
    urls = []
    link = "https://ikman.lk/en/ads/sri-lanka/cars?sort=date&order=desc&buy_now=0&urgent=0&page=" + str(i)
    print(link)
    try:
        header = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(link, headers=header)
        soupint = BeautifulSoup(response.content, 'html.parser')

        adlinks = soupint.find_all('a', class_ ='card-link--3ssYv gtm-ad-item')

        for adlink in adlinks:
            truelink = "https://ikman.lk" + adlink['href']
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

df = pd.DataFrame(all_data)
df.to_csv(file_path, mode='a', header=write_header, index=False)

print("Data has been successfully scraped and saved to scrapes2.csv.")
