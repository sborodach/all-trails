**AllTrails.com**

### The story
alltrails.com/us provides information and user reviews on hikes in the U.S. I frequent this site as a recreational hiker and in scrolling through comments I notced that 5-star reviewers often leave no comment with their review. Similarly, 4-star reviewers seemed to leave reviews at least as often as 5-star reviewers, and I wondered if it might be that 4-star reviewers leave comments more often than 5-star reviewers..., and I think the answer why is fairly intuitive.

### Gathering the data
I built a web-scraper using selenium to click through a trail's webpage to display all the reviews, pyMongo to store the HTML, and BeautifulSoup to parse the data, extracting reviewer information. Here are images of the scraper in action:

### Some basic EDA
Next I 
2. Get data for three trails, each with at least 400 reviews:
    — 4 Stars: 47 / 206
    — 5 Stars: 75 / 361
3. H0: rates of comments left by 4 and 5 star reviewers is the same --> Welch's T-Test: Fail to reject H0.
4. So I thought maybe if I have larger sample sizes the data will tell me something more intersting. With larger sample sizes, (fill in what happened, reject or not). Yes! Reject H0
5. Went back and saved each trail stats to mongoDB so I could access it agaain later using to_pandas function in pyMongo.
6. What about 3 star reviewers?
7. Interstingly, for 5 different trails, each with at least 200 reviews, in each case the percentrage of 1 and 2 star reviews was less than _____ (fill in %_). I'm curious: how could I learn if there are more folks hiking these trails who whould leave a 1 or 2 stra review if they did leave a review?


 

**Further Study:**
    *  Use NLP to create summaries based on comments left by reviewers with 1-5 stars

![percent comments](https://github.com/sborodach/all-trails/blob/main/images/percent_comments.png)

![ratings distribution](https://github.com/sborodach/all-trails/blob/main/images/ratings_distribution.png)

![reject or fail to](https://github.com/sborodach/all-trails/blob/main/images/reject_or_fail_to.png)

![tech stack](https://github.com/sborodach/all-trails/blob/main/images/tech_stack.png)
