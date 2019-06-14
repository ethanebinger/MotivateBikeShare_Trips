# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv, json
from datetime import datetime

working_dir = r'C:\Desktop\BLUEBikes'
data_files = [
	['hubway_Trips_2011.csv', '2011'],
    ['hubway_Trips_2012.csv', '2012'],
    ['hubway_Trips_2013.csv', '2013'],
    ['hubway_Trips_2014_1.csv', '2014'],
    ['hubway_Trips_2014_2.csv', '2014'],
    #['201901-bluebikes-tripdata.csv', '2019'],
	#['201902-bluebikes-tripdata.csv', '2019'],
    #['201903-bluebikes-tripdata.csv', '2019'],
    #['201904-bluebikes-tripdata.csv', '2019'],
    ['201905-bluebikes-tripdata.csv', '2019']
]

for f in data_files:
    year = f[1]
    linksByOrigin = {
		year+'01': {}, year+'02': {}, year+'03': {},
		year+'04': {}, year+'05': {}, year+'06': {},
		year+'07': {}, year+'08': {}, year+'09': {},
		year+'10': {}, year+'11': {}, year+'12': {}
	}
    with open(working_dir + "/trip_data/" + f[0], 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        print("read csv: " + f[0])
        for trip in reader:
            try:
                origin = int(trip['start station id'])
                destination = int(trip['end station id'])
            except KeyError:
                try:
                    origin = trip['Start station number']
                    destination = trip['End station number']
                except ValueError:
                    continue
            year = year
            try:
                month = str(datetime.strptime(trip['starttime'], '%Y-%m-%d %H:%M:%S.%f').month).zfill(2)
            except KeyError:
                try:
                    month = str(datetime.strptime(trip['Start date'], '%m/%d/%Y %H:%M').month).zfill(2)
                except ValueError:
                    try:
                        month = str(datetime.strptime(trip['starttime'], '%m/%d/%Y %H:%M:%S').month).zfill(2)
                    except ValueError:
                        print("ValueError 1")
                        continue
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
        #end for
    #end with
    csvfile.close()
    for month in linksByOrigin.keys():
        if len(linksByOrigin[month]) > 0:
            with open(working_dir + "/json_data/" + month + "-tripdata.json", "w") as jsonfile:
                json.dump([linksByOrigin[month]], jsonfile)
            #end with
            print("saved as json: " + month + "-tripdata.json")
            jsonfile.close()
        #end if
    #end for
    print("done: " + year)
#end for