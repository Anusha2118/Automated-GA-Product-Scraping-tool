# Project Name: G2_Innovators

## Overview
This repository contains a tool designed for scraping product data from various sources, including social media platforms, news articles, and official websites of GA (Google Analytics) products. Additionally, it checks if these products are listed on G2 using the G2 API. The tool offers automation through a scheduler, allowing for periodic scraping tasks on a daily, monthly, or weekly basis.

## Key Features:
- **Scalable Scraping**: Utilizes asynchronous requests for efficient scraping, significantly reducing scraping time from 15 minutes to just 4 minutes.
- **Batch Processing**: Optimizes search efficiency by employing batch processing with an optimal batch size of 60.
- **Result Tracking**: Generates CSV files for both found and not found products, named with timestamps for easy tracking and analysis.
- **Future Integration**: Plans for future integration include accessing a database using a paid API to further enhance scalability and data management capabilities.

## Before running the script, ensure you have the following installed:
- Python 3.x
- Required Python packages :
  - 'pandas'
  - 'aiohttp'
  - 'beautifulsoup4'
  - 'requests'
  - 'nest_asyncio'
    
## Setup Instructions:
1. Clone the repository to your local machine.
2. Install the required packages as mentioned above.
3. Modify the configuration file to include necessary API keys, URLs, and other parameters.
4. Run the scheduler script to start automated scraping and checking tasks.

## How to run:
1. Run the 'Final_g2_innovators.ipynb' file on Google Colab.
2. Clone the GitHub link and run the 'main.py' file.

## Usage
- Customize the scheduler to suit your desired scraping frequency and sources.
- Monitor the generated CSV files for results and analyze them as needed.
- Integrate additional functionalities or APIs to extend the tool's capabilities further.

## Contributors
- Ankitha Ananth - PES1UG21CS090
- Anusha MV - PES1UG21CS101
- Bhuvan Vijay Kumar - PES1UG21CS140
