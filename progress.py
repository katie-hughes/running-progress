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

plot_cumulative = True

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
    plt.title("Cumulative Miles Ran")
    plt.savefig('cumulative-miles')
    plt.close()

# Plot difference from ideal

plot_difference = True

if plot_difference:
    diff = []
    plt.axhline(10, color='gray', alpha=0.2)
    plt.axhline(20, color='gray', alpha=0.2)
    plt.axhline(30, color='gray', alpha=0.2)
    for i in range(0, len(total_miles_lst)):
        diff.append(days[i] - total_miles_lst[i])
    for i in range(len(diff)):
        color = 'g'
        if diff[i] > 30:
            color='maroon'
        elif diff[i] > 20:
            color='r'
        elif diff[i] > 10: 
            color='orange'
        elif diff[i] > 0:
            color='gold'
        plt.plot((days[i],days[i]), (0,diff[i]), color=color)
    plt.scatter(days, diff, color='k', label='Runs')
    plt.axhline(0, color='b', label='Goal')
    plt.xlabel('Days of 2023')
    plt.ylabel('# Miles Away from Goal')
    plt.legend()
    plt.title("Distance from Goal Mileage")
    plt.savefig('delta-miles')
    plt.close()

# Plot Average Pace

def colorcode_pacing(day, pace):
    color = None
    if pace > 11.5:
        color='red'
    elif pace > 11:
        color='orange'
    elif pace > 10.5:
        color='gold'
    elif pace > 10:
        color='lime'
    elif pace > 9.5:
        color='green'
    else:
        color='blue'
    plt.axhline(8,  color='gray', alpha=0.01)
    plt.axhline(9,  color='gray', alpha=0.01)
    plt.axhline(10, color='gray', alpha=0.01)
    plt.axhline(11, color='gray', alpha=0.01)
    plt.plot((day,day), (0,pace), color=color, alpha=0.75)
    plt.scatter(day, pace, color=color, alpha=0.75)
    return color

def pacing_lines():
    for i in range(7, 12):
        plt.axhline(i,  color='gray', alpha=0.3)



def colormap(pace):
    # range from (1,0,0) to (0,1,0)
    # max: 12 min: 6
    # 6 -> 0 -> (0,0,1) (blue)
    # 12 -> 1 -> (1,0,0) (red)
    scaled = (np.array(pace) - 6)/6
    # print(scaled)
    red = scaled
    blue = 1 - red
    return [(red[i], 0, blue[i]) for i in range(len(scaled))]




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
        # print(f"Day {days[i]}: {avg_pace[i]} {mins}:{secs}")


    # for i in range(len(avg_pace_mins)):
    #     c = colorcode_pacing(days[i], avg_pace_mins[i])
    # plt.scatter(days, avg_pace_mins, color='k')
    pacing_lines()
    plt.bar(days, avg_pace_mins, color=colormap(avg_pace_mins))
    plt.ylim(bottom=6.0)
    plt.xlabel('Days of 2023')
    plt.ylabel('Avg Pace (mins/mile)')
    plt.title("Average Pacing")
    plt.savefig("average-pacing")
    plt.close()

    # for i in range(len(fastest_pace_mins)):
    #     c = colorcode_pacing(days[i], fastest_pace_mins[i])
    # plt.scatter(days, fastest_pace_mins, c=fastest_pace_mins, cmap='rainbow')
    pacing_lines()
    plt.bar(days, fastest_pace_mins, color=colormap(fastest_pace_mins))
    plt.ylim(bottom=6.0)
    plt.xlabel('Days of 2023')
    plt.ylabel('Fastest Mile (mins/mile)')
    plt.title("Fastest Mile Pace")
    plt.savefig("fastest-pacing")
    plt.close()