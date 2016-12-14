'''
File: scrape_reddit.py
Purpose: CS 505 Final Project | Measuring Team Performance
Authors: Benjamin Owens, Jennifer Tsui
Last modification: December 14, 2016

Description:
This is a script that processes the baseball data and bins
it into a timeseries. See report for more details.

'''



import praw
import pandas as pd
import numpy as np
import time
import datetime
import itertools as it
import matplotlib.pyplot as plt

teams = ['ANA', 'ARI', 'ATL', 'BAL', 'BOS', 'CWS', 'CHC', 'CIN', 'CLE', 'COL', 'DET', 'HOU', 'KCR', 'LAD', 'MIA', 'MIL', 'MIN', 'NYY', 'NYM', 'OAK', 'PHI', 'PIT', 'SDP', 'SEA', 'SFG', 'SLC', 'TBR', 'TEX', 'TOR', 'WAS']


def winners(filename):
    '''Parse baseball data and determine the winner of each game'''

    df = pd.read_csv(filename)
    winners = []
    dates = []
    for line in df.iterrows():
        date = line[1]['yyyymmdd']
        date = pd.to_datetime(date, format='%Y%m%d')
        dates.append(date)
        visiting = line[1]['visiting Team']
        home = line[1]['home team']
        visiting_score = line[1][' Visiting team score']
        home_score = line[1]['home team score']
        if visiting_score > home_score:
            winner = visiting
        elif visiting_score < home_score:
            winner = home
        elif visiting_score == home_score:
            winner = 'tie'
        else:
            winner = 'err'
        # print(winner)
        winners.append(winner)
    date_series = pd.DataFrame(pd.Series(dates))
    df['yyyymmdd'] = date_series
    winners_series = pd.Series(winners)
    winners_series = pd.DataFrame(winners_series, columns=['winner'])
    df = df.join(winners_series)
    return df


def bin_winners(df, filename):
    '''Create a dataframe of the count of wins per week, per team'''
    # Initializations
    first_date = df.iloc[0]['yyyymmdd']
    last_date = df.iloc[-1]['yyyymmdd']
    week_delta = datetime.timedelta(days=7)
    day_delta = datetime.timedelta(days=1)
    week_starts = [first_date]

    # Create keys as the first day of every week

    while (week_starts[-1] < last_date):
        week_starts.append(week_starts[-1] + week_delta)
    week_dict = {key: None for key in week_starts}

    # Count wins per week per team

    for week in week_dict.keys():
        week_performance = {}
        for i in range(0, 7):
            date = week + (day_delta * i)
            for game in df.loc[df['yyyymmdd'] == date].iterrows():
                if game[1]['winner'] in week_performance.keys():
                    week_performance[game[1]['winner']] += 1
                else:
                    week_performance[game[1]['winner']] = 1
        week_dict[week] = week_performance

    # Convert dict to pandas

    results = pd.DataFrame(week_dict).fillna(value=0).astype(int)
    results.index = teams
    results.to_csv(filename)
    #print(results.index.tolist())

    print(results)
    return results




# Run functions on 2015 data
df = winners('data/baseball_data_2015.csv')
result = bin_winners(df, 'data/team_stats_2015.csv')


columns = result.iloc[0].index.values
num_plots = int(input("Enter the number of team's plots: "))
for i in range(0,num_plots):
    plt.plot(columns,result.iloc[i],markersize=25.0)
axes = plt.gca()
plt.legend(teams[:num_plots])
axes.set_ylim([0,7])
plt.show()
