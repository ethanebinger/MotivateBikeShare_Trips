# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 14:38:02 2019

@author: eebinger
"""

import csv
import datetime as datetime

working_dir = r'../'
data_files = [
    #'201706-fordgobike-tripdata.csv',
    #'201707-fordgobike-tripdata.csv',
    #'201708-fordgobike-tripdata.csv',
    #'201709-fordgobike-tripdata.csv',
    #'201710-fordgobike-tripdata.csv',
    #'201711-fordgobike-tripdata.csv',
    #'201712-fordgobike-tripdata.csv',
    #'201801-fordgobike-tripdata.csv',
    #'201802-fordgobike-tripdata.csv',
    #'201803-fordgobike-tripdata.csv',
    #'201804-fordgobike-tripdata.csv',
    #'201805-fordgobike-tripdata.csv',
    #'201806-fordgobike-tripdata.csv',
    #'201807-fordgobike-tripdata.csv',
    #'201808-fordgobike-tripdata.csv',
    #'201809-fordgobike-tripdata.csv',
    #'201810-fordgobike-tripdata.csv',
	#'201811-fordgobike-tripdata.csv',
	#'201812-fordgobike-tripdata.csv',
	#'201901-fordgobike-tripdata.csv',
	#'201902-fordgobike-tripdata.csv',
    #'201903-fordgobike-tripdata.csv',
    #'201904-fordgobike-tripdata.csv',
    #'201905-baywheels-tripdata.csv',
    #'201906-baywheels-tripdata.csv',
    #'201907-baywheels-tripdata.csv',
    #'201908-baywheels-tripdata.csv',
    #'201909-baywheels-tripdata.csv',
    #'201910-baywheels-tripdata.csv',
    #'201911-baywheels-tripdata.csv',
    #'201912-baywheels-tripdata.csv',
    #'202001-baywheels-tripdata.csv',
    #'202002-baywheels-tripdata.csv',
    #'202003-baywheels-tripdata.csv',
    #'202004-baywheels-tripdata.csv',
    #'202005-baywheels-tripdata.csv',
    #'202006-baywheels-tripdata.csv',
    #'202007-baywheels-tripdata.csv',
    #'202008-baywheels-tripdata.csv',
    #'202009-baywheels-tripdata.csv',
    #'202010-baywheels-tripdata.csv',
    '202011-baywheels-tripdata.csv',
    '202012-baywheels-tripdata.csv',
    '202101-baywheels-tripdata.csv'
]

for f in data_files:
    # collect stations
    stations = []
    with open(working_dir + "/trip_data/" + f, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        print("reading csv: " + f)
        for trip in reader:
            try:
                stations.append(int(trip['start_station_id']))
            except ValueError:
                continue
        #end for
    #end with
    csvfile.close()
    stations = list(set(stations))
    
    # create dict to store records per station (+1 for total column)
    heatmap_dict = {}
    for d in range(0,7):
        for h in range(0,24):
            heatmap_dict[(d,h)] = [x*0 for x in range(len(stations)+1)]
        #end for
    #end for
    
    # fill dict with data
    with open(working_dir + "/trip_data/" + f, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for trip in reader:
            trip = dict(('start_time' if k=='started_at' else k, v) for k, v in trip.items())
            start_time = str(trip['start_time'])
            try:
                station_id = int(trip['start_station_id'])
                start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
                start_dow = start_time.weekday()
                start_hour = start_time.hour
                #start_dow = int(trip['WEEKDAY'])
                #start_hour = int(trip['HOUR'])
                heatmap_dict[(start_dow, start_hour)][-1] += 1
                heatmap_dict[(start_dow, start_hour)][stations.index(station_id)] += 1
            except ValueError:
                try:
                    station_id = int(trip['start_station_id'])
                    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                    start_dow = start_time.weekday()
                    start_hour = start_time.hour
                    heatmap_dict[(start_dow, start_hour)][-1] += 1
                    heatmap_dict[(start_dow, start_hour)][stations.index(station_id)] += 1
                except ValueError:
                    pass
                #end try
            #end try
        #end for
    #end with
    csvfile.close()
    
    # write to CSV
    with open(working_dir+ "/heatmap_data/heatmap_data_"+f[:6]+".csv", "w") as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        #data_files_trunc = [x[:6] for x in data_files]
        writer.writerow(["day"] + ["hour"] + stations + ["total"])
        for d in range(0,7):
            for h in range(0,24):
                writer.writerow([d] + [h] + heatmap_dict[(d,h)])
            #end for
        #end for
    #end with
#end for