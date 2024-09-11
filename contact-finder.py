import os
from dotenv import load_dotenv
import pandas as pd
from pyhunter import PyHunter

load_dotenv()
df = pd.read_csv('final_data.csv')
companies = df['Company Name']

hunter = PyHunter(os.environ['PYHUNTER_API_KEY'])
contacts = dict()

for name in companies:
    # Searching for the domain
    domain = hunter.domain_search(company=name, limit=1)['domain']
    emails = []
    # Finding the email ids
    try:
        for email in hunter.domain_search(domain)['emails']:
            emails.append(email['value'])
        contacts[name] = emails
    except:
        contacts[name] = None

df['Contacts'] = list(contacts.values())

df.to_csv('includes_contacts.csv',
          index=False)
print('File saved!')