# cad-to-geant4-converter

This is a light-weight tool for converting of CAD drawings into the GDML (geometry secription markup language). GDML is the format used by particle-physics simulation packages, like GEANT4. Input files should be provided in .stl format, which is supported by majority of CAD developing software, for example KATIA. 

The conversion of CAD geometry implies following steps:
1) CAD engineer provides a model as a set of .stl files, where each .stl file represents one part of the geometry, corresponding to one single material (input_file_1.stl, input_file_2.stl, ...)
2) The tool converts a set of .stl file into the GDML model, which then can be used in e.g. GEANT4 simulations.

NOTE: so far, a Vacuum materail is assigned to the volumes in the resulting GDML file. Proper materials can be then defined iside the gdml themselves by the user. It is planned to implement automatic (semi-automatic) assignment of material in the next revisions of this software.




- Supported (tested) OS
 
  Mac OS X
  Linux


- Usage:

  python stl_gdml.py out_name  input_file_1.stl input_file_2.stl input_file_N.stl
