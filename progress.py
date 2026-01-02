import matplotlib.pyplot as plt
import matplotlib.cm as colormaps
import argparse
import numpy as np
import pandas as pd
from datetime import date
import calendar


# general utility functions

def time_string(time_minutes):
    return f"{int(time_minutes // 1)}:{int((time_minutes % 1)*60):02d}"

def convert_miletime(str):
    mile_time_spl = str.split(':')
    minutes = int(mile_time_spl[0])
    seconds = int(mile_time_spl[1])
    pace_in_seconds = minutes*60 + seconds
    return pace_in_seconds

def scale(lst):
    return (lst-np.min(lst))/(np.max(lst)-np.min(lst))

# main class for parsing file + plotting stats

class RunProgress:
    def __init__(self, year: int) -> None:
        self.year = year

        days_in_year = (date(year+1, 1, 1) - date(year, 1, 1)).days
        # days through the year, such that Jan. 1 is day 1
        self.ndays = min((date.today() - date(year-1, 12, 31)).days, days_in_year)

        self.fname = f'{year}/progress.txt'

        self.images_path = f'plots/{year}/'

        self.df = pd.DataFrame({'day': [], 'miles': [], 'times': [], 'times_str': [], 'average': [], 'fastest': [], 'slowest': []})
        self._parse_file()

        # print(plt.style.available)
        plt.style.use('dark_background')

    def _parse_file(self) -> None:
        with open(self.fname) as f:
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
                
                while(day - 1 != len(self.df.index)):
                    self.df.loc[len(self.df.index)] = np.array([len(self.df.index)+1, 0, [], [], np.nan, np.nan, np.nan],dtype=object)

                # put this when day - 1 == index
                self.df.loc[len(self.df.index)] = np.array([day, dist, day_pacing, raw_times, np.mean(day_pacing), np.min(day_pacing), np.max(day_pacing)],dtype=object)


        while(self.ndays > len(self.df.index)):
            self.df.loc[len(self.df.index)] = np.array([len(self.df.index)+1, 0, [], [], np.nan, np.nan, np.nan],dtype=object)

        self.df[["day", "miles", "average", "fastest", "slowest"]] = self.df[["day", "miles", "average", "fastest", "slowest"]].apply(pd.to_numeric)

        self.df['cumulative_miles'] = self.df['miles'].cumsum()
        self.df['difference'] = self.df['day'] - self.df['cumulative_miles']

        for label in ['average', 'fastest', 'slowest']:
            self.df[label+'_mins'] = self.df[label]/60.0

    def _plot_months(self,current_days, y=0):
        total_days = 0
        for month in range(1,13):
            days_in_month = calendar.monthrange(self.year, month)[1]
            plt.axvline(total_days, color='gray', alpha=0.1)
            plt.text(total_days, y, calendar.month_name[month][:3], rotation=90, verticalalignment='center', color='gray', alpha=0.8)
            total_days += days_in_month
            if total_days > current_days:
                return

    def print_summary(self):
        total_miles = np.max(self.df['cumulative_miles'])
        todays_miles = self.df['miles'][self.ndays-1]
        if (todays_miles > 0):
            print(f"Running 365 miles in {self.year}!")
            print()
            print(f"Day: {self.ndays}/365")
            print(f"Miles: {total_miles}/365")
            print()
            print(f"Today: {todays_miles} miles")
            for i,mile_time in enumerate(self.df['times_str'][self.ndays-1]):
                if i < todays_miles - 1:
                    print(mile_time, end='/')
                else:
                    print(mile_time)
        else:
            print(f"Days of {self.year}:\t{self.ndays}")
            print(f"Current Miles:\t{total_miles}")

    def plot_cumulative_miles(self):
        total_miles = np.max(self.df['cumulative_miles'])
        maximum = max(np.max(self.df['day']), np.max(self.df['cumulative_miles']))
        self._plot_months(self.ndays, y=-12)
        plt.ylim(bottom=-30, top=maximum*1.1)
        plt.plot((1,maximum),(1, maximum), color='white', label=f'Goal ({self.ndays})')
        plt.plot(self.df['day'], self.df['cumulative_miles'], color='aqua', label=f'Cumulative Miles ({total_miles})')
        plt.xlabel(f'Days of {self.year}')
        plt.ylabel('# Miles')
        plt.legend(loc='upper left')
        plt.title("Cumulative Miles Ran")
        plt.savefig(self.images_path+'cumulative-miles')
        plt.close()

    # Plot difference from ideal
    def plot_difference(self):
        for i in range(0, 31, 10):
            plt.axhline(i, color='gray', alpha=0.1)
        cmap = colormaps.get_cmap('rainbow')
        colors = cmap(self.df['difference']/np.max(self.df['difference']))
        plt.bar(self.df['day'], self.df['difference'], width=1.0, color=colors)

        worst = max(self.df['difference'])
        worst_desc = 'behind' if worst > 0 else 'ahead'
        best = min(self.df['difference'])
        best_desc = 'behind' if best > 0 else 'ahead'
        today = self.df['difference'].iloc[-1]
        today_desc = 'behind' if today > 0 else 'ahead'

        self._plot_months(self.ndays, y=min(self.df['difference'])-5)
        plt.ylim(bottom=min(self.df['difference'])-10)
        plt.axhline(0, color='white', label=f'Worst: {abs(worst)} {worst_desc}\nBest: {abs(best)} {best_desc}\nToday: {abs(today)} {today_desc}')
        plt.xlabel(f'Days of {self.year}')
        plt.ylabel('# Miles Away from Goal')
        plt.legend(loc='upper right')
        plt.title("Distance from Goal Mileage")
        plt.savefig(self.images_path+'delta-miles')
        plt.close()

    def _pacing_lines(self, min=7, max=12):
        for i in range(int(np.floor(min)), int(np.ceil(max))):
            plt.axhline(i,  color='gray', alpha=0.1)

    # Plot Average Pace
    def plot_pacing(self):
        for label in ['average', 'fastest', 'slowest']:
            label_pacing = self.df[label+'_mins']
            extent = 0.1
            self._pacing_lines(min = (1-extent)*np.min(label_pacing), 
                               max = (1+extent)*np.max(label_pacing))
            self._plot_months(self.ndays, y=0.9*np.min(label_pacing))

            # continuous colors
            plt.scatter(self.df['day'], label_pacing, c=self.df[label+'_mins'], cmap='cool')
            plt.xlabel(f'Days of {self.year}')
            plt.ylabel(label.capitalize()+' Pace (mins/mile)')
            plt.title(label.capitalize()+" Pacing")
            plt.savefig(self.images_path+label+"-pacing")
            plt.close()

        for day in self.df['day']:
            d = day - 1
            if self.df['miles'][d] > 0:
                nmiles = len(self.df['times'][d])
                plt.scatter([day]*nmiles, np.array(self.df['times'][d])/60.0) # , c=[df['average_mins'][d]]*nmiles)
        plt.xlabel(f'Days of {self.year}')
        plt.ylabel('Paces (mins/mile)')
        plt.title("Total Pacing")
        plt.savefig(self.images_path+"total-pacing")
        plt.close()

        box_cmap = colormaps.get_cmap('cool')
        box_colors_avg = box_cmap(scale(self.df['average_mins']))
        for i in range(len(self.df['times'])):
            curr_day = self.df['day'][i]
            if self.df['miles'][i] > 0:
                plt.plot([curr_day, curr_day], [self.df['slowest_mins'][i], self.df['fastest_mins'][i]], color=box_colors_avg[i], linewidth=2)
        self._plot_months(self.ndays, y=0.8*np.min(self.df['slowest_mins']))
        plt.ylim(bottom=0.75*np.min(self.df['slowest_mins']))
        plt.title("Daily Pacing")
        plt.xlabel("Day")
        plt.ylabel("Pace Distribution")
        plt.savefig(self.images_path+"pacing-boxplot")
        plt.close()

    def plot_time_distribution(self):
        # plot a histogram of all mile times
        all_mile_times = []

        for t in self.df['times']:
            all_mile_times += t

        all_mile_times = np.array(all_mile_times,dtype=float)
        all_mile_times /= 60.0
        pace_label = "Average: " + time_string(np.mean(all_mile_times)) + '\nFastest: ' + time_string(np.min(all_mile_times)) + '\nSlowest: ' + time_string(np.max(all_mile_times))
        plt.hist(all_mile_times,bins=50, label=pace_label)
        plt.legend(loc='upper left')
        plt.title("Pace Distribution")
        plt.xlabel("Pace (minutes)")
        plt.ylabel("Frequency")
        plt.savefig(self.images_path+'pacing-distribution')
        plt.close()

    def plot_daily_miles(self):
        color_pace = self.df['average_mins'][self.df['miles']>0]
        daily_miles = self.df['miles'][self.df['miles']>0]
        daily_miles_label = "# of runs: " + str(len(daily_miles)) + "\nAverage: " + str(round(np.mean(daily_miles),2)) + ' mi\nShortest: ' + str(np.min(daily_miles)) + ' mi\nLongest: ' + str(np.max(daily_miles)) + ' mi'
        plt.scatter(self.df['day'][self.df['miles']>0], daily_miles, c=color_pace, cmap='cool', label=daily_miles_label)
        plt.axhline(y=0, color='white')
        plt.colorbar()
        self._plot_months(self.ndays, y=-1)
        plt.ylim(bottom=-2)
        plt.legend(loc='upper left')
        plt.xlabel("Day")
        plt.ylabel("Miles Per Run")
        plt.title("Daily Miles & Average Pace")
        plt.savefig(self.images_path+'daily-miles')
        plt.close()

    def plot_miles_per_week(self):
        weeks = []
        miles_per_week = []
        current_week = 1
        current_miles = 0
        for i in range(len(self.df['day'])):
            day_i = self.df['day'][i]
            miles_i = self.df['miles'][i]
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
        plt.savefig(self.images_path+'weekly-miles')
        plt.close()

def main():
    parser = argparse.ArgumentParser(description='Tracking Runs!')
    parser.add_argument('-y', '--year', help='Which year?', default=date.today().year, type=int)
    args = parser.parse_args()
    year = args.year
    run_progress = RunProgress(year=year)

    run_progress.print_summary()
    run_progress.plot_cumulative_miles()
    run_progress.plot_daily_miles()
    run_progress.plot_difference()
    run_progress.plot_miles_per_week()
    run_progress.plot_pacing()
    run_progress.plot_time_distribution()

if __name__ == "__main__":
    main()
