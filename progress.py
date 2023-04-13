import matplotlib.pyplot as plt

days = []
miles = []
total_miles_lst = []
total_miles = 0

with open('progress.txt') as f:
    for l in f.readlines():
        spl = l.split()
        day = int(spl[0])
        dist = int(spl[1])

        days.append(day)
        miles.append(dist)

        total_miles += dist
        total_miles_lst.append(total_miles)

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
    plt.savefig('cumulative-miles')
    plt.show()

# Plot difference from ideal

plot_difference = True

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