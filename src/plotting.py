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
