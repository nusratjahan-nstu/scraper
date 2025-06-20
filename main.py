import os
import json
import gspread
from dotenv import load_dotenv

load_dotenv()

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")
GOOGLE_CREDS_JSON = os.getenv("GOOGLE_CREDS_JSON")

print("🧪 Loaded environment variables.")
print("Spreadsheet ID:", SPREADSHEET_ID)
print("Sheet Name:", SHEET_NAME)

try:
    creds_dict = json.loads(GOOGLE_CREDS_JSON)
    gc = gspread.service_account_from_dict(creds_dict)
    print("✅ Authenticated with Google Sheets API.")
    
    sh = gc.open_by_key(SPREADSHEET_ID)
    worksheet = sh.worksheet(SHEET_NAME)
    data = worksheet.get_all_records()
    
    print("📄 Data fetched from Google Sheet:")
    print(data)

except Exception as e:
    print("❌ ERROR:")
    print(e)
