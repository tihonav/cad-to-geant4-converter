# Introduction

This is a light-weight tool for converting of CAD drawings into the GDML (geometry secription markup language). GDML is the format used by particle-physics simulation packages, like GEANT4. Input files should be provided in .stl format, which is supported by majority of CAD developing software. 

The tool works as follows: 
 - A set of .stl files is provided from the CAD model, where each .stl file represents one part of the geometry, corresponding to one single material (input_file_1.stl, input_file_2.stl, ...)
 - The tool converts a set of .stl file into the GDML model
  


# Prerequisits:
 - python2.7 or higher 

# Tested Operating Systems: 
 - Mac OS X
 - Linux

# Usage: 
```bash
python stl_gdml.py out_name  input_file_1.stl input_file_2.stl input_file_N.stl
```
# Materials

Material should be encoded in the stl file name. For instance, my_geometry_part_Aluminum.stl file will be parsed as made of aluminum. To display a full list of currently available materials see:
```bash
stl_gdml.py --materials 
```
So far only basic materials are implemented. If not yet in the list, new materials can be added directly in the resulting gdml model following the example of already existing materials.


# Examples:

### 1. Basic example - conversion from stl to gdml: 
Before running the example, download and unzip the project
```bash
cd cad-to-geant4-converter/Example
python ../stl_gdml.py test_model ./*.stl 
```

As a result, you will get a test_model.gdml file, which you can use as a GEANT4 geometry. If you take a look inside the test_model.gdml, you will find different sub-detector parts, each part corresponding to one intial .stl file.

### 2. Visualization of resulting model in GEANT4. 

This example shows how to load and visualize in GEANT4 the gdml model that you obtained after conversion from stl. Running this example requires either GEANT4 installed on your computer, or having access to CERN lxplus. Instructions are given for the lxplus case. This example can be done independently of the first one.

 - Login to lxplus machine:
 ```bash
 ssh -XY yourcernlogin@lxplus.cern.ch
 ```
 
 - Set up python2.7, GCC, GEANT4, xerces (required by GEANT4 gdml module) 
 ```bash
 source /afs/cern.ch/work/a/andrii/public/GDML/setup_geant4_gdml_xerces.sh
 ```
 
 - Get and compile GEANT4 gdml example
 ```bash
 cp -r /afs/cern.ch/sw/lcg/external/geant4/9.6.p03/share/examples/extended/persistency/gdml/G01 ~/
 cd ~/G01
 make
 ```
 
 - Pick up example .stl model, put it into your home directory, and convert into gdml
 ```bash
 cp -r /afs/cern.ch/work/a/andrii/public/GDML/Example/IBL_MODULE_EXAMPLE ~/
 cd ~/IBL_MODULE_EXAMPLE
 python2.7 [path_to_cad_gdml_converter]/stl_gdml.py TEST ./*.stl
 ```
 
 - Get a nice GEANT4 visualization config file and put it where your model is, run visualization
 ```bash
 cp /afs/cern.ch/work/a/andrii/public/GDML/Example/vis.mac ./
 load_gdml TEST.gdml 
 ```
Finally you should be able to see your model as in the figure below:
![alt text](https://github.com/tihonav/cad-to-geant4-converter/blob/master/Data/VisualizationExample.png "Logo Title Text 1")
