# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv, json
from datetime import datetime

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
	['Divvy_Trips_2017_Q1.csv', '2017'],
	['Divvy_Trips_2017_Q2.csv', '2017'],
    ['Divvy_Trips_2017_Q3.csv', '2017']
    #['Divvy_Trips_2017_Q4.csv', '2017'],
	#['Divvy_Trips_2018_Q1.csv', '2018'],
	#['Divvy_Trips_2018_Q2.csv', '2018'],
    #['Divvy_Trips_2018_Q3.csv', '2018'],
    #['Divvy_Trips_2018_Q4.csv', '2018']
]

for f in data_files:
    year = f[1]
    if f[0][-6:-4] == "Q1":
		linksByOrigin = {year+'01': {}, year+'02': {}, year+'03': {}}
    elif f[0][-6:-4] == "Q2":
		linksByOrigin = {year+'04': {}, year+'05': {}, year+'06': {}}
    elif f[0][-6:-4] == "Q3":
		linksByOrigin = {year+'07': {}, year+'08': {}, year+'09': {}}
    elif f[0][-6:-4] == "Q4":
		linksByOrigin = {year+'10': {}, year+'11': {}, year+'12': {}}
    elif year == '2013':
		linksByOrigin = {
			year+'01': {}, year+'02': {}, year+'03': {},
			year+'04': {}, year+'05': {}, year+'06': {},
			year+'07': {}, year+'08': {}, year+'09': {},
			year+'10': {}, year+'11': {}, year+'12': {}
		}
    else:
		linksByOrigin = {year+f[0][-6:-4]: {}}
    with open(working_dir + "/trip_data/" + f[0], 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        print("read csv: " + f[0])
        for trip in reader:
            try:
                origin = int(trip['from_station_id'])
                destination = int(trip['to_station_id'])
            except ValueError:
                continue
            year = year
            try:
                month = str(datetime.strptime(trip['starttime'], '%m/%d/%Y %H:%M').month).zfill(2)
            except ValueError:
                try:
                    month = str(datetime.strptime(trip['starttime'], '%Y-%m-%d %H:%M').month).zfill(2)
                except ValueError:
                    try:
                        month = str(datetime.strptime(trip['starttime'], '%m/%d/%Y %H:%M:%S').month).zfill(2)
                    except ValueError:
                        print("ValueError 1")
                        continue
            except KeyError:
                try:
                    month = str(datetime.strptime(trip['start_time'], '%m/%d/%Y %H:%M').month).zfill(2)
                except ValueError:
                    try:
                        month = str(datetime.strptime(trip['start_time'], '%Y-%m-%d %H:%M').month).zfill(2)
                    except ValueError:
                        try:
                            month = str(datetime.strptime(trip['start_time'], '%Y-%m-%d %H:%M:%S').month).zfill(2)
                        except ValueError:
                            try:
                                month = str(datetime.strptime(trip['start_time'], '%m/%d/%Y %H:%M:%S').month).zfill(2)
                            except ValueError:
                                print("ValueError 2")
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
    csvfile.close()
    for month in linksByOrigin.keys():
        with open(working_dir + "/json_data/" + month + "-tripdata.json", "w") as jsonfile:
            #if len(linksByOrigin[month]) > 0:
            json.dump([linksByOrigin[month]], jsonfile)
        jsonfile.close()
        print("saved as json: " + month + "-tripdata.json")
    print("done: " + year)