# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 14:38:02 2019

@author: eebinger
"""

import csv
import datetime as datetime

working_dir = r'C:\Desktop\NiceRide'
data_files = [
	'201804-niceride-tripdata.csv',
	'201805-niceride-tripdata.csv',
	'201806-niceride-tripdata.csv',
	'201807-niceride-tripdata.csv',
	'201808-niceride-tripdata.csv',
	'201809-niceride-tripdata.csv',
	'201810-niceride-tripdata.csv',
	'201811-niceride-tripdata.csv'
]
old_data_files = [
	['Nice_Ride_trip_history_2010_season.csv', '2010'],
	['Nice_Ride_trip_history_2011_season.csv', '2011'],
	['Nice_Ride_trip_history_2012_season.csv', '2012'],
	['Nice_Ride_trip_history_2013_season.csv', '2013'],
	['Nice_Ride_trip_history_2014_season.csv', '2014'],
	['Nice_ride_trip_history_2015_season.csv', '2015'],
	['Nice_ride_trip_history_2016_season.csv', '2016'],
	['Nice_ride_trip_history_2017_season.csv', '2017']
]

for f in data_files:
    # collect stations
    stations = []
    with open(working_dir + "/trip_data/" + f, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        print("reading csv: " + f)
        for trip in reader:
            try:
                stations.append(int(trip['start station id']))
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
            try:
                start_time = str(trip['start_time'])
                station_id = int(trip['start station id'])
                start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
                start_dow = start_time.weekday()
                start_hour = start_time.hour
                heatmap_dict[(start_dow, start_hour)][-1] += 1
                heatmap_dict[(start_dow, start_hour)][stations.index(station_id)] += 1
            except ValueError:
                try:
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
    with open(working_dir+ "/heatmap_data/heatmap_data_"+f[:6]+".csv", "wb") as csv_file:
        writer = csv.writer(csv_file)
        #data_files_trunc = [x[:6] for x in data_files]
        writer.writerow(["day"] + ["hour"] + stations + ["total"])
        for d in range(0,7):
            for h in range(0,24):
                writer.writerow([d] + [h] + heatmap_dict[(d,h)])
            #end for
        #end for
    #end with
#end for

for f in old_data_files:
	# collect stations
	stations = []
	with open(working_dir + "/trip_data/" + f[0], 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		print("reading csv: " + f[0])
		for trip in reader:
			try:
				stations.append(int(trip['Start terminal']))
			except ValueError:
				continue
			except KeyError:
				try:
					stations.append(int(trip['Start station number']))
				except ValueError:
					continue
		#end for
	#end with
	csvfile.close()
	stations = list(set(stations))

	# loop through months
	year = f[1]
	month_list = ['04', '05', '06', '07', '08', '09', '10', '11']
	for month in month_list:
		print(year+month)
		# create dict to store records per station (+1 for total column)
		heatmap_dict = {}
		for d in range(0,7):
			for h in range(0,24):
				heatmap_dict[(d,h)] = [x*0 for x in range(len(stations)+1)]
			#end for
		#end for
		
		# fill dict with data
		with open(working_dir + "/trip_data/" + f[0], 'r') as csvfile:
			reader = csv.DictReader(csvfile)
			for trip in reader:
				try:
					start_time = str(trip['Start date'])
					station_id = int(trip['Start terminal'])
				except ValueError:
					continue
				except KeyError:
					try:
						start_time = str(trip['Start date'])
						station_id = int(trip['Start station number'])
					except ValueError:
						continue
				#end try
				start_time = datetime.datetime.strptime(start_time, '%m/%d/%Y %H:%M')
				start_dow = start_time.weekday()
				start_hour = start_time.hour
				if str(start_time.month).zfill(2) == month:
					heatmap_dict[(start_dow, start_hour)][-1] += 1
					heatmap_dict[(start_dow, start_hour)][stations.index(station_id)] += 1 
				#end if
			#end for
		#end with
		csvfile.close()
		
		# write to CSV
		with open(working_dir+ "/heatmap_data/heatmap_data_"+year+month+".csv", "wb") as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(["day"] + ["hour"] + stations + ["total"])
			for d in range(0,7):
				for h in range(0,24):
					writer.writerow([d] + [h] + heatmap_dict[(d,h)])
				#end for
			#end for
		#end with
	#end for
#end for