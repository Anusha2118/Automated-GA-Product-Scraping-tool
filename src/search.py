import sched
import time
import datetime
import pandas as pd
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import nest_asyncio
import requests

# Searches for products in batches using the G2 API.
# Returns lists of found and not found products.
def search_products_in_batches(product_names, batch_size=10):
    url = 'https://data.g2.com/api/v1/products'
    headers = {
        'Authorization': 'Token token=c9bb10f81b8415efeea89328f4f158f77f835308a2a955a2961f5474197e7801',
        'Content-Type': 'application/vnd.api+json'
    }

    found_products = []
    not_found_products = []
    for i in range(0, len(product_names), batch_size):
        batch = product_names[i:i + batch_size]
        batch_request_data = {'filter[name]': ','.join(batch)}
        response = requests.get(url, headers=headers, params=batch_request_data)
        if response.status_code == 200:
            data = response.json()
            products = data.get('data', [])
            for product_name in batch:
                matched_products = [product['attributes']['name'] for product in products if
                                    product_name.lower() == product['attributes']['name'].lower()]
                if matched_products:
                    found_products.extend(matched_products)
                else:
                    not_found_products.append(product_name)
        else:
            print(f"Failed to retrieve products. Status code: {response.status_code}")
    return found_products, not_found_products

# Reads product names from a CSV file.
# Returns a list of product names.
def read_product_names_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    return df['Name'].tolist()

# Searches for products from the csv file created by calling the function, saves found and not found products in csv files
def search_products_in_csv(csv_file, batch_size):
    found_products_all_files = []
    not_found_products_all_files = []
    product_names = read_product_names_from_csv(csv_file)
    found_products, not_found_products = search_products_in_batches(product_names, batch_size)
    found_products_all_files.extend(found_products)
    not_found_products_all_files.extend(not_found_products)
    df_found = pd.DataFrame({'Found Product Name': found_products})
    df_found.to_csv(f'found_{csv_file}', mode='a', index=False, header=False)
    print(f"CSV file created: found_{csv_file}")
    df_not_found = pd.DataFrame({'Not Found Product Name': not_found_products})
    df_not_found.to_csv(f'not_found_{csv_file}', mode='a', index=False, header=False)
    print(f"CSV file created: not_found_{csv_file}")
