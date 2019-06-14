# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 14:38:02 2019

@author: eebinger
"""

import csv
#import datetime as datetime
#import arcpy
#import gdaltools

working_dir = r'C:\Desktop\BLUEBikes'
data_files = [
	'201812-bluebikes-tripdata.csv',
	'201811-bluebikes-tripdata.csv',
	'201810-bluebikes-tripdata.csv',
	'201809-bluebikes-tripdata.csv',
	'201808-bluebikes-tripdata.csv',
    '201807-bluebikes-tripdata.csv',
	'201806-bluebikes-tripdata.csv',
	'201805-bluebikes-tripdata.csv',
	'201804-hubway-tripdata.csv',
	'201803_hubway_tripdata.csv',
	'201802_hubway_tripdata.csv',
	'201801_hubway_tripdata.csv'
]

stations = []
station_dict = {}
for f in data_files:
    # collect stations
    #stations = []
    with open(working_dir + "/trip_data/" + f, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        print("reading csv: " + f)
        for trip in reader:
            try:
                stations.append(int(trip['start station id']))
                stations.append(int(trip['end station id']))
            except ValueError:
                continue
        #end for
    #end with
    csvfile.close()
    stations = list(set(stations))
    
    # create dict to store records per station, fill with unique station attributes
    #station_dict = {}
    for s in stations:
		with open(working_dir + "/trip_data/" + f, 'r') as csvfile:
			reader = csv.DictReader(csvfile)
			for trip in reader:
				try:
					if s == int(trip['start station id']):
						station_dict[s] = {
							"name": trip['start station name'],
							"lat": trip['start station latitude'],
							"lon": trip['start station longitude'],
						}
						break
					elif s == int(trip['end station id']):
						station_dict[s] = {
							"name": trip['end station name'],
							"lat": trip['end station latitude'],
							"lon": trip['end station longitude'],
						}
						break
					#end if
				except ValueError:
					continue
				#end try
			#end for
		#end with
		csvfile.close()
	#end for
#end for
    
# write to CSV
with open(working_dir+"/geojson_data/stations_"+data_files[0][:4]+".csv", "wb") as csv_file:
    writer = csv.writer(csv_file)
    #data_files_trunc = [x[:6] for x in data_files]
    writer.writerow(["station_id", "name", "lat", "lon"])
    for s in stations:
        writer.writerow([s, station_dict[s]["name"], station_dict[s]["lat"], station_dict[s]["lon"]])
    #end for
#end with
csv_file.close()