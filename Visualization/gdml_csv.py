import sys
import ast



def str_to_float(text):
	try:
		return ast.literal_eval(text)
	except Exception, e:
		print "String to float conversion failed due to: "+str(e)
		print "To convert: ", text
		raise SystemExit

	
def get_attr_value(attr_name,text):
	return text.split(attr_name+"=")[-1].strip().split()[0].replace("'","").replace('"','').split("/")[0]
	

def analysze_file(f):
	lines = f.readlines()
	
	# get vertices
	openpostag = False
	for l in lines:
		# open position tag
		linetrim = l.lower().replace(" ", "")
		if '<position' in linetrim: openpostag = True
		line = reduce(lambda x,y: x+"="+y, [item.strip() for item in l.split("=")])


		# fill position attrs
		if openpostag:
			if "name=" in line: name = get_attr_value("name",line)
			if "x=" in line: x = str_to_float(get_attr_value("x",line))
			if "y=" in line: y = str_to_float(get_attr_value("y",line))
			if "z=" in line: z = str_to_float(get_attr_value("z",line))
		
			
			

		#close position tag 
		if openpostag and "/>" in linetrim: openline = False


		
		
# input files loop
def run():
	fnames = [f for f in sys.argv[1:] if ".gdml" in f.lower()]
	for fname in fnames:
		f = open(fname,"rb")
		analysze_file(f)

	
run()
	
#<position name="DAM_EQM_CornerAlu_v0" unit="mm" x="-402.4131" y="-442.1275" z="66.45833"/>
