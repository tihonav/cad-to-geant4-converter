import sys
import ast

NVERTEXTRIANGLE = 3

"""
def str_to_float(text):
	try:
		return ast.literal_eval(text)
	except Exception, e:
		print "String to float conversion failed due to: "+str(e)
		print "To convert: ", text
		raise SystemExit

def float_to_str(val):
        return '{}'.format(val)
"""


def print_progress_bar(text,percentage):
	sys.stdout.write("\r%s %5.1f%%"%(text,percentage))
	sys.stdout.flush()
	if percentage==100.: print


	
def get_attr_value(attr_name,text):
	return text.split(attr_name+"=")[-1].strip().split()[0].replace("'","").replace('"','').split("/")[0]
	

def analysze_file(fname):
	f = open(fname,"rb")
	lines = f.readlines()
	
	# get vertices
	openpostag = False
	opentritag = False
	nlines = len(lines)
	iline  = 0
	positions = {}
	triangles = []
	positionnames = 0 # self-test
	positionx     = 0 # self-test
	positiony     = 0 # self-test
	positionz     = 0 # self-test
	verticesx     = 0 # self-test
	verticesy     = 0 # self-test
	verticesz     = 0 # self-test
	for l in lines:
		# print status
		print_progress_bar("Processing: "+fname,iline*100./nlines)
		iline+=1

		# open position tag
		linetrim = l.lower().replace(" ", "")
		if '<position' in linetrim: openpostag = True
		if '<triangular' in linetrim: opentritag = True
		line = reduce(lambda x,y: x+"="+y, [item.strip() for item in l.split("=")])


		# fill position attrs
		if openpostag:
			if "name=" in line: 
				posname = get_attr_value("name",line)
				positionnames+=1
			if "x=" in line: 
				posx = get_attr_value("x",line)
				positionx+=1
			if "y=" in line: 
				posy = get_attr_value("y",line)
				positiony+=1
			if "z=" in line: 
				posz = get_attr_value("z",line)
				positionz+=1

		# fill triangles
		if opentritag:
			if "vertex1=" in line: 
				vertex1 = get_attr_value("vertex1",line)
				verticesx+=1
			if "vertex2=" in line: 
				vertex2 = get_attr_value("vertex2",line)
				verticesy+=1
			if "vertex3=" in line: 
				vertex3 = get_attr_value("vertex3",line)
				verticesz+=1
			
			

		#close position tag 
		if openpostag and "/>" in linetrim: 
			positions[posname] = {
						"x": posx,		
						"y": posy,		
						"z": posz,		
						}
			openpostag = False

		# close triangle tag
		if opentritag and "/>" in linetrim:
			triangles.append({
					"vertex1":vertex1,
					"vertex2":vertex2,
					"vertex3":vertex3,
					})
			opentritag = False
	
	# finished processing input file
	f.close()

	# some parser validation code
	assert(len(positions.keys())==positionnames and 
		positionnames == positionx and 
		positionx == positiony and 
		positiony==positionz 
		)
	assert(len(triangles)==verticesx and 
		verticesx == verticesy and 
		verticesy == verticesz 
		)
	

	# create triangles
	foutname =  fname[:fname.rfind(".")].split("/")[-1]+".csv"
	fout = open(foutname,"w")
	ntriangles = len(triangles)
	itriangle  = 0
	print
	for triangle in triangles:
		# debug info
		print_progress_bar("Creating: "+foutname,itriangle*100./ntriangles)
		itriangle+=1

		# creating output line
		line = ""
		for i in xrange(1,NVERTEXTRIANGLE+1):
			vertex = positions[triangle['vertex%d'%i]]
			line+= " " + vertex["x"] + ", " + vertex["y"] + ", " + vertex["z"] + ","
		line = line[:line.rfind(",")].strip()+"\n"
		fout.write(line)
	fout.close()
	print 
			
		
	

		


		
		
# input files loop
def run():
	fnames = [f for f in sys.argv[1:] if ".gdml" in f.lower()]
	for fname in fnames:
		analysze_file(fname)

	
run()
	
#<position name="DAM_EQM_CornerAlu_v0" unit="mm" x="-402.4131" y="-442.1275" z="66.45833"/>
#<triangular vertex1="DAM_EQM_CornerAlu_v110466" vertex2="DAM_EQM_CornerAlu_v110467" vertex3="DAM_EQM_CornerAlu_v110468"/>
