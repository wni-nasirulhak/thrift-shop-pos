import sys
import os

# Add project root to sys.path so we can import src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.connection import connect_to_sheets

def setup_sheets():
    sheet = connect_to_sheets()
    if not sheet:
        print("❌ Could not connect to Google Sheets.")
        return

    print("✅ Connected to Google Sheets.")

    # 1. Setup Customers Sheet
    try:
        ws_customers = sheet.worksheet("Customers")
        print("ℹ️ 'Customers' sheet already exists.")
    except Exception:
        print("⚠️ 'Customers' sheet not found. Creating it...")
        ws_customers = sheet.add_worksheet(title="Customers", rows="1000", cols="5")
        headers = ["Phone_Number", "Customer_Name", "Points", "Total_Spent", "Last_Visit", "Created_At"]
        ws_customers.append_row(headers)
        print("✅ 'Customers' sheet created with headers.")

    # 2. Setup Shipping Sheet
    try:
        ws_shipping = sheet.worksheet("Shipping")
        print("ℹ️ 'Shipping' sheet already exists.")
    except Exception:
        print("⚠️ 'Shipping' sheet not found. Creating it...")
        ws_shipping = sheet.add_worksheet(title="Shipping", rows="1000", cols="6")
        headers = ["Sale_ID", "Barcode_ID", "Status", "Shipping_Address", "Tracking_No", "Updated_At"]
        ws_shipping.append_row(headers)
        print("✅ 'Shipping' sheet created with headers.")

    print("🎉 Setup complete!")

if __name__ == "__main__":
    setup_sheets()
