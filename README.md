### Are some reviewers more likely to leave comments than others: <br/>    Comparing star rating reviews on AllTrails.com

### The story
alltrails.com/us provides information and user reviews on hikes in the U.S. I frequent this site as a recreational hiker and in scrolling through comments I noticed that 5-star reviewers often leave no comment with their review, which is noteworthy, though perhaps unsuprising, as these users had positive experiences and left no comment. Similarly, it seemed to me that 4-star reviewers tend to leave reviews at least as often as 5-star reviewers, and I wondered if it might be that 4-star reviewers leave comments more often than 5-star reviewers since they have some feedback regarding their experience, while 5-star reviewers only have positive remarks and so leave comments less often. This project is my first step in answering this question by grouping reviewers based on star number and comparing the rates of comments they leave.

### Gathering the data
I built a web-scraper using selenium to scroll through a trail's webpage and click through to display all hundreds or thousands of reviews, pyMongo to store the HTML, and BeautifulSoup to parse the HTML, extracting reviewer information. (Check out a gif of selenium in action at the end.)

### Some basic EDA
After converting the mongo collections into a pandas dataframe, I graphed these. The first is a distribution of reviewer ratings and the second the percent of reviews with comments grouped by star rating.

Distribution of Ratings |  Percentage Comments
:-------------------------:|:-------------------------:
![ratings distribution](https://github.com/sborodach/all-trails/blob/main/img/ratings_rates.png)  | ![percent comments](https://github.com/sborodach/all-trails/blob/main/img/percent_comments.png)

There are two things to notice here. First, 1 and 2 star reviewers are scarce, as is often the case with reviewers on passion sites (in conrast to, say, retail—like Amazon). Since More importantly for the question at hand: the 5-star comment percentage is lower than both 3 and 4 stars. From this we can already assume it is somewhat likely that comments are left less frequently by 5-star reviewers.

### Comparing 3, 4, and 5 stars
The null hypothesis for each test is nearly the same: comments are left at an equal rate between two of the three star groups, and the alternative hypothesis suggests there is some difference. Accounting for the Bonferroni Correction, I set the significance level at .017 and calculated the p-values for each comparison using a Welch's T-Test. Here are the results:

<img align="right" width="400" height="400" src="https://github.com/sborodach/all-trails/blob/main/img/reject_or_not.png">
<br/><br/><br/><br/><br/>
We can see that only the p-value for 4/5 star comparisons is below the significance level, while the 3/4 and 3/5 comparison is above. Thus, there is sufficient evidence to suggest that 5 star reviewers leave comments at a different rate than only 4 star reviewers, while evidence is lacking that 3 star reviewers differ from both 4 and 5 star reviewers.
<br/><br/><br/><br/><br/><br/><br/>

### Further Study
After learning NLP, I would like to create summaries based on comments left by reviewers in each of the 5 star raating categories. I am most curious to learn if 4-star reviewers leave comments than their 5-star counterparts since they have some negative feedback or constructive criticsm to share in their reviews.
<br/>

### Thank you
to Juliana Duncan, Dan Rupp, and Kiara Hearn for their guidance and insight throughout this project.

![tech stack](https://github.com/sborodach/all-trails/blob/main/img/tech-stack.png)

![selenium](https://github.com/sborodach/all-trails/blob/main/img/selenium.gif)
