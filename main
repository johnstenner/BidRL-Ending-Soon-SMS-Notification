import requests
import datetime
from bs4 import BeautifulSoup

# Replace USERNAME and PASSWORD with the appropriate values
USERNAME = 'your_username'
PASSWORD = 'your_password'

# Use requests to log in to the website
login_url = 'https://www.bidrl.com/login'
payload = {'username': USERNAME, 'password': PASSWORD}
session = requests.Session()
response = session.post(login_url, data=payload)

# Use Beautiful Soup to parse the HTML of the user's account page
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table containing the user's auction history
auction_history_table = soup.find('table', {'id': 'auction-history-table'})

# Iterate through each row in the table (excluding the header row)
for row in auction_history_table.find_all('tr')[1:]:
    # Find the cells in the row
    cells = row.find_all('td')
    
    # Extract the data from the cells
    auction_id = cells[0].text
    item_name = cells[1].text
    purchase_price = cells[2].text
    status = cells[3].text
    
    # Check if the auction is upcoming and the user has previously bid on it
    if status == 'Upcoming' and purchase_price != '-':
        # Find the time remaining for the auction
        time_remaining_cell = cells[4]
        time_remaining_text = time_remaining_cell.text.strip()
        time_parts = time_remaining_text.split(':')
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        seconds = int(time_parts[2])
        time_remaining = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        
        # Check if the auction ends in 1 hour
        if time_remaining <= datetime.timedelta(hours=1):
            # Send the notification
            print(f'Auction {auction_id} for {item_name} ends in 1 hour!')
