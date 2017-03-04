# Baseball Discussion on Reddit

### Benjamin Owens @bsowens
### Jennifer Tsui @j-tsui

# Intro:

Often times sports have the side effect of bonding together the fans of each team. Perhaps it is the case that a very lonely person is looking to find their niche in the form of a baseball team to be a fan of. Our data would help this person find the most loyal fanbases, so they can make some new friends and bond over their newfound passion of baseball! We wanted to explore the idea of loyal or disloyal fanbases by comparing time series that detail reddit posting frequency (for each team) and win data for each team.

# Datasets

Both datasets sampled on a weekly basis.
##⚾ Reddit Data
###⚾ Scraped from subreddit /r/baseball month by month

using the Python package PRAW, which stands for
Python Reddit API Wrapper
### ⚾ We then filtered the data by only considered posts
that included the team name, city, or their stadium name. Frequency of Reddit posts were scaled by the score, which is a value that Reddit gives to posts based on the number of upvotes and downvotes. After that, we just added the scaled frequencies for each week.
###⚾ We took the log of each post’s score, then the sum of those scores for every week:
weekly-score = sum ( log ( score[post 0: post n]))
##⚾ Team Win Data
⚾ We took the dataset from Retrosheet 2015 game log,
which was given as a CSV in order to get more information on how each team performed during the year.
⚾ From the original data, we kept yyyymmdd, Visiting Team, Visiting League, Home Team, Home League, Visiting Team Score, and Home Team Score


# Technique
We used the resulting filtered data to create two time series for each team
####⚾ Time Series 1: Reddit Posting Frequency for the team 
####⚾ Time Series 2: Wins (summed up over time, weekly) 
Ultimately we decided to compare these two time series for each team by calculating the Pearson Correlation Coefficient using the built function corrcoef in the Numpy package. We assume that a high negative correlation would indicate that a team’s fans are loyal, since the frequency at which the fans are talking is not really affected by their performance — they’re always excited to talk about their teams. By the same token, we assume that a high positive correlation would indicate that a team’s fanbase is not the most loyal in that the rate of talking seems very much related to the teams performance during the season.
We did try to compare the two time series by taking the cross-correlation, which is a measure of similarity between two series as a function of the displacement of one relative to the other. It is often used for signal processing. We tried this because it’s a common way to analyze time series, but ultimately didn’t stick with it because we don’t care about displacement for our time series.

#Conclusions
After looking at the resulting data and visualizations, we were not able to definitively conclude anything about the loyalty of each team’s fan base. We obviously oversimplified the complexity of fan loyalty by only looking at a small subset of fans. However, we can confidently claim the following:
###⚾ Teams like the Phillies (PHI) and Cardinals (CWS) tend to have more loyal fanbases. On the other hand, teams such as the Diamondbacks (ARI) and Padres (SDP) seem to only be discussed during win streaks. Remarkably, we found these results to be consistent with the 2015 Brand Keys Sports Fan LoyaltyTM survey.
###⚾ Baseball fans love to talk about the St. Louis Cardinals no matter what, especially when they are eliminated from the world series.
###⚾ The global average of correlation coefficients was found to be slightly positive. We can therefore claim that, in general, baseball fans tend to talk more about teams that are performing well.

##See the full report here:


##https://github.com/bsowens/Baseball_Discussion_on_Reddit/blob/master/report.pdf

## Workflow

1) `scrape_reddit.py` (warning: takes awhile to run!)
 * Writes: `data.csv`
 
2) `sort_reddit.py`

 * Reads: `data.csv` (turns into df, performs work)
 * Writes: `posts_with_mentions.csv`, `reddit_stats_2015.csv` (which was converted to a CSV from a df), 
 
3) `baseball_stats.py`
 * Reads: `baseball_data_2015.csv` (turns into df, performs work)
 * Writes: `team_stats_2015.csv` (which was converted to a CSV from a df)
 
4) `Correlations.py`
 * Reads: `team_stats_2015.csv`, `reddit_stats_2015.csv`
 * Writes: `cross_corr.csv`, `reg_corr.csv` (where `reg_corr.csv` contains the Pearson Correlation Coefficients)
