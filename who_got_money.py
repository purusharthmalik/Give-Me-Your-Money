from datetime import date
from bs4 import BeautifulSoup
import requests
import pandas as pd
from utilities import seed_related

def latest_funds():
    title_links, title_names, dates = [], [], []
    idx, num_pages = 1, -1
    flag = True

    while idx != num_pages + 1:
        url = f"https://www.finsmes.com/{date.today().year}/{date.today().month}/page/{idx}"
        print(url)
        # Parsing the url
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Getting the number of pages
        if idx == 1:
            num_pages = int(soup.find(class_='pages').text.split(' ')[-1])

        # Getting the titles and dates
        title_elements = soup.findAll(class_='entry-title')
        date_elements = soup.findAll(class_='entry-date')

        for title_elem, date_elem in zip(title_elements[:-4], date_elements[:-4]):
            if pd.to_datetime(date_elem.text, ) == pd.to_datetime(date.today()):
                title = title_elem.find('a')
                # Checking if the title is related to a funded company
                if seed_related(title.text):
                    title_links.append(title.get('href'))
                    title_names.append(title.text)
                    dates.append(date_elem.text)
            else:
                flag = False
                break
        if flag == True:
            idx += 1
        else:
            break

    # Saving the data
    df = pd.DataFrame({'Date': dates, 
                    'Title': title_names, 
                    'Link': title_links})
    df.to_csv('latest_seed_money.csv')