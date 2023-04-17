import matplotlib.pyplot as plt
import numpy as np

days = []
miles = []
total_miles_lst = []
total_miles = 0

pacing = []

# parse file

with open('progress.txt') as f:
    for l in f.readlines():
        spl = l.split()
        day = int(spl[0])
        dist = int(spl[1])

        days.append(day)
        miles.append(dist)

        total_miles += dist
        total_miles_lst.append(total_miles)

        day_pacing = []
        for i in range(dist):
            try:
                mile_time = spl[i+2]
                mile_time_spl = mile_time.split(':')
                minutes = int(mile_time_spl[0])
                seconds = int(mile_time_spl[1])
                pace_in_seconds = minutes*60 + seconds
                # print(f"Minutes: {minutes}, seconds: {seconds}, total {pace_in_seconds}")
                day_pacing.append(pace_in_seconds)
            except:
                pass
        pacing.append(day_pacing)

maximum = max(total_miles_lst+days)

# Plot Cumulative Miles

plot_cumulative = False

if plot_cumulative:
    plt.plot((1,maximum),(1, maximum), color='b', label='Goal')
    for i in range(0, len(total_miles_lst)-1):
        # plt.plot((days[i],days[i+1]), (total_miles_lst[i],total_miles_lst[i+1]), linestyle='dashed',color='g')
        plt.plot((days[i],days[i+1]), (total_miles_lst[i],total_miles_lst[i]), linestyle='dashed',color='gray')
        plt.plot((days[i+1],days[i+1]), (total_miles_lst[i],total_miles_lst[i+1]), linestyle='dashed',color='gray')
    plt.scatter(days, total_miles_lst, color='k', label='Cumulative Miles')
    plt.xlabel('Days of 2023')
    plt.ylabel('# Miles')
    plt.legend()
    plt.savefig('cumulative-miles')
    plt.show()

# Plot difference from ideal

plot_difference = False

if plot_difference:
    diff = []
    for i in range(0, len(total_miles_lst)):
        diff.append(days[i] - total_miles_lst[i])
    for i in range(len(diff)):
        color = 'g'
        if diff[i] > 0:
            color='r'
        plt.plot((days[i],days[i]), (0,diff[i]), linestyle='dashed',color=color)
    plt.scatter(days, diff, color='k', label='Runs')
    plt.axhline(0, color='b', label='Goal')
    plt.xlabel('Days of 2023')
    plt.ylabel('# Miles Away from Goal')
    plt.legend()
    plt.savefig('delta-miles')
    plt.show()

# Plot Average Pace

plot_pacing = True
avg_pace = []
avg_pace_mins = []
fastest_pace = []
fastest_pace_mins = []
if plot_pacing:
    for i in range(0, len(days)):
        avg_pace.append(np.mean(pacing[i]))
        avg_pace_mins.append(avg_pace[i]/60.0)
        fastest_pace.append(min(pacing[i]))
        fastest_pace_mins.append(fastest_pace[i]/60.0)
        # mins = int(avg_pace[i]//60)
        # secs = avg_pace[i] - mins*60
        # print(f"Avg Pace Day {days[i]}: {avg_pace[i]} {mins}:{secs}")
    plt.scatter(days, avg_pace_mins)
    plt.xlabel('Days of 2023')
    plt.ylabel('Avg Pace (mins/mile)')
    plt.savefig("average-pacing")
    plt.show()

    plt.scatter(days, fastest_pace_mins)
    plt.xlabel('Days of 2023')
    plt.ylabel('Fastest Mile (mins/mile)')
    plt.savefig("fastest-pacing")
    plt.show()