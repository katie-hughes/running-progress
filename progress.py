import numpy as np
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

plt.scatter(days, total_miles_lst, color='g')
plt.plot((1,maximum),(1, maximum), color='r')
for i in range(0, len(total_miles_lst)-1):
    plt.plot((days[i],days[i+1]), (total_miles_lst[i],total_miles_lst[i+1]), linestyle='dashed',color='g')
plt.show()

