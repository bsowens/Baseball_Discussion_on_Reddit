# cs505-final-project

##Proposal
####Topic: Baseball Discussion on Reddit
####Authors: Benjamin Owens [(bsowens)](https://github.com/bsowens) & Jennifer Tsui [(j-tsui)](https://github.com/j-tsui)


####1) Discuss the dataset and their nature. How you got them, how they have been collected, what are their main characteristics, if you need to pre-process them, etc.


We will be analyzing 2 datasets:

* [www.reddit.com/r/baseball](https://www.reddit.com/r/baseball/) (posts and comments)
 * We will be using the Reddit API to retrieve data from the /r/baseball subreddit. We plan to perform semantic analysis to quantify popularity of teams based on quantity and frequency of mentions and discussion.
 
* [ESPN](www.espn.com/static/apis/devcenter/docs/scores.html) OR [Retrosheet 2015 game log](http://www.retrosheet.org/gamelogs/index.html) 
 * We may either use the ESPN API or the gamelogs dataset from 2015 (which is a CSV) in order to get more information on how each team performed during the year. For example, we would retrieve the number of losses and wins for a team, when these losses and wins happened, as well as post-season performance, where teams are either eliminated or advance to the next series.
 * Note (11/11/16): We discovered we could not access the ESPN API anymore, thus we decided to use the Retrosheet game log. That dataset did not contain any information on post-season performance, so we only kept the data pertaining to which teams were playing and who won or lost.
 
* If we have time: [Sentiment Labelled Sentences Data Set ](https://archive.ics.uci.edu/ml/datasets/Sentiment+Labelled+Sentences)
 * If we want to delve further into the discussion of teams on subreddits, we might use this very unique dataset, which provides the tools to classify sentences based on a positive or negative sentiment.


####2) Expected analysis on the dataset. What kind of techniques you plan to use.


In order to retrieve the data, we plan to use web scraping and `HTTP GET` request techniques we learned in this course.


We plan to place more emphasis on posts with high scores vs posts with low scores. To reduce noise, we will most likely drop posts with a very low score, as they have low visibility and relevance. On the other hand, posts with very high scores will be weighted more heavily than posts with low, but not negligible scores.


We hope to discover a correlation between teams’ performance in the regular/post-season and its popularity on the /r/baseball subreddit. From there, we want to glean some idea of whether the teams fanbases are loyal or not.


To visualize the data, we plan to represent the wins and losses in at least two ways. The first way would be a scatter plot, where wins and losses are plotted on the x and y axis, respectively. The second way would incorporate some measurement of time (maybe a timeseries of a ratio between wins and losses). We would document Reddit activity by comparing mentions of each team over time.


####3) Application.


Often times sports have the side effect of bonding together the fans of each team. Perhaps it’s the case that a very lonely person is looking to find their niche in the form of a baseball team to be a fan of. Our data would help this person find the most loyal fanbases, so they can make some new friends and bond over their newfound passion of baseball! On the other hand, locating a very loyal fanbase may help with classifying the general sentiment of the fanbase, and why they may be seen as negative or positive. This may sound farfetched, but in actuality the study of sports fans lays at the intersections of various disciplines including psychology, sociology, and physiology. If you’re curious about it, please see the included links.


* [The Psychology Of Social Sports Fans: What Makes Them So Crazy?](http://www.sportsnetworker.com/2012/02/15/the-psychology-of-sports-fans-what-makes-them-so-crazy/)
* [The psychology of being a sports fan](http://www.seattletimes.com/sports/the-psychology-of-being-a-sports-fan/)
* [Fan Loyalty](https://en.wikipedia.org/wiki/Fan_loyalty)

####4) Expected results.


Our hypothesis is that teams will, in general, become more popular if they perform well, and less popular if they perform poorly. With this correlation in mind, we hope to find that some teams have more loyal fanbases than other, when their popularity remains high despite poor performance, and that some teams are only popular when they are performing well.



##Files

###scrape_reddit.ipynb
####Purpose: CS 505 Final Project | Scraping reddit.com/r/baseball posts
####Last modification: November 11, 2016

Description:
This is a script that allows one to collect reddit posts from a subreddit (in this case, /r/baseball).
The script allows the user to collect data from any time period, specified by the user input. 

For the purposes of this assignment, we collected posts from the most recent full year (2015). The `.csv`
file derived from the full execution is included in the repository `data.csv`, as well as the filtered data
that includes only posts including the mentions of teams and cities (`posts_with_mentions.csv`). 
The filtering component of the script is not finalized, but the methodology is sound 
(we'll need to include abbreviations, nicknames, common typos, etc. in the future). 

The runtime is on the order of 5-10 seconds / day, depending of the activity (number of posts). 

###baseball_data.csv
####Last modification: November 10, 2016

Description:
This file contains information about which teams faced each other, and the scores for each respective teams. 
Rows take on the form of [date, visiting team, visiting league, home team, home league, visiting team score, home score. ]

