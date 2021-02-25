**AllTrails.com**

When I browse on All Trails to find a hike in at Bear Mountain in NY, I find myself looking to pick one hike to do, and wanting to easily have accurate and good information that can inform me if I will enjoy a specific hike. Reading through dozens of comments left by reviewers is boring and takes time, especially if I need to look through up to 5 trails before I find one with which I am satisfied. I think that recent comments left in the past 2-3 years are the most relevant, and having a summary of them would make selecting a trail ideal.

alltrails.com/us has information on many hiking trails here in the United States. I appreciate reading comments left by reviewers as they help me determine if a specific hike is for me, as well as what considerations I should take into account, like whether it's well-marked or heavily-trafficked. Reviews with 5 stars and no comment always stand out to me: if one had a great time on the hike, wouldn't you write what you loved about it? Similarly, 4-star reviews also stand out to me: what brings someone to leave a good review, but not a great one? Taking this one step further: when a 4-star reviewer leaves a comment, is it because they have something negative to say _with_ comments also stand out to me: The broad question I'm intersted in for this project is what brings a 4-star reviewer to leave a great review but leave out one star? Can this be determined from the comments that they leave? I hypothesize that 4-star reviewers are more inclined to leave a review, specifically 

_My Process_
1. Create pipeline to get reviewer data for one trail. Took me many revisions to get pipeline to be efficient. It works like this:
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

![tech stack](https://github.com/sborodach/all-trails/blob/main/images/tech_stack.pdf)
