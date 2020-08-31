import gpxpy 
import gpxpy.gpx 
import pandas as pd
import gmplot
from geopy.distance import geodesic 
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time as tm
import numpy as np
# import mysql.connector

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="pass"
# )
# array consist of data of all tracks
trck_latitude = []
trck_longitude = []
trck_elevation = []
trck_Time = []

trck_Total_elevation = []
trck_Total_distance = []
trck_Total_time = []
trck_max_altitude = []
trck_min_altitude = []
trck_Avg_speed = []

seg_Total_elevation = []
seg_Total_distance = []
seg_Total_time = []
seg_max_altitude = []
seg_min_altitude = []
seg_Avg_speed = []
files = []

seg_latitude = []
seg_longitude = []
seg_elevation = []
seg_time = []

points = ['#FF0000','#008000','#0000FF','#800080','#FF00FF']

# function to analyse segment data
def segment(lati1,longi1,lati2,longi2):
	del seg_Total_elevation[:]
	del seg_Total_distance[:]
	del seg_Total_time[:]
	del seg_min_altitude[:]
	del seg_max_altitude[:]
	del seg_Avg_speed[:]

	del seg_latitude[:]
	del seg_longitude[:]
	del seg_elevation[:]
	del seg_time[:]

	u = len(trck_latitude)
	v = 0
	while v<u:
		latitude = trck_latitude[v]
		longitude = trck_longitude[v]
		Time = trck_Time[v]
		elevation = trck_elevation[v]

		near_lat1 = 1
		near_lon1 = 1
		near_lat2 = 1
		near_lon2 = 1
		p = len(latitude)
		i = 1
		near_dist1 = 10000000
		near_dist2 = 10000000
		point1 = 0
		point2 = 0
		while i<p-1:
			a = (lati1, longi1)
			b = (lati2,longi2) 
			c = (latitude[i],longitude[i])
			dist1 = (geodesic(a,c).km)
			dist2 = (geodesic(b,c).km)
			if near_dist1>dist1:
				near_dist1 = dist1
				near_lat1 = latitude[i]
				near_lon1 = longitude[i]
				point1 = i
			if near_dist2>dist2:
				near_dist2 = dist2
				near_lat2 = latitude[i]
				near_lon2 = longitude[i]
				point2 = i
			i = i+1
		print(point1)
		print(point2)
		p1 = min(point1,point2)
		p2 = max(point1,point2)
		print(p1)
		print(p2)

		lati = []
		longi = []
		ele = []
		sec = []
		k = p1
		while k<=p2:
			lati.append(latitude[k])
			longi.append(longitude[k])
			sec.append(Time[k])
			ele.append(elevation[k])
			k = k+1

		seg_latitude.append(lati)
		seg_longitude.append(longi)
		seg_elevation.append(ele)
		seg_time.append(sec)

		# to plot data on google maps
		data = gmplot.GoogleMapPlotter(lati[0],longi[0],17)
		data.scatter(lati,longi,'#FF0000',size = 1, marker = False)
		data.plot(lati,longi, 'cornflowerblue', edge_width = 3.0)
		data.draw("templates/part.html")

		n = len(sec)
		td = sec[n-1] - sec[0]
		Total_time = int(round(td.total_seconds()))
		print(Total_time)

		alt_max = max(ele)
		alt_min = min(ele)
		ele = alt_max - alt_min
	   
		total_dist=0
		p = len(lati)
		i = 1
		while i<p-1:
			a = (lati[i], longi[i]) 
			b = (lati[i+1],longi[i+1])
			total_dist += (geodesic(a,b).km)
			i = i+1
		seg_Total_time.append(int(Total_time/60))
		seg_Total_elevation.append(ele)
		seg_Total_distance.append(total_dist)
		seg_min_altitude.append(alt_min)
		seg_max_altitude.append(alt_max)
		if Total_time!=0:
			seg_Avg_speed.append((total_dist*1000)/Total_time)
		else:
			seg_Avg_speed.append(2)
		v = v+1
		# return Total_time,alt_min,alt_max,ele,total_dist

# function to compare segments and plotting graphs
def compare_segments(tracks,attribute):
	total_trck = len(tracks)
	if attribute=="Total_Time":
		y = seg_Total_time
		y_pos = np.arange(len(files))
		print(y_pos)
		plt.bar(y_pos,y,align='center',alpha=0.8,width=0.1)
		plt.xticks(y_pos,files)
		plt.ylabel('Total time (in minutes)')
		plt.title("Total_time vs Track_Segments")

	elif attribute=="Total_Elevation":
		y = seg_Total_elevation
		y_pos = np.arange(len(files))
		plt.bar(y_pos,y,align='center',alpha=0.8,width=0.1)
		plt.xticks(y_pos,files)
		plt.ylabel('Total elevation (in metre)')
		plt.title("Total_elevation vs Track_Segments")
	elif attribute=="Average_Speed":
		y = seg_Avg_speed
		y_pos = np.arange(len(files))
		plt.bar(y_pos,y,align='center',alpha=0.8,width=0.1)
		plt.xticks(y_pos,files)
		plt.ylabel('Average_speed (in m/s)')
		plt.title("Average_Speed vs Track_Segments")

	else:
		i=0
		while i<total_trck:
			j = tracks[i]-1
			elevation = seg_elevation[j]
			Time = seg_time[j]
			latitude = seg_latitude[j]
			longitude = seg_longitude[j]
			distance = []
			time = []
			p = len(elevation)
			k = 0
			while k<=p-1:
				a = (latitude[0], longitude[0])
				b = (latitude[k],longitude[k])
				c = (geodesic(a,b).km)
				distance.append(c)
				k = k+1
			i = i+1
			if attribute=="Elevation":
				plt.plot(distance,elevation,label='%s'%files[i-1])
			elif attribute=="Time":
				u = len(Time)
				t = 0
				while t<=u-1:
					td = Time[t] - Time[0]
					td = int(round(td.total_seconds()/60))
					time.append(td)
					t = t+1
				plt.plot(distance,time,label='%s'%files[i-1])
		plt.xlabel('Distance(in km)')
		if attribute=="Elevation":
			plt.ylabel('Elevation(in metre)')
			plt.title('Distance Vs Elevation')
		elif attribute=="Time":
			plt.ylabel('Time(in minutes)')
			plt.title('Distance Vs Time')
		
		plt.grid(True)
		plt.legend()

	graph_name = "graph" + str(tm.time()) + ".png"
	for filename in os.listdir('static/'):
		if filename.startswith('graph'):  # not to remove other images
			os.remove('static/' + filename)
	plt.savefig('static/'+ graph_name,bbox_inches='tight')
	plt.close()
	name = "static/"+graph_name
	return name

# uploading gpx file and extracting data 
def trck(file_name):
	del trck_latitude[:]
	del trck_longitude[:]
	del trck_elevation[:]
	del trck_Time[:]
	del files[:]
	# extracting data
	for file in os.listdir('gps_data/'):
		latitude = []
		longitude = []
		elevation = []
		Time = []

		x_tag = file[:-4]
		files.append(x_tag)

		name = "gps_data/" + file
		gpx_file = open(name,'r')
		gpx = gpxpy.parse(gpx_file)
		for track in gpx.tracks:
			for segment in track.segments:
				for point in segment.points:
					for ex in point.extensions:
						latitude.append(point.latitude)
						longitude.append(point.longitude)
						elevation.append(point.elevation)
						Time.append(point.time)
		trck_latitude.append(latitude)
		trck_longitude.append(longitude)
		trck_elevation.append(elevation)
		trck_Time.append(Time)
	for file in os.listdir('gps_data/'):
		name = "gps_data/"+file
		os.remove(name)
	# plot = {'Latitude':latitude,'Longitude':longitude,'Elevation':elevation,'Time':Time}
	# df = pd.DataFrame(plot)
	# df.to_csv('file1.csv')
	no_of_trck = len(trck_latitude)
	print("hii")
	print(no_of_trck)
	print("hii")
	i = 0
	# plotting gps data on google maps
	data = gmplot.GoogleMapPlotter(latitude[0],longitude[0],17)
	while i < no_of_trck:
		latitude = trck_latitude[i]
		longitude = trck_longitude[i]
		elevation = trck_elevation[i]
		Time = trck_Time[i]
		data.scatter(latitude,longitude,'#000000',size = 1, marker = False)
		data.plot(latitude,longitude, '%s'%points[i], edge_width = 3.0)
		i = i+1
		if i==no_of_trck:
			data.draw("%s"%file_name)
	j = 0
	del trck_Total_elevation[:]
	del trck_Total_distance[:]
	del trck_Total_time[:]
	del trck_max_altitude[:]
	del trck_min_altitude[:]
	del trck_Avg_speed[:]
	while j < no_of_trck:
		latitude = trck_latitude[j]
		longitude = trck_longitude[j]
		elevation = trck_elevation[j]
		Time = trck_Time[j]

		n = len(Time)
		td = Time[n-1] - Time[0]
		Total_time = int(round(td.total_seconds()))

		alt_max = max(elevation)
		alt_min = min(elevation)
		ele = alt_max - alt_min
	   
		total_dist=0
		p = len(latitude)
		i = 0
		while i<p-1:
			a = (latitude[i], longitude[i]) 
			b = (latitude[i+1],longitude[i+1])
			total_dist += (geodesic(a,b).km)
			i = i+1
		total_dist = int(total_dist)
		trck_min_altitude.append(alt_min)
		trck_max_altitude.append(alt_max)
		trck_Total_time.append(int(Total_time/60))
		trck_Total_distance.append(total_dist)
		trck_Total_elevation.append(ele)
		if Total_time!=0:
			trck_Avg_speed.append((total_dist*1000)/Total_time)
		else:
			trck_Avg_speed.append(2)
		# print(trck_Total_distance)
		j = j+1
		s = len(trck_longitude)
		print(s)
		# return trck_Total_elevation,trck_min_altitude,trck_max_altitude,trck_Total_distance,trck_Total_time
# extracting track details of various tracks
def trckdetails(data_type,no):
	no = no-1
	print(data_type)
	if data_type=="Segments":
		return files[no],seg_Total_time[no],seg_min_altitude[no],seg_max_altitude[no],seg_Total_elevation[no],seg_Total_distance[no]
	else:
		return files[no],trck_Total_time[no],trck_min_altitude[no],trck_max_altitude[no],trck_Total_elevation[no],trck_Total_distance[no]

# analysing data and plotting graphs
def graphanalysis(tracks,attribute):
	total_trck = len(tracks)
	print("golu")
	if attribute=="Total_Time":
		y = trck_Total_time
		y_pos = np.arange(len(files))
		print(y_pos)
		plt.bar(y_pos,y,align='center',alpha=0.8,width=0.1)
		plt.xticks(y_pos,files)
		plt.ylabel('Total time (in minutes)')
		plt.title("Total_time vs Tracks")

	elif attribute=="Total_Elevation":
		y = trck_Total_elevation
		y_pos = np.arange(len(files))
		plt.bar(y_pos,y,align='center',alpha=0.8,width=0.1)
		plt.xticks(y_pos,files)
		plt.ylabel('Total elevation (in metre)')
		plt.title("Total_elevation vs Tracks")
	elif attribute=="Average_Speed":
		y = trck_Avg_speed
		y_pos = np.arange(len(files))
		plt.bar(y_pos,y,align='center',alpha=0.8,width=0.1)
		plt.xticks(y_pos,files)
		plt.ylabel('Average_speed (in m/s)')
		plt.title("Average_Speed vs Tracks")
	else:

		i=0
		while i<total_trck:
			j = tracks[i]-1
			elevation = trck_elevation[j]
			Time = trck_Time[j]
			latitude = trck_latitude[j]
			longitude = trck_longitude[j]
			distance = []
			time = []
			p = len(elevation)
			k = 0
			while k<=p-1:
				a = (latitude[0], longitude[0])
				b = (latitude[k],longitude[k])
				c = (geodesic(a,b).km)
				distance.append(c)
				k = k+1
			i = i+1
			if attribute=="Elevation":
				plt.plot(distance,elevation,label='%s'%files[i-1])
			elif attribute=="Time":
				u = len(Time)
				t = 0
				while t<=u-1:
					td = Time[t] - Time[0]
					td = int(round(td.total_seconds()/60))
					time.append(td)
					t = t+1
				plt.plot(distance,time,label='%s'%files[i-1])
		plt.xlabel('Distance(in km)')
		if attribute=="Elevation":
			plt.ylabel('Elevation(in metre)')
			plt.title('Distance Vs Elevation')
		elif attribute=="Time":
			plt.ylabel('Time(in minutes)')
			plt.title('Distance Vs Time')
		
		plt.grid(True)
		plt.legend()

	graph_name = "graph" + str(tm.time()) + ".png"
	for filename in os.listdir('static/'):
		if filename.startswith('graph'):  # not to remove other images
			os.remove('static/' + filename)
	plt.savefig('static/'+ graph_name,bbox_inches='tight')
	plt.close()
	name = "static/"+graph_name
	return name

