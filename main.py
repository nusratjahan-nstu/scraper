import os
import gspread

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")

print("🧪 Loaded environment variables.")
print("Spreadsheet ID:", SPREADSHEET_ID)
print("Sheet Name:", SHEET_NAME)

if not SPREADSHEET_ID or not SHEET_NAME:
    raise ValueError("SPREADSHEET_ID and SHEET_NAME environment variables must be set.")

try:
    gc = gspread.service_account(filename='credentials.json')
    print("✅ Authenticated with Google Sheets.")
    sheet = gc.open_by_key(SPREADSHEET_ID)
    worksheet = sheet.worksheet(SHEET_NAME)
    data = worksheet.get_all_records()
    print(f"📄 Sheet data ({len(data)} rows):")
    print(data)

except Exception as e:
    print("❌ ERROR:")
    print(repr(e))
