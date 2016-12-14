'''
File: scrape_reddit.py
Purpose: CS 505 Final Project | Finding correlation of Reddit Posts and Team Performance
Authors: Benjamin Owens, Jennifer Tsui
Last modification: December 14, 2016

Description:
This is a script that finds the correlation between the frequency and score of /r/baseball
posts and MLB team performance. See report for more details.

'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from sklearn.metrics.pairwise import euclidean_distances



bdf = pd.read_csv('team_stats_2015.csv')
bdf = bdf.set_index('Unnamed: 0',drop=True)

bdf = bdf.dropna()
bdf_col = list(bdf.columns.values)

rdf = pd.read_csv('reddit_stats_2015.csv')

rdf = rdf.fillna(value=0)

rdf_col = list(rdf.columns.values)
intersection = list(set(rdf_col) & set(bdf_col))

bdf = bdf[intersection].transpose()
rdf = rdf[intersection].transpose()

teams = ['ANA', 'ARI', 'ATL', 'BAL', 'BOS', 'CWS', 'CHC', 'CIN', 'CLE', 'COL', 'DET', 'HOU', 'KCR', 'LAD', 'MIA', 'MIL', 'MIN', 'NYY', 'NYM', 'OAK', 'PHI', 'PIT', 'SDP', 'SEA', 'SFG', 'SLC', 'TBR', 'TEX', 'TOR', 'WAS']
rdf.columns = teams

cross_corr = {}
for i in teams:
    try:
        cross_corr[i] = np.correlate(bdf[i],  rdf[i]).tolist()[0]
    except:pass

reg_corr = {}
for i in teams:
    try:
        reg_corr[i] = np.corrcoef(bdf[i],  rdf[i]).tolist()[0][1]
    except:pass


for i in teams:
    try:
        print("Team: ", i, "Cross Correlation: ",cross_corr[i])
        print("Team: ", i, "Regular Correlation: ", reg_corr[i])
        print('')
    except:pass

plt.subplot(211)
plt.bar(range(len(cross_corr)), cross_corr.values(), align='center')
plt.xticks(range(len(cross_corr)), cross_corr.keys())


plt.subplot(212)
plt.bar(range(len(reg_corr)), reg_corr.values(), align='center')
plt.xticks(range(len(reg_corr)), reg_corr.keys())
plt.show()


with open('cross_corr.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in cross_corr.items():
       writer.writerow([key, value])


with open('reg_corr.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in reg_corr.items():
       writer.writerow([key, value])