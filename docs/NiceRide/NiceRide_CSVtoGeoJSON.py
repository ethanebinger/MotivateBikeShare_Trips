# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 14:38:02 2019

@author: eebinger
"""

import csv
#import datetime as datetime
#import arcpy
#import gdaltools

working_dir = r'C:\Users\eebinger\Desktop\MotivateBikeShare_Trips\docs\NiceRide'
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

for f in data_files:
    # collect stations
    stations = []
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
    station_dict = {}
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
    
    # write to CSV
    with open(working_dir+"/geojson_data/stations_"+f[:6]+".csv", "wb") as csv_file:
        writer = csv.writer(csv_file)
        #data_files_trunc = [x[:6] for x in data_files]
        writer.writerow(["station_id", "name", "lat", "lon"])
        for s in stations:
            writer.writerow([s, station_dict[s]["name"], station_dict[s]["lat"], station_dict[s]["lon"]])
        #end for
    #end with
	csv_file.close()
	"""
	# create XY layer
	lyr_name = "stations_"+f[:6]
	arcpy.MakeXYEventLayer_management(
		table="//tsclient/C/Users/eebinger/Desktop/FordGoBike_Trips/docs/geojson_data/"+lyr_name+".csv",
		in_x_field="lon",
		in_y_field="lat",
		out_layer=lyr_name,
		spatial_reference="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision",
		in_z_field="#"
	)

	# export feature layer to shapefile
	arcpy.FeatureClassToShapefile_conversion(lyr_name, "//tsclient/C/Users/eebinger/Desktop/FordGoBike_Trips/docs/geojson_data")
	"""
    """
    # convert shapefile to geojson
    ogr = gdaltools.ogr2ogr()
    ogr.set_encoding("UTF-8")
    ogr.set_input(working_dir+"/geojson_data/stations_"+f[:6]+".shp", srs="EPSG:4326")
    ogr.set_output(working_dir+"/geojson_data/stations_"+f[:6]+".geojson")
    ogr.execute()
    """
#end for

