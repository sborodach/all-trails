import scipy.stats as scs
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', None)
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

from pymongo import MongoClient
from bs4 import BeautifulSoup

from time import sleep
from selenium import webdriver

import functions_


'''Using selenium to get webpage html for trails on a specific mountain or in a '''
trails_urls = []
mongo_db = #mountain/park name
for url in trails_urls:
    driver = webdriver.Chrome()
    client = MongoClient()

    driver.get(url)
    sleep(3)

    driver.execute_script("window.scrollTo(0, 10000)")

    # find 'show more reviews button'
    search = driver.find_element_by_css_selector("#reviews > div.styles-module__container___px-t2.xlate-none > button")

    # prevents error being thrown once total trail reviews is reached; 
    showing_results = driver.find_element_by_css_selector('#reviews > div.styles-module__container___px-t2.xlate-none > div')
    total_ = int(showing_results.text.split(' ')[-1])

    # clicks through to see additional reviews
    for _ in range(total_//30):
        search.click()
        sleep(1)

    # get page html
    html = driver.page_source
    time.sleep(2)

    # add html to mongo
    db = client.bearmountain
    trail_name = "".join(((" ".join(((url.split('/'))[-1]).split('-'))).title()).split(" "))
    pages = db[trail_name]
    pages.insert_one({'link': url, 'html': html})
    
'''Display '''
client = MongoClient()
db = client.bearmountain
db.list_collection_names()

'''Use stored html text in mongo to create mongo collection of hiking trail reviewer data'''
df = pd.DataFrame(list(db.BearMountainLoopTrail.find({})))
soup = BeautifulSoup(df.iloc[0,2], 'html.parser')

# getting trail title, description, difficulty, info
soup.find('h1', class_='xlate-none styles-module__name___1nEtW').text.rstrip()
soup.find('p', id="auto-overview").text.rstrip()
soup.find('span', class_="styles-module__diff___22Qtv styles-module__moderate___3w1it styles-module__selected___3fawg").text.rstrip()
soup.find('span', class_="styles-module__detailData___kQ-eK").text.rstrip()

soup_ratings = soup.find_all('span', class_="MuiRating-root default-module__rating___1k45X MuiRating-sizeLarge MuiRating-readOnly")
soup_dates = soup.find_all('span', class_="styles-module__dateTrailDetails___3qgZC xlate-none")
soup_types = soup.find_all('span', class_="styles-module__tag___2s-oD styles-module__activityTag___3-RdN")
soup_reviews = soup.find_all('div', class_="styles-module__container___3etfA")

# getting reviewer data for trail, appending to lists
for i, review in enumerate(soup.find_all('div', itemprop="review")):
    d = {'ratings': [], 'dates': [], 'types': [], 'written_review': []}
    d['ratings'] = soup_ratings[i]['aria-label']
    d['dates'] = soup_dates[i].text.rstrip()
    d['types'] = soup_types[i].text.rstrip()

    written_review = soup_reviews[i].find('p', itemprop="reviewBody")

    if written_review == None:
        d['review_text'] = (None)

    else:
        d['review_text'] = (soup.find_all('div', class_="styles-module__container___3etfA")[i].find('p', itemprop="reviewBody").text.rstrip())
        
    client = MongoClient()
    db = client.bearmountain
    db.BearMountainLoopTrail.insert_one(d)