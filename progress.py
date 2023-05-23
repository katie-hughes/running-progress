import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import argparse
import numpy as np
import pandas as pd
from datetime import date



parser = argparse.ArgumentParser(description='Solve a sudoku! :D')
parser.add_argument('-a', '--add', action='store_true', help='Add a new run!')
args = parser.parse_args()

start_date = date(2022, 12, 31)
todays_date = date.today()
ndays = (todays_date - start_date).days

df = pd.DataFrame({'day': [], 'miles': [], 'times': [], 'average': [], 'fastest': [], 'slowest': []})

# parse file

def convert_miletime(str):
    mile_time_spl = str.split(':')
    minutes = int(mile_time_spl[0])
    seconds = int(mile_time_spl[1])
    pace_in_seconds = minutes*60 + seconds
    return pace_in_seconds

with open('progress.txt') as f:
    for l in f.readlines():
        spl = l.split()
        day = int(spl[0])
        dist = int(spl[1])

        day_pacing = []
        for i in range(dist):
            try:
                # print(f"Minutes: {minutes}, seconds: {seconds}, total {pace_in_seconds}")
                day_pacing.append(convert_miletime(spl[i+2]))
            except:
                pass
        
        while(day - 1 != len(df.index)):
            df.loc[len(df.index)] = np.array([len(df.index)+1, 0, [], np.nan, np.nan, np.nan],dtype=object)
            # df = df.append({'day':len(df.index)+1, 'miles':0}, ignore_index=True) 
        
        # put this when day - 1 == index
        df.loc[len(df.index)] = np.array([day, dist, day_pacing, np.mean(day_pacing), np.min(day_pacing), np.max(day_pacing)],dtype=object)


while(ndays > len(df.index)):
    df.loc[len(df.index)] = np.array([len(df.index)+1, 0, [], np.nan, np.nan, np.nan],dtype=object)

df[["day", "miles", "average", "fastest", "slowest"]] = df[["day", "miles", "average", "fastest", "slowest"]].apply(pd.to_numeric)



if args.add is True:
    print("Add a new run!")
    while True:
        try:
            day_add = input(f"What day is this for? (Today is {ndays}): ")
            day_add = int(day_add)
            print(f"You selected: {day_add}")
            miles_add = input("How many miles? ")
            miles_add = int(miles_add)
            print(f"You ran {miles_add}")
            miletimes_add = []
            for i in range(miles_add):
                miletime_add = input(f"Mile {i+1} time (mm:ss): ")
                miletime_add = convert_miletime(miletime_add)
                miletimes_add.append(miletime_add)
            break
        except:
            print("Invalid input, try again!")

df['cumulative_miles'] = df['miles'].cumsum()


df['difference'] = df['day'] - df['cumulative_miles']

for label in ['average', 'fastest', 'slowest']:
    df[label+'_mins'] = df[label]/60.0


print(f"Days of 2023:\t{ndays}")
print(f"Current Miles:\t{np.max(df['cumulative_miles'])}")



maximum = max(np.max(df['day']), np.max(df['cumulative_miles']))

# Plot Cumulative Miles

plot_cumulative = True

if plot_cumulative:
    plt.plot((1,maximum),(1, maximum), color='b', label='Goal')
    plt.plot(df['day'], df['cumulative_miles'], color='k', label='Cumulative Miles')
    plt.xlabel('Days of 2023')
    plt.ylabel('# Miles')
    plt.legend()
    plt.title("Cumulative Miles Ran")
    plt.savefig('cumulative-miles')
    plt.close()

# Plot difference from ideal

def colormap_difference(diff):
    # I want a way of doing this that is continuous
    
    def help(d):
        if d <= 0:
            return 'green'
        elif d > 30:
            return 'maroon'
        elif d > 20:
            return 'red'
        elif d > 10: 
            return 'orange'
        elif d > 0:
            return 'gold'
    return [help(d) for d in diff]

plot_difference = True

df_nonzero = df[df["miles"] != 0]
df_zero = df[df["miles"] == 0]



cdict = {'red':   [(0.0,  0.0, 0.0),
                       (0.5,  1.0, 1.0),
                       (1.0,  1.0, 1.0)],

             'green': [(0.0,  0.0, 0.0),
                       (0.25, 0.0, 0.0),
                       (0.75, 1.0, 1.0),
                       (1.0,  1.0, 1.0)],

             'blue':  [(0.0,  0.0, 0.0),
                       (0.5,  0.0, 0.0),
                       (1.0,  1.0, 1.0)]}
my_colormap = mplc.LinearSegmentedColormap('my_colormap',cdict,256)
# print(my_colormap)

if plot_difference:
    diff = []
    plt.axhline(10, color='gray', alpha=0.2)
    plt.axhline(20, color='gray', alpha=0.2)
    plt.axhline(30, color='gray', alpha=0.2)
    plt.bar(df_nonzero['day'], df_nonzero['difference'], color=colormap_difference(df_nonzero['difference']))
    plt.bar(df_zero['day'], df_zero['difference'], color=colormap_difference(df_zero['difference']), alpha=0.25)
    plt.axhline(0, color='b', label='Goal\nWorst: '+str(max(df['difference']))+' behind\nBest: '
                                                   +str(abs(min(df['difference'])))+' ahead')
    plt.xlabel('Days of 2023')
    plt.ylabel('# Miles Away from Goal')
    plt.legend(loc='upper left')
    plt.title("Distance from Goal Mileage")
    plt.savefig('delta-miles')
    plt.close()

# Plot Average Pace

def pacing_lines():
    for i in range(7, 12):
        plt.axhline(i,  color='gray', alpha=0.3)

def colormap(pace):
    # range from (1,0,0) to (0,1,0)
    # max: 12 min: 6
    # 6 -> 0 -> (0,0,1) (blue)
    # 12 -> 1 -> (1,0,0) (red)
    fastest = 7
    slowest = 12
    scaled = (np.array(pace) - fastest)/(slowest-fastest)
    # print(scaled)
    red = scaled
    blue = 1 - red
    return [(red[i], 0, blue[i]) for i in range(len(scaled))]


plot_pacing = True

if plot_pacing:

    for label in ['average', 'fastest', 'slowest']:
        pacing_lines()
        plt.bar(df['day'], df[label+'_mins'], color=colormap(df[label+'_mins']))
        plt.ylim(bottom=6.0)
        plt.xlabel('Days of 2023')
        plt.ylabel(label.capitalize()+' Pace (mins/mile)')
        plt.title(label.capitalize()+" Pacing")
        plt.savefig(label+"-pacing")
        plt.close()