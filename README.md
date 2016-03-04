# cad-to-geant4-converter

This is a light-weight tool for converting of CAD drawings into the GDML (geometry secription markup language). GDML is the format used by particle-physics simulation packages, like GEANT4. Input files should be provided in .stl format, which is supported by majority of CAD developing software, for example KATIA. 

The conversion of CAD geometry implies following steps: 
 - CAD engineer provides a model as a set of .stl files, where each .stl file represents one part of the geometry, corresponding to one single material (input_file_1.stl, input_file_2.stl, ...)
 - The tool converts a set of .stl file into the GDML model
  

NOTE: so far, a Vacuum materail is assigned to the volumes in the resulting GDML file. Proper materials can be then defined iside the gdml themselves by the user. It is planned to implement automatic (semi-automatic) assignment of material in the next revisions of this software.

TESTED OS: Mac OS X, Linux

USAGE: python stl_gdml.py out_name  input_file_1.stl input_file_2.stl input_file_N.stl

EXAMPLE: 
 - cd Example
 - python stl_gdml.py test_model ./*.stl 
