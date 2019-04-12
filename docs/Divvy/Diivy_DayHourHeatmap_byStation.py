# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 14:38:02 2019

@author: eebinger
"""

import csv
import datetime as datetime

working_dir = r'C:\Users\eebinger\Desktop\Divvy'
data_files = [
	#['Divvy_Trips_2013.csv', '2013'],
    #['Divvy_Trips_2014_Q1.csv', '2014'],
    #['Divvy_Trips_2014_Q2.csv', '2014'],
    #['Divvy_Trips_2014_07.csv', '2014'],
	#['Divvy_Trips_2014_08.csv', '2014'],
	#['Divvy_Trips_2014_09.csv', '2014'],
    #['Divvy_Trips_2014_Q4.csv', '2014'],
	#['Divvy_Trips_2015_Q1.csv', '2015'],
	#['Divvy_Trips_2015_Q2.csv', '2015'],
    #['Divvy_Trips_2015_07.csv', '2015'],
	#['Divvy_Trips_2015_08.csv', '2015'],
	#['Divvy_Trips_2015_09.csv', '2015'],
    #['Divvy_Trips_2015_Q4.csv', '2015'],
	#['Divvy_Trips_2016_Q1.csv', '2016'],
	#['Divvy_Trips_2016_04.csv', '2016'],
	#['Divvy_Trips_2016_05.csv', '2016'],
	#['Divvy_Trips_2016_06.csv', '2016'],
    #['Divvy_Trips_2016_Q3.csv', '2016'],
    #['Divvy_Trips_2016_Q4.csv', '2016'],
	#['Divvy_Trips_2017_Q1.csv', '2017'],
	#['Divvy_Trips_2017_Q2.csv', '2017'],
    #['Divvy_Trips_2017_Q3.csv', '2017'],
    #['Divvy_Trips_2017_Q4.csv', '2017'],
	#['Divvy_Trips_2018_Q1.csv', '2018'],
	['Divvy_Trips_2018_Q2.csv', '2018'],
    ['Divvy_Trips_2018_Q3.csv', '2018'],
    ['Divvy_Trips_2018_Q4.csv', '2018']
]

for f in data_files:
	# collect stations
	stations = []
	with open(working_dir + "/trip_data/" + f[0], 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		print("reading csv: " + f[0])
		for trip in reader:
			stations.append(int(trip['from_station_id']))
			stations.append(int(trip['to_station_id']))
		#end for
	#end with
	csvfile.close()
	stations = list(set(stations))

	# loop through months
	year = f[1]
	month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
	for month in month_list:
		#print(year+month)
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
					start_time = str(trip['starttime'])
					station_id = int(trip['from_station_id'])
					start_time = datetime.datetime.strptime(start_time, '%m/%d/%Y %H:%M')
				except ValueError:
					try:
						start_time = datetime.datetime.strptime(start_time, '%m/%d/%Y %H:%M:%S')
					except ValueError:
						try:
							start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
						except ValueError:
							try:
								start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
							except ValueError:
								continue
				except KeyError:
					try:
						start_time = str(trip['start_time'])
						station_id = int(trip['from_station_id'])
						start_time = datetime.datetime.strptime(start_time, '%m/%d/%Y %H:%M')
					except ValueError:
						try:
							start_time = datetime.datetime.strptime(start_time, '%m/%d/%Y %H:%M:%S')
						except ValueError:
							try:
								start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
							except ValueError:
								continue
				#end try
				start_dow = start_time.weekday()
				start_hour = start_time.hour
				if str(start_time.month).zfill(2) == month:
					heatmap_dict[(start_dow, start_hour)][-1] += 1
					heatmap_dict[(start_dow, start_hour)][stations.index(station_id)] += 1 
				#end if
			#end for
		#end with
		csvfile.close()
		
		# sum heatmap_dict, if 0 then skip writing
		hcount = 0
		for d in range(0,7):
			for h in range(0,24):
				hcount += heatmap_dict[(d,h)][-1]
			#end for
		#end for
		if hcount > 0:
			# write to CSV
			print("saving csv: heatmap_data_"+year+month+".csv")
			with open(working_dir+ "/heatmap_data/heatmap_data_"+year+month+".csv", "wb") as csv_file:
				writer = csv.writer(csv_file)
				writer.writerow(["day"] + ["hour"] + stations + ["total"])
				for d in range(0,7):
					for h in range(0,24):
						writer.writerow([d] + [h] + heatmap_dict[(d,h)])
					#end for
				#end for
			#end with
			csv_file.close()
		#end if
	#end for
#end for