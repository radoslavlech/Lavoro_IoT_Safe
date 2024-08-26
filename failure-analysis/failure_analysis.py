##Created 02.07 for the analysis of system 15

from matplotlib import pyplot as plt
import pandas as pd
import os
import json
from datetime import datetime

path = "systems"
files_list = os.listdir(path)

#DATA FROM AN EXEMPLARY FILE
data = pd.read_csv(f"{path}/{files_list[5]}",sep = ';')
data.info()

print('\n')
print(data)

days_list=[]
days_data=[]
points_1day = []
points_all = []
trips_points_all = []
daily_means = []
daily_variances = []


day = '0'
for j in range(len(data)):
    message = data['message'][j]
    message = json.loads(message)
    service = data['service'][j]
    alg_timestamp = data['datetime']


    if j == 0:
        print("Content of message:")
        for i in message:
            print(i)
        print('\n')


    # try:
    #     print(message['sensors'])
    # except:
    #     pass





    #DOOR OPERATIONS
    try:
        door_operations = message['data']['doors_operations']
        for k, reg in enumerate(door_operations):
            start = reg['time_start']
            current_day = datetime.utcfromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')[:10]

            end = reg['time_end']
            max_ax = reg['a_std_max_x']
            max_ay = reg['a_std_max_y']
            max_az = reg['a_std_max_z']
            floor = reg['floor']
            duration = reg['duration']
            system = message['system']


            # print(f"door operation:{k}/{j}/{current_day}")

            point = {'time':start,'coords':(max_ax,max_ay,max_az),'system': system, 'floor':floor,'date':current_day,'duration':duration}
            points_all.append(point)
            points_1day.append(point)


            if current_day != day:
                if current_day in days_list:
                    idx = days_list.index(current_day)
                    days_data[idx]+=points_1day
                else:
                    points_1day.reverse()
                    days_list.append(current_day)
                    days_data.append(points_1day)
                    #calculatoing the daily means
                    mean = 0
                    variance = 0
                    for point in points_1day:
                        mean+=point['duration']
                    mean = mean/len(points_1day)
                    for point in points_1day:
                        variance+=(point['duration']-mean)**2
                    daily_means.append(mean)
                    daily_variances.append(variance)
                points_1day = []

            day = datetime.utcfromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')[:10]
    except:
        pass

    if service!= "DM":
        print(service)
    #TRIPS
    try:
        mess_data = message['data']
        if type(mess_data)==dict:
            trips = message['data']['trips']
        elif type(mess_data)==list:
            trips = mess_data
        for k, trip in enumerate(trips):
            start = trip['time_start']
            current_day = datetime.utcfromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')[:10]
            end = trip['time_end']
            floor_error = trip['floor_error']
            floors_no = trip['floors']
            duration = trip['duration']
            floor_end = trip['floor_end']
            system = message['system']

            point = {'start_time':start, 'duration':duration,'floors_no':floors_no,'floor_end':floor_end, 'date':current_day, 'floor_error':floor_error}
            trips_points_all.append(point)
            if datetime.utcfromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')=='2024-07-02 12:45:01':
                print(trip)

    except:
        pass



points_all.reverse()
trips_points_all.reverse()
days_data.reverse()
days_list.reverse()
days_data.reverse()
# daily_means.reverse()
# daily_variances.reverse()

print(f"total number of trips: {len(trips_points_all)}")

#COMBINED PLOT FOR ALL DAYS


title_dt = f"door operation duration for {system} (all floors)"
fig_dt = plt.figure()
ax_dt = fig_dt.add_subplot(111)
ax_dt.set(title = title_dt)
ax_dt.set_xlabel('start time')
ax_dt.set_ylabel('door_operation duration')
ax_dt.tick_params(axis='x', rotation=35, labelsize='3')


title_P6 = f"door operation duration for {system} (only floor 6)"
fig_P6 = plt.figure()
ax_P6 = fig_P6.add_subplot(111)
ax_P6.set(title = title_P6)
ax_P6.set_xlabel('start time')
ax_P6.set_ylabel('door_operation duration')
ax_P6.tick_params(axis='x', rotation=35, labelsize=6)


title_trips_dur1 = "1-floor-long trips duration for System 15"
fig_trips = plt.figure()
ax_trips = fig_trips.add_subplot(111)
ax_trips.set(title = title_trips_dur1)
ax_trips.set_xlabel('start time')
ax_trips.set_ylabel('1-flor trip duration')
ax_trips.tick_params(axis='x', rotation=35, labelsize=6)
ax_trips.grid(axis='x')


title_trips_P6 = "1-floor-long trips duration in arrival to floor 6"
fig_trips_P6 = plt.figure()
ax_trips_P6 = fig_trips_P6.add_subplot(111)
ax_trips_P6.set(title = title_trips_P6)
ax_trips_P6.set_xlabel('start time')
ax_trips.set_ylabel('1-flor trip duration')
ax_trips_P6.tick_params(axis='x', rotation=35, labelsize='small')

title_trips_2f = "2-floor-long trips duration"
fig_trips_2f = plt.figure()
ax_trips_2f = fig_trips_2f.add_subplot(111)
ax_trips_2f.set(title = title_trips_2f)
ax_trips_2f.set_xlabel('start time')
ax_trips_2f.set_ylabel('2-flor trip duration')
ax_trips_2f.tick_params(axis='x', rotation=35, labelsize='small')

title_trips_3f = "3-floor-long trips duration"
fig_trips_3f = plt.figure()
ax_trips_3f = fig_trips_3f.add_subplot(111)
ax_trips_3f.set(title = title_trips_3f)
ax_trips_3f.set_xlabel('start time')
ax_trips_3f.set_ylabel('3-flor trip duration')
ax_trips_3f.tick_params(axis='x', rotation=35, labelsize='small')

title_means = "Daily means of door_operation time"
fig_means = plt.figure()
ax_means = fig_means.add_subplot(111)
ax_means.set(title = title_means)
ax_means.set_xlabel('day')
ax_means.set_ylabel('mean duration')
ax_means.tick_params(axis='x', rotation=35, labelsize='small')


title_var = "Daily variance of door_operation time"
fig_var = plt.figure()
ax_var = fig_var.add_subplot(111)
ax_var.set(title = title_var)
ax_var.set_xlabel('day')
ax_var.set_ylabel('mean duration')
ax_var.tick_params(axis='x', rotation=35, labelsize='small')

times = []
times_P6 = []
dt = []
dt_P6 = []




for point in points_all:
    if point['floor']!='N/A':
        times.append(datetime.utcfromtimestamp(point['time']).strftime('%Y-%m-%d %H:%M:%S'))
        dt.append(point['duration'])
        if int(point['floor'])==6:
            times_P6.append(datetime.utcfromtimestamp(point['time']).strftime('%Y-%m-%d %H:%M:%S'))
            dt_P6.append(point['duration'])



trip_up_times = []
trip_up_durations = []
trip_down_times = []
trip_down_durations = []
trip_times_P6 = []
trip_durations_P6 = []


legend6 = True
legend_other = True
for point in trips_points_all:
    if point['floor_error']=='':
        if int(point['floors_no'])==-1:
            trip_down_times.append(datetime.utcfromtimestamp(point['start_time']).strftime('%Y-%m-%d %H:%M:%S'))
            trip_down_durations.append(point['duration'])
            if point['floor_end']!='N/A' and int(point['floor_end'])==6:
                trip_times_P6.append(datetime.utcfromtimestamp(point['start_time']).strftime('%Y-%m-%d %H:%M:%S'))
                trip_durations_P6.append(point['duration'])
                if legend6:
                    ax_trips.scatter(datetime.utcfromtimestamp(point['start_time']).strftime('%Y-%m-%d %H:%M:%S'),point['duration'],color='r', marker="v",label= '6-th floor')
                    legend6 = False
                else:
                    ax_trips.scatter(datetime.utcfromtimestamp(point['start_time']).strftime('%Y-%m-%d %H:%M:%S'),point['duration'],color='r', marker="v")
            else:
                if legend_other:
                    ax_trips.scatter(datetime.utcfromtimestamp(point['start_time']).strftime('%Y-%m-%d %H:%M:%S'),point['duration'],color='b', marker="v",label= 'other floors')
                    legend_other = False
                else:
                    ax_trips.scatter(datetime.utcfromtimestamp(point['start_time']).strftime('%Y-%m-%d %H:%M:%S'),point['duration'],color='b', marker="v")

        if int(point['floors_no'])==1:
            trip_up_times.append(datetime.utcfromtimestamp(point['start_time']).strftime('%Y-%m-%d %H:%M:%S'))
            trip_up_durations.append(point['duration'])
            if point['floor_end']!='N/A' and int(point['floor_end'])==6:
                trip_times_P6.append(datetime.utcfromtimestamp(point['start_time']).strftime('%Y-%m-%d %H:%M:%S'))
                trip_durations_P6.append(point['duration'])
                if legend6:
                    ax_trips.scatter(datetime.utcfromtimestamp(point['start_time']).strftime('%Y-%m-%d %H:%M:%S'),point['duration'],color='r', marker="^",label= '6-th floor')
                    legend6=False
                else:
                    ax_trips.scatter(datetime.utcfromtimestamp(point['start_time']).strftime('%Y-%m-%d %H:%M:%S'),point['duration'],color='r', marker="^")
            else:
                ax_trips.scatter(datetime.utcfromtimestamp(point['start_time']).strftime('%Y-%m-%d %H:%M:%S'),point['duration'],color='b', marker="^")

        if int(point['floors_no'])==2 or int(point['floors_no'])==-2:
            if point['floor_end']!='N/A' and int(point['floor_end'])==6:
                ax_trips_2f.scatter(datetime.utcfromtimestamp(point['start_time']).strftime('%Y-%m-%d %H:%M:%S'),point['duration'],color='r', marker="o")
            else:
                ax_trips_2f.scatter(datetime.utcfromtimestamp(point['start_time']).strftime('%Y-%m-%d %H:%M:%S'),point['duration'],color='b', marker="o")

        if int(point['floors_no'])==3 or int(point['floors_no'])==-3:
            if point['floor_end']!='N/A' and int(point['floor_end'])==6:
                ax_trips_3f.scatter(datetime.utcfromtimestamp(point['start_time']).strftime('%Y-%m-%d %H:%M:%S'),point['duration'],color='r', marker="o")
            else:
                ax_trips_3f.scatter(datetime.utcfromtimestamp(point['start_time']).strftime('%Y-%m-%d %H:%M:%S'),point['duration'],color='b', marker="o")

ax_dt.plot(times,dt, color= 'b') #For all floors
ax_P6.plot(times_P6,dt_P6, color= 'r') #Only for 6-th floor

ax_trips_P6.scatter(trip_times_P6,trip_durations_P6,color='r', marker="o")
ax_trips_P6.plot(trip_times_P6,trip_durations_P6, linewidth=0.5, linestyle='dashed')
ax_trips.legend()



ax_means.scatter(days_list,daily_means, color ='orange')
ax_means.plot(days_list,daily_means, color ='orange',linewidth=0.5)
ax_var.scatter(days_list, daily_variances, color ='g')
ax_var.plot(days_list, daily_variances, color ='g', linewidth=0.5)

plt.show()

exit()

#PLOT DAY BY DAY
for day in days_data:
    date = day[0]['date']

    #Plot of horizontal acceleration
    title = f"acc. data from {date}"
    fig3 = plt.figure()
    ax5 = fig3.add_subplot(111)
    ax5.set(title = title)
    ax5.set_xlabel('time')
    ax5.set_ylabel('max a_x')

    times = []
    dt = []
    for point in day:
        times.append(datetime.utcfromtimestamp(point['time']).strftime('%Y-%m-%d %H:%M:%S'))
        dt.append(point['duration'])
    ax5.plot(times,dt)
    plt.show()

