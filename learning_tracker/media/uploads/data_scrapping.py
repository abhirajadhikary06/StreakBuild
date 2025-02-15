import requests
from bs4 import BeautifulSoup
import csv
import os

# Print current working directory
print("Current working directory:", os.getcwd())

# URL to scrape
url = "https://finance.yahoo.com/quote/VZ/history/"

# Headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Fetch the webpage
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table by class name
    table = soup.find('table', {'class': 'table yf-j5d1ld noDl'})
    
    if table:
        # Specify full path to save file
        csv_file = os.path.join(os.getcwd(), "VZ_historical_data.csv")
        print(f"Saving CSV to: {csv_file}")
        
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Extract and write table rows to the CSV
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['th', 'td'])  # Include 'th' for header rows
                row_data = [cell.text.strip() for cell in cells]  # Extract text from each cell
                writer.writerow(row_data)  # Write row to CSV
        
        print(f"Data has been written to {csv_file}")
    else:
        print("Table not found on the page.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
