## Introduction

This is a light-weight tool for converting of CAD drawings into the GDML (geometry secription markup language). GDML is the format used by particle-physics simulation packages, like GEANT4. Input files should be provided in .stl format, which is supported by majority of CAD developing software, for example KATIA. 

The conversion of CAD geometry implies following steps: 
 - CAD engineer provides a model as a set of .stl files, where each .stl file represents one part of the geometry, corresponding to one single material (input_file_1.stl, input_file_2.stl, ...)
 - The tool converts a set of .stl file into the GDML model
  

NOTE: so far, a Vacuum materail is assigned to the volumes in the resulting GDML file. Proper materials can be then defined iside the gdml themselves by the user. It is planned to implement automatic (semi-automatic) assignment of material in the next revisions of this software.

## Prerequisits:
 - python2.7 or higher 

## Tested Operating Systems: 
 - Mac OS X
 - Linux

## Usage: 
```bash
python stl_gdml.py out_name  input_file_1.stl input_file_2.stl input_file_N.stl
```


## Examples:

### 1. Basic example - conversion from stl to gdml: 
Before running the example, download and unzip the project
```bash
cd cad-to-geant4-converter/Example
python ../stl_gdml.py test_model ./*.stl 
```

As a result, you will get a test_model.gdml file, which you can use as a GEANT4 geometry. If you take a look inside the test_model.gdml, you will find different sub-detector parts, each part corresponding to one intial .stl file.

### 2. Visualization of resulting model in GEANT4. 

This example shows how to load gdml model that you obtained after conversion in GEANT4. Running this example requires either GEANT4 installed on your computer, or having access to CERN lxplus machines. Instructions are given for the lxplus case. This example can be done independently of the first one.

 - Login to lxplus machine:
 ```bash
 ssh -XY yourcernmane@lxplus.cern.ch
 ```
 
 - Set up python2.7, GCC, GEANT4, xerces (required by GEANT4 gdml module) 
```bash
source /afs/cern.ch/work/a/andrii/public/GDML/setup_geant4_gdml_xerces.sh
```

![alt text](https://github.com/tihonav/cad-to-geant4-converter/blob/master/Data/VisualizationExample.png "Logo Title Text 1")
