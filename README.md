# cap-stone-1
Galvanize DSI, Project 1

I enjoy hiking and do it maybee once a month. I find myself looking to pick one hike to do, and wanting to easily have accurate and good information that can inform me if I will enjoy a specific hike. Reading through dozens of comments left by reviewers is boring and takes time, especially if I need to look through up to 5 trails before I find one with which I am satisfied. I think that recent comments left in the past 2-3 years are the most relevant, and having a summary of them would make selecting a trail ideal.

The broad question I'm intersted in for this project is can it be inferred what brings reviewers to leave written comments based on their rating (stars 1-5)?

_My Process_
1. Create pipeline to get reviewer data for one trail.
2. Get data for three trails:
    — 4 Stars: 47 / 206
    — 5 Stars: 75 / 361
3. H0: rates of comments left by 4 and 5 star reviewers is the same --> Welch's T-Test: Fail to reject H0.
4. So I thought maybe if I have larger sample sizes the data will tell me something more intersting. With larger sample sizes, (fill in what happened, reject or not).
5. What about 3 star reviewers?
6. Interstingly, for 5 different trails, each with at least 200 reviews, in each case the percentrage of 1 and 2 star reviews was less than _____ (fill in %_). I'm curious: how could I learn if there are more folks hiking these trails who whould leave a 1 or 2 stra review if they did leave a review?


 

**Further Study:**
1. Refine pipeline to acquire hike reviewer data
2. Use NLP to create summaries based on comments left by reviewers with 1-5 stars
