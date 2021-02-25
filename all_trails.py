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


trails_urls = [] #urls for hike pages (e.g. https://www.alltrails.com/parks/us/new-york/bear-mountain-state-park?ref=result-card)
db_name = 'bearmountain' #mountain/park name to be saved in mongo
client = MongoClient()
db = client[db_name]

def get_trails_html(urls):
    '''Using selenium to get webpage html for trails on a specific mountain or in a '''
    for url in urls:
        driver = webdriver.Chrome()
        client = MongoClient()

        driver.get(url)
        sleep(3)

        driver.execute_script("window.scrollTo(0, 10000)")

        search = driver.find_element_by_css_selector("#reviews > div.styles-module__container___px-t2.xlate-none > button") # find 'show more reviews button'

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
        trail_name = "".join(((" ".join(((url.split('/'))[-1]).split('-'))).title()).split(" "))
        pages = db[trail_name]
        pages.insert_one({'link': url, 'html': html})
    

def get_reviewer_data(db):
    '''Use stored html text in mongo to create mongo collection of hiking trail reviewer data'''
    for i, trail in enumerate(list(db.list_collection_names())):
        df = pd.DataFrame(list(db[trail].find({})))
        soup = BeautifulSoup(df.iloc[i,2], 'html.parser')

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
            db.trail.insert_one(d)
            

'''Converting stored mongo collections into pandas dataframes'''
bear_mount = db.BearMountainLoopTrail
bear_mount_df = (pd.DataFrame(list(bear_mount.find({}, {'_id':False, 'ratings':True, 'dates':True, 'types':True, 'review_text':True})))).iloc[1:,:]

pop = db.PopolopenTorneLoop
pop_df = (pd.DataFrame(list(pop.find({}, {'_id':False, 'ratings':True, 'dates':True, 'types':True, 'review_text':True})))).iloc[1:,:]

dund = db.DunderbergBaldMountainAndTheTimpLoop
dund_df = (pd.DataFrame(list(dund.find({}, {'_id':False, 'ratings':True, 'dates':True, 'types':True, 'review_text':True})))).iloc[1:,:]

ttt = db.TimpTorneTrail
ttt_df = (pd.DataFrame(list(ttt.find({}, {'_id':False, 'ratings':True, 'dates':True, 'types':True, 'review_text':True})))).iloc[1:,:]

perkins = db.PerkinsMemorialTowerViaAppalachianTrail
perkins_df = (pd.DataFrame(list(perkins.find({}, {'_id':False, 'ratings':True, 'dates':True, 'types':True, 'review_text':True})))).iloc[1:,:]

doodle = db.DoodletownBridlePathLoopTrail
doodle_df = (pd.DataFrame(list(doodle.find({}, {'_id':False, 'ratings':True, 'dates':True, 'types':True, 'review_text':True})))).iloc[1:,:]

tt = db.TimpTrail
tt_df = (pd.DataFrame(list(tt.find({}, {'_id':False, 'ratings':True, 'dates':True, 'types':True, 'review_text':True})))).iloc[1:,:]

tttd = db.TimpTorneTrailAndDunderbergSpiralRailwayAndLoop
tttd_df = (pd.DataFrame(list(tttd.find({}, {'_id':False, 'ratings':True, 'dates':True, 'types':True, 'review_text':True})))).iloc[1:,:]

west_mount = db.WestMountainLoopTrail
west_mount_df = (pd.DataFrame(list(west_mount.find({}, {'_id':False, 'ratings':True, 'dates':True, 'types':True, 'review_text':True})))).iloc[1:,:]

bald_mount = db.BaldMountainLoop
bald_mount_df = (pd.DataFrame(list(bald_mount.find({}, {'_id':False, 'ratings':True, 'dates':True, 'types':True, 'review_text':True})))).iloc[1:,:]


'''Concatenating sub-dataframes to form one dataframe'''
df = pd.concat([bear_mount_df, pop_df, dund_df, ttt_df, perkins_df, doodle_df, tt_df, tttd_df, west_mount_df, bald_mount_df], ignore_index=True)


def hist_star_rates(df):
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
