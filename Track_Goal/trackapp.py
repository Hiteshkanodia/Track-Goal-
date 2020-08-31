from flask import Flask, redirect, url_for, request,render_template
import cnvrt as m1
import chnghtml as m2
import os
import time
app = Flask(__name__,static_url_path='/static')

# start of the app
@app.route('/')
def log():
   return render_template('track.html')
# route to the app
@app.route('/try',methods = ['POST'])
def initial():
   return render_template('track.html')

@app.route('/second',methods = ['POST'])
def second():
	final_name = "static/"
	for filename in os.listdir('static/'):
		if filename.startswith('change'):
			final_name += filename
	return render_template('Map.html',file_name = final_name)

# plooting gps data on google map
@app.route('/trackmap',methods = ['POST'])
def TrackMap():
    data1 = request.files.getlist('data1')
    for file in data1:
    	dir1 = "gps_data/" + file.filename
    	file.save(dir1)
    file_name = "static/map" + str(time.time())+ "b.html"
    final_name = "static/change" + str(time.time())+ "b.html" 
    # deleting files to improve performance
    for filename in os.listdir('static/'):
         if filename.startswith('map'):
         	os.remove('static/' + filename)
         if filename.startswith('change'):
         	os.remove('static/' + filename)
    # Total_time,alt_min,alt_max,ele,total_dist = m1.trck(file_name)
    m1.trck(file_name)
    m2.change(file_name,final_name);
    print(final_name)
    return render_template('Map.html',file_name = final_name)
    # return render_template('Map.html',file_name = final_name,Total_time = Total_time,alt_min = alt_min,alt_max=alt_max,ele=ele,total_dist=total_dist)

# function to extract basic track details
@app.route('/trackdetails',methods = ['POST'])
def TrackDetails():
	data_type = request.form.get("type")
	trck_number = request.form.get("data")
	no = int(trck_number,10)
	trck_name,Total_time,alt_min,alt_max,ele,total_dist = m1.trckdetails(data_type,no)
	final_name = "static/"
	for filename in os.listdir('static/'):
		if filename.startswith('change'):
			final_name = final_name + filename

	return render_template('Map1.html',trck_name = trck_name,trck_number = trck_number,file_name = final_name,Total_time = Total_time,alt_min = alt_min,alt_max=alt_max,ele=ele,total_dist=total_dist)

# function to analyse data and plotting charts
@app.route('/graphanalysis',methods = ['POST'])
def GraphAnalysis():
	attribute = request.form.get("attribute")
	data = request.form.get("tracks")
	track = data.split()
	track = [int(i) for i in track]
	graph_name = m1.graphanalysis(track,attribute)
	return render_template('graph.html',graph_name=graph_name)

# function to compare segements of given data
@app.route('/compare_segments',methods = ['POST'])
def CompareSegments():
	attribute = request.form.get("attribute")
	data = request.form.get("tracks")
	track = data.split()
	track = [int(i) for i in track]
	graph_name = m1.compare_segments(track,attribute)
	return render_template('graph.html',graph_name=graph_name)

# plotting the segment part on google map
@app.route('/trackmap/segment',methods = ['POST'])
def Segment():
	lati1 = request.form['lati1']
	longi1 = request.form['longi1']
	lati2 = request.form['lati2']
	longi2 = request.form['longi2']
	m1.segment(lati1,longi1,lati2,longi2)
	return render_template('part.html')


if __name__ == '__main__':
   app.run(debug = True,threaded=True)