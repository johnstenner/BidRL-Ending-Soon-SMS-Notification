pip install requests bs4 twilio


import requests
import datetime
from bs4 import BeautifulSoup
from twilio.rest import Client

# Replace USERNAME, PASSWORD, TWILIO_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER
# with the appropriate values
USERNAME = 'your_username'
PASSWORD = 'your_password'
TWILIO_SID = 'your_twilio_sid'
TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

# Use requests to log in to the website
login_url = 'https://www.bidrl.com/login'
payload = {'username': USERNAME, 'password': PASSWORD}
session = requests.Session()
response = session.post(login_url, data=payload)

# Use Twilio to set up the SMS client
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

while True:
    # Use requests to get the My Bids page
    bids_url = 'https://www.bidrl.com/myaccount/recentbids/hide_closed/1'
    response = session.get(bids_url)

    # Use Beautiful Soup to parse the HTML of the My Bids page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing the user's bids
    bids_table = soup.find('table', {'id': 'my-bids-table'})

    # Iterate through each row in the table (excluding the header row)
    for row in bids_table.find_all('tr')[1:]:
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
                # Send the SMS notification
                message = client.messages.create(
                    body=f'Auction {auction_id} for {item_name} ends in one hour!')
