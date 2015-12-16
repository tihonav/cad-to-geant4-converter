"""
Author:      Andrii Tykhonov (andrii.tykhonov@cern.ch)
Describtion: a light-weight tool to convert CAD drawings 
             (.stl) into geant4 compatible format (.gdml)
"""

import ast
import sys
import numpy as np
import __main__

EMAIL         = "andrii.tykhonov@cernSPAMNOT.ch"
ERROR_CONTACT = "\nPlease contact %s for more information"%EMAIL

HEADER = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n'
SCHEMA = '<gdml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd">\n'
FOOTER = '</gdml>'


AUNIT  = 'deg'
LUNIT  = 'mm'



MATERIALS = '''
    <materials>

        <element name="aluminum" formula="Al" Z="13"> 
            <atom value="26.98"/>   
        </element>
    
        <element name="carbon" formula="C" Z="6"> 
            <atom value="12.01"/>   
        </element>

        <material formula="Al" name="Aluminum" state="solid">
            <D value="2.700" unit="g/cm3"/>
            <fraction n="1." ref="aluminum"/>
        </material>
        
        <material name="CarbonFibre" state="solid">      
            <D unit="g/cm3" value="0.145"/>
            <fraction n="1.0" ref="carbon"/>      
        </material>     
  
        <!--Vacuum-->
        <element name="videRef" formula="VACUUM" Z="1">
            <atom value="1."/>
        </element>
        <material formula=" " name="Vacuum">
            <D value="1.e-25" unit="g/cm3" />
            <fraction n="1.0" ref="videRef" />
        </material>
    
    </materials>
'''


WORLD = '''
    <setup name="Default" version="1.0">
        <world ref="%s"/>
    </setup>
'''

STRUCTURE = '''
    <structure>
        <volume name="%s">
            <materialref ref="%s"/>
            <solidref ref="%s"/>%s
        </volume>
    </structure>
'''

MODULE_NAME  = __main__.__file__.split("/")[-1].split("\\")[-1] 
HELP_MESSAGE = ''' 

    Usage: 
            python  %s  out_name  input_file_1.stl input_file_2.stl  input_file_N.stl"

            or

            python  %s  out_name  path_to_stl_file/blah_blah_*.stl
	
'''%(MODULE_NAME,MODULE_NAME)






def __is_help__():
	ishelp = False 
	for arg in sys.argv:
		if "-h" in arg.lower() and arg[0]=="-": ishelp = True 
		if "help" in arg.lower(): ishelp = True
	if ishelp: print HELP_MESSAGE


def __print_error__(text):
	print text


def __print__(text):
	print text


def __print_progress_bar__(text,percentage):
	sys.stdout.write("\r%s %5.1f%%"%(text,percentage))
	sys.stdout.flush()
	if percentage==100.: print


def __print_and_terminate__(text):
	__print_error__(text + " ==> terminating the program!")
	__print__(ERROR_CONTACT)
	raise SystemExit
	

def __str_to_float__(text):
	try:
		return ast.literal_eval(text)
	except Exception, e:
		__print_and_terminate__("String to float conversion failed due to: "+str(e))

def __float_to_str__(val):
	return '{}'.format(val)
		
def __get_three_values__(line, delimiter):
	vals = line.split(delimiter)[-1]
	vals = vals.split()
	if len(vals)!=3:
		#print 
		#print delimiter
		#print vals
		__print_and_terminate__("Input format inconsistency: more than 3 values per line: "+line)
	return [__str_to_float__(val) for val in vals]


def __get_orientation__(norm, vertex1, vertex2, vertex3):
	v1 = np.array(vertex1)
	v2 = np.array(vertex2)
	v3 = np.array(vertex3)
	vec1 = v2 - v1
	vec2 = v3 - v2
	norm1 = np.cross(vec1,vec2)
	return 1 if np.inner(norm,norm1)>0 else -1
	

def __get_inputname_base__(fname):
	return fname.split("/")[-1].split(".stl")[0]


def get_triangles(fname):
	f=open(fname,"r")
	solid = None

	lines  = f.readlines()
	nlines = len(lines)
	for l in xrange(nlines):
		__print_progress_bar__("Processing file %s: "%fname,100.*(l+1)/nlines)
		line = lines[l].lower()
	

		# start facet 
		if " facet " in line:
			solid = {}

		# Get normal to triangle
		if "normal" in line:
			if "normal" in solid.keys():
				__print_and_terminate__("Input format inconsistency: duplicate normal for triangle")
			solid["normal"] = __get_three_values__(line, "normal")
			continue


		# Get vertices
		if "vertex" in line:
			if "vertex" not in solid:
				solid["vertex"] = []
			if len(solid["vertex"])>=3:
				__print_and_terminate__("Input format inconsistency: more than 3 vertices per triangle")
			solid["vertex"].append(__get_three_values__(line,"vertex"))
			continue


		# Finalize the triangle
		if "endfacet" in line:
			yield solid



def stl_to_gdml(fname):
	outname = __get_inputname_base__(fname)
	outsolidname = outname+"-SOL"



	# get body
	vertices = '\n    <define>\n'
	solids   = '\n    <solids>\n'
	solids  += '        <tessellated aunit="%s" lunit="%s" name="%s">\n'%(AUNIT,LUNIT,outsolidname)
	vertexid = 0
	for triangle in get_triangles(fname):
		if len(triangle["vertex"])!=3:
			__print_and_terminate__("Illegal number of vertices per triangle: "+str(triangle["vertex"]))
		ids = []
		for vertex in triangle["vertex"]:
			vertices+='        <position name="%s_v%d" unit="%s" x="%s" y="%s" z="%s"/>\n'%	(outname,
													vertexid,
													LUNIT,
													__float_to_str__(vertex[0]),
													__float_to_str__(vertex[1]),
													__float_to_str__(vertex[2])
													) 
			ids.append(vertexid)
			vertexid+=1

		orientation = __get_orientation__(triangle["normal"], *triangle["vertex"])
		idsforsolid = ids if orientation>0 else [ids[2],ids[1],ids[0]]
		solids+= '             <triangular vertex1="%s_v%d" vertex2="%s_v%d" vertex3="%s_v%d"/>\n'%(outname, idsforsolid[0],
													outname, idsforsolid[1],
													outname, idsforsolid[2]
													)
	
	# finalize 
	vertices+= '    </define>\n'
	solids+=   '        </tessellated>\n'
	solids+=   '    </solids>\n'


	# structure
	structure = STRUCTURE%(outname,"Vacuum", outsolidname,"")

	# world
	world = WORLD%outname
	

	
	# create output gdml file
	outfilename = outname+".gdml"
	fout = open(outfilename,"w")
	fout.write(HEADER)
	fout.write(SCHEMA)
	#fout.write(MATERIALS)
	fout.write(vertices)
	fout.write(solids)
	fout.write(structure)
	fout.write(world)
	fout.write(FOOTER)
	fout.close()
	return outfilename
					 									

def creat_gdml_bundle(outname, infiles):
	# some world constants
	WORLD_BOX_SIZE = __float_to_str__(10000.)
	SOLIDNMAE  = "world_solid"
	VOLUMENAME = "world_volume"

	# solids
	solid  = '\n    <solids>\n'
	solid += '        <box lunit="%s" name="%s" x="%s" y="%s" z="%s" />\n'%(LUNIT,SOLIDNMAE,WORLD_BOX_SIZE,WORLD_BOX_SIZE,WORLD_BOX_SIZE)
	solid += '    </solids>\n'

	# structure 
	includes  = "\n\n"
	for fname in infiles:
		gdmlname = stl_to_gdml(fname)
		includes += '            <physvol>\n'
		includes += '                <file name="%s"/>\n'%gdmlname
		#includes += '                <position name="stk_corner_bolts_pos" x="stk_adjust_x_position" y="stk_adjust_y_position" z="stk_adjust_z_position" unit="mm"/>'
		#includes += '                <rotationref ref="old_to_new_coordinatesystem_rotation" />'
		includes += '             </physvol>\n'

	includes += "\n"
	structure = STRUCTURE%(VOLUMENAME,"Vacuum", SOLIDNMAE,includes)

	# world
	world = WORLD%VOLUMENAME


	# create top level gdml file
	fout = open(outname+".gdml","w")
	fout.write(HEADER)
	fout.write(SCHEMA)
	fout.write(MATERIALS)
	fout.write(solid)
	fout.write(structure)
	fout.write(world)
	fout.write(FOOTER)
	fout.close()
	
		

#__is_help__()
#stl_to_gdml(sys.argv[1])


__is_help__()
if len(sys.argv)<3:
	__print__('Not enough argumnets provided! see  "python %s -h" for more details'%MODULE_NAME)
	raise SystemExit
creat_gdml_bundle(sys.argv[1],sys.argv[2:])
	
	
	
