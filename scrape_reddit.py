'''
File: scrape_reddit.py
Purpose: CS 505 Final Project | Scraping reddit.com/r/baseball posts
Authors: Benjamin Owens, Jennifer Tsui
Last modification: December 14, 2016

Description:
This is a script that allows one to collect reddit posts from a subreddit (in this case, /r/baseball).
The script allows the user to collect data from any time period, specified by the user input. 

For the purposes of this assignment, we collected posts from the most recent full year (2015). The .csv
file derived from the full execution is included in the repository (data.csv), as well as the filtered data
that includes only posts including the mentions of teams and cities (posts_with_mentions.csv). 
The filtering component of the script is not finalized, but the methodology is sound 
(we'll need to include abbreviations, nicknames, common typos, etc. in the future). 


###### WARNING ######
This web scraper takes A LONG TIME to collect even a few days worth of data. Don't attempt to run it,
just use the data included in the /data/ directory.

The runtime is on the order of 5-10 seconds per day, depending on the activity (number of posts).


'''

import praw
import pandas as pd
import time
import datetime


print("Enter date to start checking:\n (default 01/01/2015)")
print("")
start = ''
start = input("User input: ")
if start == '':
    start = "01/01/2015"

startStamp = int(time.mktime(datetime.datetime.strptime(start, "%m/%d/%Y").timetuple()))
print("Enter number of days to check: [>2] \n(Default 30)")
numDays = 0
numDays = input("User input: ")
if numDays == 0:
    numDays = "30"
days = [(int(startStamp)+ (86400*i)) for i in range(0,int(numDays))]

print("Requesting Data ")
r = praw.Reddit(user_agent='ben_and_jens_505_project')

'''
Here we use a helper function from the PRAW library that allows us to get the posts within a certain timestamp.
It seems to be asynchronous which is a little strange but it works!
'''
submissionList = []
# Get the first day's data
print("Checking day: " + str(datetime.datetime.fromtimestamp(int(days[0]))))
submission = praw.helpers.submissions_between(r,r.get_subreddit('baseball'),
                                                lowest_timestamp=days[0],highest_timestamp=days[1])


thelist = [str(x).split('::') + [str(datetime.datetime.fromtimestamp(int(days[0])))] for x in submission]
submissionList += thelist
# get the rest of the days' data
for i in range(1,len(days[1:])):
    print("Checking day: " + str(datetime.datetime.fromtimestamp(int(days[i]))))
    submission = praw.helpers.submissions_between(r,r.get_subreddit('baseball'),
                                                    lowest_timestamp=days[i],highest_timestamp=days[i+1],
                                                    verbosity=1)

    #split the string returned and add the date to every row
    thelist = [str(x).split('::') + [str(datetime.datetime.fromtimestamp(int(days[i])))] for x in submission]
    submissionList += thelist

scores = [x[0] for x in submissionList]
posts = [x[1] for x in submissionList]
dates = [x[2] for x in submissionList]
df = pd.DataFrame()
df["Score"] = scores
df["Title"] = posts
df["Date"] = dates

df.to_csv("data/data.csv")
print("Done writing 'data.csv'")

