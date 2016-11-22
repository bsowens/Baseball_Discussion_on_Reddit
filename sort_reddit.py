

import pandas as pd
import datetime
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt


# some preprocessing to filter out posts that dont mention a team or city
teams = ['Arizona',
 'Diamondbacks',
 'Atlanta',
 'Braves',
 'Baltimore',
 'Orioles',
 'Boston',
 'Red',
 'Sox',
 'Chicago',
 'Cubs',
 'Chicago',
 'White',
 'Sox',
 'Cincinnati',
 'Reds',
 'Cleveland',
 'Indians',
 'Colorado',
 'Rockies',
 'Detroit',
 'Tigers',
 'Miami',
 'Marlins',
 'Houston',
 'Astros',
 'Kansas',
 'City',
 'Royals',
 'Los',
 'Angeles',
 'Angels',
 'Anaheim',
 'Los',
 'Angeles',
 'Dodgers',
 'Milwaukee',
 'Brewers',
 'Minnesota',
 'Twins',
 'New',
 'York',
 'Mets',
 'New',
 'York',
 'Yankees',
 'Oakland',
 'Athletics',
 'Philadelphia',
 'Phillies',
 'Pittsburgh',
 'Pirates',
 'Saint',
 'Louis',
 'Cardinals',
 'San',
 'Diego',
 'Padres',
 'San',
 'Francisco',
 'Giants',
 'Seattle',
 'Mariners',
 'Tampa',
 'Bay',
 'Rays',
 'Texas',
 'Rangers',
 'Toronto',
 'Blue',
 'Jays',
 'Washington',
 'Nationals']
df = pd.read_csv('data.csv')
filtered = df[df['Title'].str.split().apply(lambda x: len(set(x).intersection(set(teams))))>0]
filtered.to_csv("posts_with_mentions.csv")
print("Done writing 'posts_with_mentions.csv'")

#EOF


# TODO: count the mention of each team
df = pd.read_csv('posts_with_mentions.csv')
df = df.drop("Unnamed: 0",1)
teams = ['ANA', 'ARI', 'ATL', 'BAL', 'BOS', 'CWS', 'CHC', 'CIN', 'CLE', 'COL', 'DET', 'HOU', 'KCR', 'LAD', 'MIA', 'MIL', 'MIN', 'NYY', 'NYM', 'OAK', 'PHI', 'PIT', 'SDP', 'SEA', 'SFG', 'SLC', 'TBR', 'TEX', 'TOR', 'WAS']
teamDict = dict.fromkeys(teams)
zeroes = pd.DataFrame(0,columns=teams,index=df.index)
df = df.join(zeroes)

teamDict = {'ANA':["Anaheim","Angels",],
 'ARI':["Arizona",'ARI','Diamondbacks','Chase Field'],
 'ATL':["Atlanta",'ATL','Braves','Suntrust Park'],
 'BAL':["Baltimore","Orioles",' BAL ','Camden Yards'],
 'BOS':["Boston","Red","Red Sox",'BOS','Fenway','boston'],
 'CWS':['White Sox','Guaranteed Rate'],
 'CHC':["Cubs","Wrigley"],
 'CIN':["Cincinatti",'Reds','Great American'],
 'CLE':["Cleveland","Indians",'Progressive'],
 'COL':["Colorado",'Rockies',"Coors"],
 'DET':["Detriot","Tigers",'comerica'],
 'HOU':["Houston","Astros",'minute maid'],
 'KCR':["Kansas","Kansas City","Royals","KC",'kauffman'],
 'LAD':["Angeles","LA ", "Dodgers"],
 'MIA':["Miami",'Marlins'],
 'MIL':["Milwaukee","Brewers","Miller Park"],
 'MIN':["Minnesota","Twins","Target Field"],
 'NYY':["Yankees","Yankee","Bronx"],
 'NYM':["Mets","Citi","Queens"],
 'OAK':['Athletics','Coliseum'],
 'PHI':["Pittsburg","Pirates","PNC"],
 'PIT':["Philadelphia","Phillies"],
 'SDP':["Diego","Padres","Petco"],
 'SEA':["Seattle","Mariners","Safeco"],
 'SFG':["Francisco","giants"],
 'SLC':["St","Louis","Saint","Cardinals","Busch"],
 'TBR':["Tampa","Rays","Tropicana"],
 'TEX':["Texas","Rangers","Globe Life","Arlington"],
 'TOR':["Toronto","Blue Jays","Jays","rogers centre"],
 'WAS':["Washington","Nationals"]}


# Initialize date variables
first_date = pd.to_datetime(df.iloc[0]['Date'])
last_date = pd.to_datetime(df.iloc[-1]['Date'])
week_delta = datetime.timedelta(days=7)
day_delta = datetime.timedelta(days=1)
hour_delta = datetime.timedelta(hours=1)
week_starts = [first_date]

# Create keys as the first day of every week
week_starts[-1] = pd.to_datetime(week_starts[-1])
# Create an array of all of the first days of the weeks
while(week_starts[-1] < last_date):
    week_starts.append(week_starts[-1] + week_delta)
# create a dictionary from the array
week_dict = {key: None for key in week_starts}

# Remove DST
df['Date'] = df['Date'].apply(lambda date: pd.datetime.strptime(date,"%Y-%m-%d %H:%M:%S").replace(hour=0))

# Count mentions by week
for week in week_dict.keys():
    # print(week)
    week_performance = dict.fromkeys(teams)
    week = pd.to_datetime(week)
    # For every day this week
    for i in range(0, 7):
        date = week + (day_delta * i)
        date = date.replace(hour=0)
        # print(date)
        date_with_dst = [str(date), str(date + hour_delta)]
        # print(date)
        # For every post on this day

        for post in df.loc[df['Date'] == date].iterrows():
            # print(post[1]['Title'])
            # For every team
            for team in teamDict.keys():
                # Initialize dict values to an int
                if week_performance[str(team)] == None:
                    week_performance[str(team)] = 0
                # print(team)
                # Set is team in flag
                is_team_in = False
                # for every word associated with that team
                for word in teamDict[team]:
                    # print(word)
                    # if that word is in the post title
                    if word in post[1]['Title']:
                        # set the flag to true and stop checking
                        is_team_in = True
                        break

                if is_team_in == True:
                    # print("Found: " + team)
                    # DEPRECIATED: here is where we "weight" posts. Higher scored posts get more weight
                    # CURRENT: what we do here is simple add the post scores
                    if post[1]['Score'] > 2000:
                        week_performance[str(team)] += 20
                    elif post[1]['Score'] > 1000:
                        week_performance[str(team)] += 10
                    elif post[1]['Score'] > 100:
                        week_performance[str(team)] += 5
                    elif post[1]['Score'] > 10:
                        week_performance[str(team)] += 2
                    else:
                        week_performance[str(team)] += 1
                    # post[1]['Score']

    week_dict[week] = week_performance

# Convert dict to pandas

results = pd.DataFrame(week_dict)
results.to_csv("reddit_stats.csv")
print(results)
#df_1_columns = list(results.columns.values)
#df_1 = results[df_1_columns]
#df_1

bar_1 = plt.bar()

plt.show()

