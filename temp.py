import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.environ['APOLLO_API_KEY']

# Set the base URL for Apollo API
base_url = 'https://api.apollo.io/v1'

# Define the endpoint to search for contacts
search_contacts_url = f'{base_url}/contacts/search'

# Set the parameters for the search query
params = {
    'api_key': api_key,
    'q_organization_name': 'Google',  # Replace with the target company name
    'page': 1,  # Use pagination to handle large results
    'person_titles': [],  # Optionally filter by job title (e.g., 'Engineer', 'Manager')
    'per_page': 3
}

# Make the API request
response = requests.post(search_contacts_url, json=params)

if response.status_code == 200:
    data = response.json()
    print(data)
    contacts = data.get('contacts', [])
    emails = [contact['email'] for contact in contacts if 'email' in contact]
    print(emails)
else:
    print(f"Failed to retrieve data: {response.status_code} - {response.text}")
