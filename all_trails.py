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


trails_urls = [] #must instantiate this empty list
def get_all_trails_urls(park_url):

    '''Get all trails urls for specific mountain/park'''
    driver = webdriver.Chrome()
    driver.get(url)
    sleep(3)
    driver.execute_script("window.scrollTo(0, 3500)")
    search = driver.find_element_by_class_name("styles-module__button___1nuva ")

    for _ in range(100):
        try:
            search.click()
            sleep(1)
        except:
            pass
        
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.close()
    
    # collect hrefs
    hrefs = []
    divs = soup.find_all('div', "styles-module__containerDescriptive___3aZqQ styles-module__trailCard___2oHiP")
    for i, div in enumerate(divs):
        hrefs.append(soup.find_all('div', "styles-module__containerDescriptive___3aZqQ styles-module__trailCard___2oHiP")[i].a['href'])

    # concatenate website link with hrefs to get all park trail links
    for i, href in enumerate(hrefs):
        trails_urls.append('https://www.alltrails.com/' + href)

        
def get_all_trails_htmls(park_url, trails_urls):
    '''Using selenium to get webpage html for mountain/park trails'''
    for url in trails_urls:
    
        driver = webdriver.Chrome()
        client = MongoClient()
        park_name = (url.split('/'))[-1]
        db = client[park_name]

        driver.get(url)
        sleep(3)
        driver.execute_script("window.scrollTo(0, 10000)")
        search = driver.find_element_by_css_selector("#reviews > div.styles-module__container___px-t2.xlate-none > button")
        for _ in range(100):
            try:
                search.click()
                sleep(1)
            except:
                pass
        html = driver.page_source
        time.sleep(2)

        trail_name = "".join(((" ".join(((url.split('/'))[-1]).split('-'))).title()).split(" "))
        db[trail_name].insert_one({'link': url, 'html': html})
        
        driver.close()


def get_reviewer_data(park_url):
    '''Use stored html text in mongo to create mongo collection of hiking trail reviewer data'''
    
    client = MongoClient()
    park_name = (park_url.split('/'))[-1]
    db = client[park_name]
    
    for i, trail in enumerate(list(db.list_collection_names())[1:]):
        trail_name = (list(db.list_collection_names()))[i]
        df = pd.DataFrame(list(db[trail].find({})))
        soup = BeautifulSoup(df.iloc[0,2], 'html.parser')

        # getting trail title, description, difficulty, info
        soup.find('h1', class_='xlate-none styles-module__name___1nEtW').text.rstrip()
        soup.find('p', id="auto-overview").text.rstrip()
        soup.find('span', class_="styles-module__diff___22Qtv styles-module__moderate___3w1it styles-module__selected___3fawg").text.rstrip()
        soup.find('span', class_="styles-module__detailData___kQ-eK").text.rstrip()

        ratings = list(soup.find_all('span', class_="MuiRating-root default-module__rating___1k45X MuiRating-sizeLarge MuiRating-readOnly"))
        dates = list(soup.find_all('span', class_="styles-module__dateTrailDetails___3qgZC xlate-none"))
        highlights = list(soup.find_all('span', class_="styles-module__tag___2s-oD styles-module__activityTag___3-RdN"))
        reviews = list(soup.find_all('div', class_="styles-module__container___3etfA"))
        review_text = []

        # getting reviewer data for trail, appending to lists
        for i, review in enumerate(soup.find_all('div', itemprop="review")):
            d = {'ratings': [], 'dates': [], 'types': [], 'written_review': []}
            d['ratings'] = ratings[i]['aria-label']
            d['dates'] = dates[i].text.rstrip()
            d['highlights'] = highlights[i].text.rstrip()
            written_review = reviews[i].find('p', itemprop="reviewBody")

            if written_review == None:
                d['review_text'] = (None)
            else:
                d['review_text'] = reviews[i].find('p', itemprop="reviewBody").text.rstrip()
        
            db[trail_name].insert_one(d)

'''Converting stored mongo collections into one concatenated pandas dataframe'''
def panda_function():
    client = MongoClient()
    park_name = (url.split('/'))[-1]
    db = client[park_name]
    df = pd.DataFrame({'ratings': [], 'dates': [], 'highlights': [], 'review_text': []})
    for i, trail in enumerate(list(db.list_collection_names())):
        df1 = (pd.DataFrame(list(db[list(db.list_collection_names())[i]].find({}, {'_id':False, 'ratings':True, 'dates':True, 'highlights':True, 'review_text':True})))).iloc[1:,:]
        df = pd.concat([df, df1])


def plot_star_rates(df):
    '''Plotting historgram of star-rates'''
    total_reviews = df['ratings'].count()

    fig, ax = plt.subplots(figsize=(10,5))
    ax.hist(df[df['ratings'] == '1 Star']['ratings'], label=df[df['ratings'] == '1 Star']['ratings'].count(), bins=1, rwidth=.8)
    ax.hist(df[df['ratings'] == '2 Stars']['ratings'], label=df[df['ratings'] == '2 Stars']['ratings'].count(), bins=1, rwidth=.8)
    ax.hist(df[df['ratings'] == '3 Stars']['ratings'], label=df[df['ratings'] == '3 Stars']['ratings'].count(), bins=1, rwidth=.8)
    ax.hist(df[df['ratings'] == '4 Stars']['ratings'], label=df[df['ratings'] == '4 Stars']['ratings'].count(), bins=1, rwidth=.8)
    ax.hist(df[df['ratings'] == '5 Stars']['ratings'], label=df[df['ratings'] == '5 Stars']['ratings'].count(), bins=1, rwidth=.8)
    ax.set_title(f'Distribution of ~{round(total_reviews-300,-2)} reviews')
    ax.set_yscale('log')
    # _ = ax.legend()
    

def plot_percent_comments_left(df):
    '''Plotting percent of reviews left per star rating'''
    # calculating percent of reviews left per star rating
    one = df[df['ratings'] == '1 Star']['review_text'].count() / df[df['ratings'] == '1 Star']['ratings'].count()
    two = df[df['ratings'] == '2 Stars']['review_text'].count() / df[df['ratings'] == '2 Stars']['ratings'].count()
    three = df[df['ratings'] == '3 Stars']['review_text'].count() / df[df['ratings'] == '3 Stars']['ratings'].count()
    four = df[df['ratings'] == '4 Stars']['review_text'].count() / df[df['ratings'] == '4 Stars']['ratings'].count()
    five = df[df['ratings'] == '5 Stars']['review_text'].count() / df[df['ratings'] == '5 Stars']['ratings'].count()

    # gathering data for bar plot
    df[df['ratings'] == '1 Star']['review_text'].count(), df[df['ratings'] == '1 Star']['ratings'].count()
    df_ = pd.DataFrame(
        {'stars': ['1 Star','2 Stars','3 Stars','4 Stars','5 Stars'], '% comments': [one, two, three, four, five]})

    # plotting bar plot
    x = np.arange(1,6)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(x, df_['% comments'], color=('dodgerblue', 'orangered', 'goldenrod', 'green', 'grey'))
    ax.set_xticks(x)
    ax.set_xticklabels(df_['stars'])
    ax.set_ylabel('% comments')
    _ = ax.set_title(f'% Comments Left by Reviewers')
    # _ = ax.legend()

three_star_reviews = df[df['ratings'] == '3 Stars']['review_text'].count() # num of written reviews left by five-star reviewers
three_star_ratings = df[df['ratings']=='3 Stars']['ratings'].count() # num of five-star reviewers
four_star_reviews = df[df['ratings'] == '4 Stars']['review_text'].count() # num of written reviews left by four-star reviewers
four_star_ratings = df[df['ratings']=='4 Stars']['ratings'].count() # num of four-star reviewers
five_star_reviews = df[df['ratings'] == '5 Stars']['review_text'].count() # num of written reviews left by five-star reviewers
five_star_ratings = df[df['ratings']=='5 Stars']['ratings'].count() # num of five-star reviewers

three_stars_distribution = (([0] * (three_star_ratings - three_star_reviews)) + ([1] * three_star_reviews))
four_stars_distribution = ([0] * (four_star_ratings - four_star_reviews)) + ([1] * four_star_reviews)
five_stars_distribution = (([0] * (five_star_ratings - five_star_reviews)) + ([1] * five_star_reviews))

table = pd.DataFrame({'Written Reviews': [four_star_reviews, five_star_reviews], 'Total Reviewers': [four_star_ratings, five_star_ratings]}, index = ['4 Stars', '5 Stars']).T
table = table.style.set_properties(**{'text-align': 'center'})
table

four_v_five = scs.ttest_ind(four_stars_distribution, five_stars_distribution , equal_var= False)
three_v_four = scs.ttest_ind(three_stars_distribution, four_stars_distribution , equal_var= False)
three_v_five = scs.ttest_ind(three_stars_distribution, five_stars_distribution , equal_var= False)

if four_v_five[1] < 0.017:
    print('Rejcet H0')
else:
    print('Fail to reject H0')

if three_v_four[1] < 0.017:
    print('Rejcet H0')
else:
    print('Fail to reject H0')

if three_v_five[1] < 0.017:
    print('Rejcet H0')
else:
    print('Fail to reject H0')
