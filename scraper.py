import os
import json
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

# Load credentials from .env
load_dotenv()

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")
GOOGLE_CREDS_JSON = os.getenv("GOOGLE_CREDS_JSON")
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Headers for HTTP request
headers = {"User-Agent": "Mozilla/5.0"}

# URLs to scrape
category_urls = [
    "https://martplus.net/product-category/fruits-vegetables/fresh-vegetables/",
    "https://martplus.net/product-category/fruits-vegetables/fresh-fruits/",
    "https://martplus.net/product-category/meat-fish/"
]

# Get current time
scrape_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
all_products = []

def authenticate_google():
    """Authenticate with Google Sheets API"""
    if GOOGLE_CREDS_JSON.startswith('{'):
        creds_dict = json.loads(GOOGLE_CREDS_JSON)
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    else:
        creds = Credentials.from_service_account_file(GOOGLE_CREDS_JSON, scopes=SCOPES)
    return gspread.authorize(creds)

def scrape_category(base_url):
    """Scrape all pages of a category"""
    page = 1
    while True:
        url = f"{base_url}page/{page}/"
        print(f"🔍 Scraping: {url}")
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            break

        soup = BeautifulSoup(res.content, "html.parser")
        product_cards = soup.select("li.product")
        if not product_cards:
            break

        for card in product_cards:
            try:
                name = card.select_one("h2.woocommerce-loop-product__title").text.strip()
                price = card.select_one("span.woocommerce-Price-amount").text.strip()

                all_products.append({
                    "Name": name,
                    "Price": price,
                    "Scraped At": scrape_time
                })
            except Exception as e:
                print(f"⚠️ Error parsing product: {e}")

        page += 1
        time.sleep(1)

def update_google_sheet(dataframe):
    """Append data to a Google Sheet"""
    try:
        client = authenticate_google()
        spreadsheet = client.open_by_key(SPREADSHEET_ID)

        try:
            worksheet = spreadsheet.worksheet(SHEET_NAME)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=SHEET_NAME, rows="1000", cols="20")

        existing_rows = worksheet.get_all_values()
        if not existing_rows:
            worksheet.append_row(list(dataframe.columns))

        for _, row in dataframe.iterrows():
            worksheet.append_row(row.tolist())

        print("✅ Google Sheet updated successfully.")
    except Exception as e:
        print(f"❌ Google Sheet update failed: {e}")

# Run the scraper
for category_url in category_urls:
    scrape_category(category_url)

# Push to Google Sheet
if all_products:
    df = pd.DataFrame(all_products)
    update_google_sheet(df)
    print(f"✅ Total products scraped and uploaded: {len(df)}")
else:
    print("⚠️ No products found.")
