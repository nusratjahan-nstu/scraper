import os
import gspread

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")

print("🧪 Loaded environment variables.")
print("Spreadsheet ID:", SPREADSHEET_ID)
print("Sheet Name:", SHEET_NAME)

try:
    gc = gspread.service_account(filename='credentials.json')
    print("✅ Authenticated with Google Sheets.")
    sheet = gc.open_by_key(SPREADSHEET_ID)
    worksheet = sheet.worksheet(SHEET_NAME)
    data = worksheet.get_all_records()
    print("📄 Sheet data:")
    print(data)

except Exception as e:
    print("❌ ERROR:")
    print(repr(e))
