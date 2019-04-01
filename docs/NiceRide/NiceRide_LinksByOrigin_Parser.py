# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv, json
from datetime import datetime

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

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

for f in data_files:
    linksByOrigin = {}
    od_pairs = []
    year = int(f[:4])
    with open(working_dir + "/trip_data/" + f, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        print("read csv: " + f)
        for trip in reader:
            origin = trip['start station id']
            destination = trip['end station id']
            if origin not in linksByOrigin:
                linksByOrigin[origin] = []
            #end if
            links = linksByOrigin[origin]
            if [origin, destination] in od_pairs:
                for x in links:
                    if x['source']==origin and x['target']==destination:
                        x['count'] += 1
                    #end if
                #end for
            elif [origin, destination] not in od_pairs:
                links.append({
                    'source': origin, 
                    'target': destination,
                    'count': 1
                })
                od_pairs.append([origin, destination])
            #end if
        #end for
    #end with
    csvfile.close()
    with open(working_dir + "/json_data/" + f[:6] + "-tripdata.json", "w") as jsonfile:
        json.dump([linksByOrigin], jsonfile)
    jsonfile.close()
    print("saved as json: " + f[:6] + "-tripdata.json")
#end for

for f in old_data_files:
    year = f[1]
    linksByOrigin = {
        year+'01': {},
        year+'02': {},
        year+'03': {},
        year+'04': {},
        year+'05': {},
        year+'06': {},
        year+'07': {},
        year+'08': {},
        year+'09': {},
        year+'10': {},
        year+'11': {},
        year+'12': {}
    }
    with open(working_dir + "/trip_data/" + f[0], 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        print("read csv: " + f[0])
        for trip in reader:
            try:
                origin = int(trip['Start terminal'])
                destination = int(trip['End terminal'])
            except ValueError:
                continue
                print(trip)
            except KeyError:
                try:
                    origin = int(trip['Start station number'])
                    destination = int(trip['End station number'])
                except ValueError:
                    continue
            year = year
            month = str(datetime.strptime(trip['Start date'], '%m/%d/%Y %H:%M').month).zfill(2)
            if origin not in linksByOrigin[year+month]:
                linksByOrigin[year+month][origin] = []
            links = linksByOrigin[year+month][origin]
            dest_check = [x['target'] for x in links]
            if destination in dest_check:
                for x in links:
                    if x['source']==origin and x['target']==destination:
                        x['count'] += 1
                    #end if
                #end for
            else:
                links.append({
                    'source': origin, 
                    'target': destination,
                    'count': 1
                })
            #end if
    csvfile.close()
    for month in linksByOrigin.keys():
        with open(working_dir + "/json_data/" + month + "-tripdata.json", "w") as jsonfile:
            if len(linksByOrigin[month]) > 0:
                json.dump([linksByOrigin[month]], jsonfile)
        jsonfile.close()
        print("saved as json: " + month + "-tripdata.json")
    print("done: " + year)