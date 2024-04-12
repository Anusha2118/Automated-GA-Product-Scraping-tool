import sched
import time
import datetime
import pandas as pd
import aiohttp
import asyncio
#from bs4 import BeautifulSoup
import nest_asyncio
#import requests
from scrape import scrape_categories
from search import search_products_in_csv
from scrape import get_categories

# Allow running asyncio code in environments with an active event loop
nest_asyncio.apply()

async def main():
    def calculate_seconds(period):
        if period == 'daily':
            return 24 * 60 * 60
        elif period == 'weekly':
            return 7 * 24 * 60 * 60
        elif period == 'monthly':
            return 30 * 24 * 60 * 60
        elif period == '10minutes':
            return 10*60
        else:
            return "Invalid input. Please choose '10minutes','daily', 'weekly', or 'monthly'."
    period = input("Choose between 10minutes, daily, weekly, or monthly: ")
    duration=calculate_seconds(period)
    items = await get_categories()
    startup_data = await scrape_categories(items)
    flat_list = [item for sublist in startup_data for item in sublist]
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
    csv_filename = f'betalist_data_{timestamp}.csv'
    df = pd.DataFrame(flat_list)
    df.to_csv(csv_filename, index=False)
    print(f"Scraping complete. Data saved to '{csv_filename}'.")
    return duration
# Runs a scheduler that periodically executes the main scraping and product search tasks.
def run_scheduler():
    s = sched.scheduler(time.time, time.sleep)
    def scheduled_task():
        duration=asyncio.run(main())
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
        csv_filename = f'betalist_data_{timestamp}.csv'
        search_products_in_csv(csv_filename, batch_size=60)
        print("Next Cycle starts after 10 minutes:")
        s.enter(duration, 1, scheduled_task)

    s.enter(0, 1, scheduled_task)
    s.run()

if __name__ == "__main__":
    run_scheduler()