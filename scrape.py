import sched
import time
import asyncio
import pandas as pd
import aiohttp
from bs4 import BeautifulSoup
import nest_asyncio
import requests
import datetime

# Asynchronously fetches the HTML content of a given URL using an aiohttp session.
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

# Gets the catgeories from betalist and stores it as a list
async def get_categories():
    url = "https://betalist.com/topics"
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        categories = []
        for category in soup.find_all('a', class_='flex items-center gap-1 px-2 hover:bg-gray-100 group gap-4 hover:-my-[1px]'):
            category_href = category['href']  # Accessing the href attribute
            category_name = category_href.split('/')[-1]  # Extract category name from the URL
            categories.append(category_name)
        return categories

# Asynchronously scrapes startup data from the Betalist website for a given category.
# Returns a list of dictionaries containing startup information.
async def scrape_category(session, category):
    page_num = 1
    startup_data = []

    while True:
        url = f"https://betalist.com/topics/{category}?page={page_num}"
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find_all('div', class_='startupCard__details__text mt-3 text-base')

        if not articles:
            break

        for article in articles:
            startup_link = article.find('a')
            if startup_link:
                startup_name = startup_link.text.strip()
                block_text = article.text.strip().replace(startup_name, '').strip()
                startup_data.append({'Category': category, 'Name': startup_name, 'Block Text': block_text})

        page_num += 1

    return startup_data


#scrapes data for multiple categories concurrently using asynchronous programming techniques
async def scrape_categories(categories):
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_category(session, category) for category in categories]
        results = await asyncio.gather(*tasks)
        return results