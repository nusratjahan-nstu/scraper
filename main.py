import os
import json
import gspread

# Load environment variables (GitHub Actions will pass them in)
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")
GOOGLE_CREDS_JSON = os.getenv("GOOGLE_CREDS_JSON")

print("🧪 Loaded environment variables.")
print("Spreadsheet ID:", SPREADSHEET_ID)
print("Sheet Name:", SHEET_NAME)

# Fail fast if missing
if not GOOGLE_CREDS_JSON:
    print("❌ GOOGLE_CREDS_JSON is missing!")
    exit(1)

try:
    # Parse escaped JSON string into a dict
    creds_dict = json.loads(GOOGLE_CREDS_JSON)

    # Authenticate using the dictionary
    gc = gspread.service_account_from_dict(creds_dict)
    print("✅ Authenticated with Google Sheets.")

    # Access the spreadsheet and sheet
    sh = gc.open_by_key(SPREADSHEET_ID)
    worksheet = sh.worksheet(SHEET_NAME)
    data = worksheet.get_all_records()

    print("📄 Fetched data from sheet:")
    print(data)

except Exception as e:
    print("❌ ERROR:")
    print(repr(e))  # use repr to get the exact error class and message
