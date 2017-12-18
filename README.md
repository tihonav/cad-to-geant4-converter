### Table of Contents
**[Introduction](#introduction)**  
**[Prerequisits](#prerequisits)**  
**[Usage](#usage)**  
**[Materials](#materials)**  
**[Examples](#examples)**  
**[Note on preparation of STL file](#note-on-preparation-of-stl-file)**  


## Introduction

The tool performs conversion of CAD drawings into the GDML format (Geometry Decription Markup Language). GDML is the format used in particle-physics simulation packages, like GEANT4. Input files should be provided in stl format, which is supported by majority of CAD developer software. 

How it works:
As an input to the tool, a set of stl files is provided where each stl file represents a part of the geometry, corresponding to one single material (input_file_1.stl, input_file_2.stl, ...). The tool converts this set of .stl file into the GDML model in one step.
  


## Prerequisits:
 - python2.7 or higher 

##### Tested Operating Systems: 
 - Mac OS X
 - Linux

## Usage: 
```bash
python stl_gdml.py out_name  input_file_1.stl input_file_2.stl input_file_N.stl
```

This will create:
  - out_name.gdml       - top level gdml
  - input_file_1.gdml   
  - input_file_2.gdml  
  - input_file_N.gdml
    
Note, even if there is one input .stl file, two gdml files will be created:
  - out_name.gdml 
  - input_file_1.gdml  
  
## Materials

Material should be encoded in the stl file name. For instance, my_geometry_part_Aluminum.stl file will be parsed as made of aluminum. To display a full list of currently available materials see:
```bash
python stl_gdml.py --materials 
```
So far only basic materials are implemented. If not yet in the list, new materials can be added directly in the resulting gdml model following the example of already existing materials.


## Examples:

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

## Note on preparation of STL file

The STL model can be created out of CAD drawing (.step files) in most of contemproary CAD packages, for example in CATIA. However, one should keep in mind that the level of details in STL is configurable.

At least in CATIA there is a specific module to create stl file and user can choose the level of details to implement. Also, there you can "decimate" facettes if you original stl file is too detailed. You can find information about this module on the CAD site of CERN:

[CERN CAD Support](https://edms.cern.ch/ui/file/1519241/Last_released/1519241.pdf) 


In the table on page 4, you can see that the stl file of the same model can vary from 45 Kb to 10,419 kb depending on parameters you have chosen.
 
In a more general way, it is always beneficial to remove details in the geometry before tessellation like holes, chanfers, fillets. The impact on the stl final model size is far from being negligible.
