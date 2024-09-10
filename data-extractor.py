import pandas as pd
import requests
from bs4 import BeautifulSoup
from utilities import extractor

df = pd.read_csv('seed_money.csv')

# Changing the index column and sorting it
df['Date'] = pd.to_datetime(df['Date'])
df.index = df['Date']
df.sort_index(inplace=True)

# Dataframe to store the final details
final_df = pd.DataFrame(columns=['Date', 'Company Name', 'Sector',
                                 'Summary', 'Amount'])

# Scraping each link and extracting the final data
for row in df.iterrows():
    url = row[1]['Link']
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')

    divs = soup.findAll(class_='tdb-block-inner')

    # Extracting the page content
    full_content = []
    for div in divs:
        content = div.findAll('p')
        if content != []:
            for para in content:
                full_content.append(para.text)

    # Creating the final string of data
    data = '\n'.join(full_content)

    # Extracting the data
    json_data = extractor(data)
    temp_df = pd.DataFrame([[row[0], 
                         json_data['company_name'],
                         json_data['sector'],
                         json_data['summary'],
                         json_data['amount']]],
                         columns=['Date', 'Company Name', 'Sector',
                                  'Summary', 'Amount'])

    final_df = pd.concat([final_df, temp_df])

final_df.to_csv('final_data.csv',
                index=False)