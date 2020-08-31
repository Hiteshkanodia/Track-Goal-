# chainging html file to provide functionality of selecting two points
def change(file_name,final_name):
	fp = open("%s" %file_name,'r')
	fp1 = open("%s" %final_name,'w')

	for line in fp:
	    if line=="""		var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);\n""":
	    	fp1.write(line)
	        fp1.write("var lati = [];\nvar longi = [];\nvar i=0;\n")
	        fp1.write("google.maps.event.addListener(map,'click',function(event) {\n")
	        fp1.write("lati[i] =  event.latLng.lat();\n")
	        fp1.write("longi[i] = event.latLng.lng();\n")
	        fp1.write("if(i%2==0)\n")
	        fp1.write("{\n")
	        fp1.write("document.getElementById('la1').value = lati[i];\n")
	        fp1.write("document.getElementById('lo1').value =  longi[i];\n")
	        fp1.write("}\n")
	        fp1.write("else\n")
	        fp1.write("{\n")
	        fp1.write("document.getElementById('la2').value = lati[i];\n")
	        fp1.write("document.getElementById('lo2').value =  longi[i];\n")
	        fp1.write("}\n")
	        fp1.write("i = i+1;\n")
	        fp1.write("});\n")
	    elif line=="</body>\n":
	    	fp1.write("""<form action = "http://localhost:5000/trackmap/segment" method = "post" enctype="multipart/form-data">\n""")
	    	fp1.write("First Point:&nbsp &nbsp &nbsp &nbsp &nbsp\n")
	    	fp1.write("""<input id="la1" type="text" name="lati1">&nbsp &nbsp &nbsp &nbsp\n""")
	    	fp1.write("""<input id="lo1" type="text" name="longi1"><br>\n""")
	    	fp1.write("Second Point:&nbsp &nbsp &nbsp \n")
	    	fp1.write("""<input id="la2" type="text" name="lati2">&nbsp &nbsp &nbsp &nbsp\n""")
	    	fp1.write("""<input id="lo2" type="text" name="longi2"><br>\n""")
	    	fp1.write("""<input type="submit" value="Submit" >\n""")
	    	fp1.write("</form> \n")
	    	fp1.write("\n")
	    	fp1.write(line)
	    else:
	        fp1.write(line)


