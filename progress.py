import matplotlib.pyplot as plt
import matplotlib.cm as colormaps
import argparse
import numpy as np
import pandas as pd
from datetime import date
import calendar


# print(plt.style.available)
plt.style.use('dark_background')

year = 2023

def time_string(time_minutes):
    return f"{int(time_minutes // 1)}:{int((time_minutes % 1)*60):02d}"

def plot_months(current_days, y=0):
    total_days = 0
    for month in range(1,13):
        days_in_month = calendar.monthrange(year, month)[1]
        # print(days_in_month)
        plt.axvline(total_days, color='gray', alpha=0.1)
        plt.text(total_days, y, calendar.month_name[month][:3], rotation=90, verticalalignment='center', color='gray', alpha=0.8)
        total_days += days_in_month
        if total_days > current_days:
            return

parser = argparse.ArgumentParser(description='Tracking Runs!')
parser.add_argument('-a', '--add', action='store_true', help='Add a new run!')
args = parser.parse_args()

start_date = date(2022, 12, 31)
todays_date = date.today()
ndays = (todays_date - start_date).days
ndays = min(ndays, 365)

fname = 'progress.txt'

images_path = 'plots/'

df = pd.DataFrame({'day': [], 'miles': [], 'times': [], 'times_str': [], 'average': [], 'fastest': [], 'slowest': []})

# parse file

def convert_miletime(str):
    mile_time_spl = str.split(':')
    minutes = int(mile_time_spl[0])
    seconds = int(mile_time_spl[1])
    pace_in_seconds = minutes*60 + seconds
    return pace_in_seconds

def scale(lst):
    return (lst-np.min(lst))/(np.max(lst)-np.min(lst))

with open(fname) as f:
    for l in f.readlines():
        spl = l.split()
        day = int(spl[0])
        dist = int(spl[1])

        day_pacing = []
        raw_times = []
        for i in range(dist):
            try:
                # print(f"Minutes: {minutes}, seconds: {seconds}, total {pace_in_seconds}")
                day_pacing.append(convert_miletime(spl[i+2]))
                raw_times.append(spl[i+2])
            except:
                pass
        
        while(day - 1 != len(df.index)):
            df.loc[len(df.index)] = np.array([len(df.index)+1, 0, [], [], np.nan, np.nan, np.nan],dtype=object)
            # df = df.append({'day':len(df.index)+1, 'miles':0}, ignore_index=True) 
        
        # put this when day - 1 == index
        df.loc[len(df.index)] = np.array([day, dist, day_pacing, raw_times, np.mean(day_pacing), np.min(day_pacing), np.max(day_pacing)],dtype=object)


while(ndays > len(df.index)):
    df.loc[len(df.index)] = np.array([len(df.index)+1, 0, [], [], np.nan, np.nan, np.nan],dtype=object)

df[["day", "miles", "average", "fastest", "slowest"]] = df[["day", "miles", "average", "fastest", "slowest"]].apply(pd.to_numeric)

if args.add is True:
    print("Add a new run!")
    while True:
        try:
            day_add = input(f"What day is this for? (Today is {ndays}): ")
            day_add = int(day_add)
            miles_add = input("How many miles? ")
            miles_add = int(miles_add)
            miletimes_add = []
            miletimes_add_str = []
            for i in range(miles_add):
                miletime_add = input(f"Mile {i+1} time (mm:ss): ")
                miletimes_add_str.append(miletime_add)
                miletime_add = convert_miletime(miletime_add)
                miletimes_add.append(miletime_add)
            input_string = str(day_add)+' '+str(miles_add)
            for i in miletimes_add_str:
                input_string+=' '+i
            print(f"Your input is:\n{input_string}")
            c = input("Press q to cancel this, and anything else to add! ")
            if c != 'q':
                print("Adding!")
                # don't add it if the date already exists in fname
            break
        except:
            print("Invalid input, try again!")

df['cumulative_miles'] = df['miles'].cumsum()
df['difference'] = df['day'] - df['cumulative_miles']

for label in ['average', 'fastest', 'slowest']:
    df[label+'_mins'] = df[label]/60.0

total_miles = np.max(df['cumulative_miles'])
todays_miles = df['miles'][ndays-1]
if (todays_miles > 0):
    print("Running 365 miles in 2023!")
    print()
    print(f"Day: {ndays}/365")
    print(f"Miles: {total_miles}/365")
    print()
    print(f"Today: {todays_miles} miles")
    for i,mile_time in enumerate(df['times_str'][ndays-1]):
        if i < todays_miles - 1:
            print(mile_time, end='/')
        else:
            print(mile_time)
else:
    print(f"Days of 2023:\t{ndays}")
    print(f"Current Miles:\t{total_miles}")

maximum = max(np.max(df['day']), np.max(df['cumulative_miles']))

# Plot Cumulative Miles

plot_cumulative = True

if plot_cumulative:
    plot_months(ndays, y=-12)
    plt.ylim(bottom=-30, top=maximum*1.1)
    plt.plot((1,maximum),(1, maximum), color='white', label=f'Goal ({ndays})')
    plt.plot(df['day'], df['cumulative_miles'], color='aqua', label=f'Cumulative Miles ({total_miles})')
    plt.xlabel('Days of 2023')
    plt.ylabel('# Miles')
    plt.legend(loc='upper left')
    plt.title("Cumulative Miles Ran")
    plt.savefig(images_path+'cumulative-miles')
    plt.close()

# Plot difference from ideal
plot_difference = True

df_nonzero = df[df["miles"] != 0]
df_zero = df[df["miles"] == 0]

if plot_difference:
    diff = []
    for i in range(0, 31, 10):
        plt.axhline(i, color='gray', alpha=0.1)
    cmap = colormaps.get_cmap('rainbow')
    colors = cmap(df['difference']/np.max(df['difference']))
    # transparency = [1 if nmiles >0 else 0.75 for nmiles in df['miles']]
    # for i in range(len(df['day'])):
    #     plt.bar(df['day'][i], df['difference'][i], width=1.0, color=colors[i],alpha=transparency[i])
    plt.bar(df['day'], df['difference'], width=1.0, color=colors)

    worst = max(df['difference'])
    worst_desc = 'behind' if worst > 0 else 'ahead'
    best = min(df['difference'])
    best_desc = 'behind' if best > 0 else 'ahead'
    today = df['difference'].iloc[-1]
    today_desc = 'behind' if today > 0 else 'ahead'

    plot_months(ndays, y=min(df['difference'])-5)
    plt.ylim(bottom=min(df['difference'])-10)
    plt.axhline(0, color='white', label=f'Worst: {abs(worst)} {worst_desc}\nBest: {abs(best)} {best_desc}\nToday: {abs(today)} {today_desc}')
    plt.xlabel('Days of 2023')
    plt.ylabel('# Miles Away from Goal')
    plt.legend(loc='upper right')
    plt.title("Distance from Goal Mileage")
    plt.savefig(images_path+'delta-miles')
    plt.close()

# Plot Average Pace

def pacing_lines(min=7, max=12):
    for i in range(int(np.floor(min)), int(np.ceil(max))):
        plt.axhline(i,  color='gray', alpha=0.1)

plot_pacing = True

if plot_pacing:

    for label in ['average', 'fastest', 'slowest']:
        label_pacing = df[label+'_mins']
        extent = 0.1
        pacing_lines(min = (1-extent)*np.min(label_pacing), 
                     max = (1+extent)*np.max(label_pacing))
        plot_months(ndays, y=0.9*np.min(label_pacing))

        # continuous colors
        plt.scatter(df['day'], label_pacing, c=df[label+'_mins'], cmap='cool')
        plt.xlabel('Days of 2023')
        plt.ylabel(label.capitalize()+' Pace (mins/mile)')
        plt.title(label.capitalize()+" Pacing")
        plt.savefig(images_path+label+"-pacing")
        plt.close()

    for day in df['day']:
        d = day - 1
        # print(f"Day: {day} Miles: {df['miles'][d]}")
        if df['miles'][d] > 0:
            nmiles = len(df['times'][d])
            plt.scatter([day]*nmiles, np.array(df['times'][d])/60.0) # , c=[df['average_mins'][d]]*nmiles)
    plt.xlabel('Days of 2023')
    plt.ylabel('Paces (mins/mile)')
    plt.title("Total Pacing")
    plt.savefig(images_path+"total-pacing")
    plt.close()

    times = list(df['times'])
    day_list = list(df['day'])
    box_cmap = colormaps.get_cmap('cool')
    box_colors_avg = box_cmap(scale(df['average_mins']))
    box_colors_miles = box_cmap(scale(df['miles']))
    for i in range(len(df['times'])):
        curr_day = df['day'][i]
        # print(df['day'][i], df['fastest_mins'][i], df['slowest_mins'][i], df['average_mins'][i])
        if df['miles'][i] > 0:
            plt.plot([curr_day, curr_day], [df['slowest_mins'][i], df['fastest_mins'][i]], color=box_colors_avg[i], linewidth=2)
    # plt.boxplot(times, positions=day_list)
    plot_months(ndays, y=0.8*np.min(df['slowest_mins']))
    plt.ylim(bottom=0.75*np.min(df['slowest_mins']))
    plt.title("Daily Pacing")
    plt.xlabel("Day")
    plt.ylabel("Pace Distribution")
    plt.savefig(images_path+"pacing-boxplot")
    plt.close()


# plot a histogram of all mile times
plot_distribution = True
if plot_distribution:
    all_mile_times = []

    for t in df['times']:
        all_mile_times += t

    all_mile_times = np.array(all_mile_times,dtype=float)
    all_mile_times /= 60.0
    pace_label = "Average: " + time_string(np.mean(all_mile_times)) + '\nFastest: ' + time_string(np.min(all_mile_times)) + '\nSlowest: ' + time_string(np.max(all_mile_times))
    plt.hist(all_mile_times,bins=50, label=pace_label)
    plt.legend(loc='upper left')
    plt.title("Pace Distribution")
    plt.xlabel("Pace (minutes)")
    plt.ylabel("Frequency")
    plt.savefig(images_path+'pacing-distribution')
    plt.close()


plot_daily_miles = True
if plot_daily_miles:
    color_miles = df['miles'][df['miles']>0]
    color_pace = df['average_mins'][df['miles']>0]
    daily_miles = df['miles'][df['miles']>0]
    daily_miles_label = "# of runs: " + str(len(daily_miles)) + "\nAverage: " + str(round(np.mean(daily_miles),2)) + ' mi\nShortest: ' + str(np.min(daily_miles)) + ' mi\nLongest: ' + str(np.max(daily_miles)) + ' mi'
    plt.scatter(df['day'][df['miles']>0], daily_miles, c=color_pace, cmap='cool', label=daily_miles_label)
    plt.axhline(y=0, color='white')
    plt.colorbar()
    plot_months(ndays, y=-1)
    plt.ylim(bottom=-2)
    plt.legend(loc='upper left')
    plt.xlabel("Day")
    plt.ylabel("Miles Per Run")
    plt.title("Daily Miles & Average Pace")
    plt.savefig(images_path+'daily-miles')
    plt.close()

plot_miles_per_week = True
if plot_miles_per_week:
    weeks = []
    miles_per_week = []
    current_week = 1
    current_miles = 0
    for i in range(len(df['day'])):
        day_i = df['day'][i]
        miles_i = df['miles'][i]
        # print(day_i, day_i % 7, miles_i)
        current_miles += miles_i
        if day_i % 7 == 0:
            weeks.append(current_week)
            miles_per_week.append(current_miles)
            current_week += 1
            current_miles = 0
    weeks.append(current_week)
    miles_per_week.append(current_miles)
    plt.axhline(y=7, color='gray', linestyle='dashed')
    plt.bar(weeks, miles_per_week)
    plt.xlabel("Week Number")
    plt.ylabel("Miles Per Week")
    plt.title("Weekly Miles")
    plt.savefig(images_path+'weekly-miles')