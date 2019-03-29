# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv, json, urllib2
from datetime import datetime

working_dir = r'C:\Users\eebinger\Desktop\FordGoBike_Trips\docs'
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
    '201806-fordgobike-tripdata.csv'#,
    #'201807-fordgobike-tripdata.csv',
    #'201808-fordgobike-tripdata.csv',
    #'201809-fordgobike-tripdata.csv',
    #'201810-fordgobike-tripdata.csv',
	#'201811-fordgobike-tripdata.csv',
	#'201812-fordgobike-tripdata.csv',
	#'201901-fordgobike-tripdata.csv',
	#'201902-fordgobike-tripdata.csv'
]
gbfs_stations = r'https://gbfs.fordgobike.com/gbfs/en/station_information.json'
gbfs_regions = r'https://gbfs.fordgobike.com/gbfs/en/system_regions.json'

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
            try:
                origin = trip['start_station_id']
            except ValueError:
                continue
            #end try
            destination = trip['end_station_id']
            if origin not in linksByOrigin:
                linksByOrigin[origin] = []
            #end if
            links = linksByOrigin[origin]
            if [origin, destination] in od_pairs:
                for x in links:
                    if x['source']==origin and x['target']==destination:
                        x['count'] += 1
                        #x['avg_duration'] += int(trip['tripduration'])
                        #x['avg_age'] += year-int(trip['birth year']) if is_number(trip['birth year']) else 0
                        #x['pct_female'] += float(trip['gender'])-1.0 if is_number(trip['birth year']) else 0
                        #x['count_demog'] += 1 if is_number(trip['birth year']) else 0
                        #x['pct_subscriber'] += 1 if trip['usertype']=='Subscriber' else 0
                    #end if
                #end for
            elif [origin, destination] not in od_pairs:
                links.append({
                    'source': origin, 
                    'target': destination,
                    'count': 1#,
                    #'avg_duration': int(trip['tripduration']),
                    #'avg_age': year-int(trip['birth year']) if is_number(trip['birth year']) else 0,
                    #'pct_female': float(trip['gender'])-1.0 if is_number(trip['birth year']) else 0,
                    #'count_demog': 1 if is_number(trip['birth year']) else 0,
                    #'pct_subscriber': 1 if trip['usertype']=='Subscriber' else 0
                })
                od_pairs.append([origin, destination])
            #end if
        #end for
    #end with
    csvfile.close()
    """
    # get average values within linksByOrigin
    for key in linksByOrigin.keys():
        for x in linksByOrigin[key]:
            x['avg_duration'] = x['avg_duration']/x['count']
            x['avg_age'] = x['avg_age']/x['count_demog'] if x['count_demog'] > 0 else x['avg_age']
            x['pct_female'] = x['pct_female']/x['count_demog'] if x['count_demog'] > 0 else x['pct_female']
            x['pct_subscriber'] = x['pct_subscriber']/x['count']
            del x['count_demog']
        #end for
    #end for
    """
    with open(working_dir + "/json_data/" + f[:6] + "-tripdata.json", "w") as jsonfile:
        json.dump([linksByOrigin], jsonfile)
    jsonfile.close()
    print("saved as json: " + f[:6] + "-tripdata.json")
#end for