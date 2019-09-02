"""
Author      : Andrii Tykhonov (andrii.tykhonov@cern.ch)
Description : A light-weight tool to convert CAD drawings 
              (.stl) into geant4 compatible format (.gdml)
"""

import ast
import sys
#import numpy as np
from bisect import bisect
import __main__

if int(sys.version_info.major)>=3:
	xrange = range

EMAIL         = "andrii.tykhonov@cernSPAMNOT.ch"
ERROR_CONTACT = "\nPlease contact %s for more information"%EMAIL

HEADER = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n'
SCHEMA = '<gdml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd">\n'
FOOTER = '</gdml>'


AUNIT  = 'deg'
LUNIT  = 'mm'

MATERIALS_INFO = '''

#@
#@  So far, following complex  materials are implemented:
#@       - Vacuum
#@       - Mechanic tructures
#@            - Aluminum
#@            - Honeycomb (Aluminum)
#@            - CarbonFibre
#@       - Adhesives
#@            - DC3140 (Glue, Dow Corning)
#@       - PCB 
#@            - FR4
#@            - Copper
#@            - Kapton
#@            - Gold
#@            - Nickel
#@            - Titanium
#@            - Silver
#@            - Palladium
#@            - Tin
#@            - Platinum
#@       - Detector materials: 
#@            - Silicon
#@            - CdTe
#@            - Tungsten
#@            - PMT
#@            - BGO
#@            - BC254 (neutron detector)
#@            - CdWO4 (cadmium tungstanate)
#@       - Others: 
#@            - Glass 
#@            - Lead
#@            - Q235 (Steel)
#@            - AL5052-H32 (Aluminium alloy)
#@            - Brass
#@            - FibrousGlass
#@            - PDMS: Polydimethylsiloxane (Silicon Rubber)
#@            - EpoxyResin
#@            - AlNO
#@            - SAC305
#@       
#@  Please contact the author to implement more materials, 
#@  or (and) feel free to implement them yourself
#@
'''

MATERIALS_LIST = [
	{"name" : "Vacuum",       "group" : "Other"},
	{"name" : "Aluminum",     "group" : "Mechanic tructures"},
	{"name" : "Honeycomb",    "group" : "Mechanic tructures"},
	{"name" : "CarbonFibre",  "group" : "Mechanic tructures"},
	{"name" : "DC3140",       "group" : "Adhesives"}, 
	{"name" : "FR4",          "group" : "PCB"},
	{"name" : "Copper",       "group" : "PCB"},
	{"name" : "Gold",         "group" : "PCB"},
	{"name" : "Nickel",       "group" : "PCB"},
	{"name" : "Titanium",     "group" : "PCB"},
	{"name" : "Silver",       "group" : "PCB"},
	{"name" : "Palladium",    "group" : "PCB"},
	{"name" : "Tin",          "group" : "PCB"},
	{"name" : "Platinum",     "group" : "PCB"},
	{"name" : "Silicon",      "group" : "Detector Elements"},
	{"name" : "CdTe",         "group" : "Detector Elements"},
	{"name" : "Tungsten",     "group" : "Detector Elements"},
	{"name" : "PMT",          "group" : "Detector Elements"},
	{"name" : "BGO",          "group" : "Detector Elements"},
	{"name" : "BC254",        "group" : "Detector Elements"},
	{"name" : "CdWO4",        "group" : "Detector Elements"},
	{"name" : "Glass",        "group" : "Other"},
	{"name" : "FibrousGlass", "group" : "Other"},
	{"name" : "PDMS",         "group" : "Other"},
	{"name" : "EpoxyResin",   "group" : "Other"},
	{"name" : "AlNO",         "group" : "Other"},
	{"name" : "SAC305",       "group" : "Other"},
	{"name" : "Lead",         "group" : "Other"},
	{"name" : "Q235",         "group" : "Other"},
	{"name" : "AL5052-H32",   "group" : "Other"},
	{"name" : "Brass",        "group" : "Other"},
]

MATERIALS = '''
    <materials>
        <!--          -->
        <!-- elements -->
        <!--          -->
        <!-- http://www-cdf.fnal.gov/~kirby/lbne_geo_tests/lbne_10kT_Materials.gdml -->
        <element name="videRef"    formula="VACUUM" Z="1"> <atom value="1."/>       </element>
        <element name="hydrogen"   formula="H"   Z="1">    <atom value="1.0079"/>   </element>
        <element name="carbon"     formula="C"   Z="6">    <atom value="12.0107"/>  </element>
        <element name="nitrogen"   formula="N"   Z="7">    <atom value="14.0067"/>  </element>
        <element name="oxygen"     formula="O"   Z="8">    <atom value="15.999"/>   </element>
        <element name="sodium"     formula="Na"  Z="11">   <atom value="22.99"/>    </element>
        <element name="magnesium"  formula="Mg"  Z="12">   <atom value="24.305"/>   </element>
        <element name="aluminum"   formula="Al"  Z="13">   <atom value="26.9815"/>  </element>
        <element name="silicon"    formula="Si"  Z="14">   <atom value="28.0855"/>  </element>
        <element name="phosphorus" formula="P"   Z="15">   <atom value="30.973"/>   </element>
        <element name="sulphur"    formula="S"   Z="16">   <atom value="32.065"/>   </element>
        <element name="argon"      formula="Ar"  Z="18">   <atom value="39.9480"/>  </element>
        <element name="potassium"  formula="K"   Z="19">   <atom value="39.0983"/>  </element>
        <element name="calcium"    formula="Ca"  Z="20">   <atom value="40.078"/>   </element>
        <element name="titanium"   formula="Ti"  Z="22">   <atom value="47.867"/>   </element>
        <element name="chromium"   formula="Cr"  Z="24">   <atom value="51.9961"/>  </element>
        <element name="manganese"  formula="Mn"  Z="25">   <atom value="54.9380"/>  </element>
        <element name="iron"       formula="Fe"  Z="26">   <atom value="55.8450"/>  </element>
        <element name="nickel"     formula="Ni"  Z="28">   <atom value="58.6934"/>  </element>
        <element name="copper"     formula="Cu"  Z="29">   <atom value="63.55"/>    </element>
        <element name="germanium"  formula="Ge"  Z="32">   <atom value="72.63"/>    </element>
        <element name="bromine"    formula="Br"  Z="35">   <atom value="79.904"/>   </element>
        <element name="palladium"  formula="Pd"  Z="46">   <atom value="106.42"/>   </element>
        <element name="tin"        formula="Sn"  Z="50">   <atom value="118.71"/>   </element>
        <element name="platinum"   formula="Pt"  Z="78">   <atom value="195.084"/>  </element>
        <element name="gold"       formula="Au"  Z="79">   <atom value="196.97"/>   </element>
        <element name="tungsten"   formula="W"   Z="74">   <atom value="183.84"/>   </element>
        <element name="bismuth"    formula="Bi"  Z="83">   <atom value="208.980"/>  </element>


        <!--                    -->
	<!-- composite elements -->
        <!--                    -->

        <isotope name="B10"  N="5" Z="5">   <atom unit="g/mole" value="10.0129369"/>  </isotope>
        <isotope name="B11"  N="6" Z="5">   <atom unit="g/mole" value="11.0093054"/>  </isotope>
        <element name="B">
            <fraction n="0.199" ref="B10"/>
            <fraction n="0.801" ref="B11"/>
        </element>

        <isotope name="Zn64"  N="34" Z="30">   <atom unit="g/mole" value="63.9291422"/>  </isotope>
        <isotope name="Zn66"  N="36" Z="30">   <atom unit="g/mole" value="65.9260334"/>  </isotope>
        <isotope name="Zn67"  N="37" Z="30">   <atom unit="g/mole" value="66.9271273"/>  </isotope>
        <isotope name="Zn68"  N="38" Z="30">   <atom unit="g/mole" value="67.9248442"/>  </isotope>
        <isotope name="Zn70"  N="40" Z="30">   <atom unit="g/mole" value="69.9253193"/>  </isotope>
        <element name="zink">
            <!-- see: https://en.wikipedia.org/wiki/Isotopes_of_zinc -->
            <fraction n="0.492" ref="Zn64"/>
            <fraction n="0.277" ref="Zn66"/>
            <fraction n="0.040" ref="Zn67"/>
            <fraction n="0.185" ref="Zn68"/>
            <fraction n="0.006" ref="Zn70"/>
        </element>

        <isotope name="Ag107"  N="60" Z="47">   <atom value="106.905092"/>   </isotope>
        <isotope name="Ag109"  N="62" Z="47">   <atom value="108.904756"/>   </isotope>
        <element name="silver">
                <!-- https://www.webelements.com/silver/isotopes.html -->
                <fraction n="0.51839" ref="Ag107"/>
                <fraction n="0.48161" ref="Ag109"/>
        </element>

        <isotope name="Sb121"  N="70" Z="51">   <atom value="120.9038157"/>   </isotope>
        <isotope name="Sb122"  N="71" Z="51">   <atom value="121.9051737"/>   </isotope>
        <element name="antimony">
                <!-- https://en.wikipedia.org/wiki/Isotopes_of_antimony -->
                <fraction n="0.572" ref="Sb121"/>
                <fraction n="0.428" ref="Sb122"/>
        </element>

        <isotope name="Cd106Cd" N="58" Z="48"> <atom unit="g/mole" value="105.906461"/>  </isotope>
        <isotope name="Cd108Cd" N="60" Z="48"> <atom unit="g/mole" value="107.904176"/>  </isotope>
        <isotope name="Cd110Cd" N="62" Z="48"> <atom unit="g/mole" value="109.903005"/>  </isotope>
        <isotope name="Cd111Cd" N="63" Z="48"> <atom unit="g/mole" value="110.904182"/>  </isotope>
        <isotope name="Cd112Cd" N="64" Z="48"> <atom unit="g/mole" value="111.902757"/>  </isotope>
        <isotope name="Cd113Cd" N="65" Z="48"> <atom unit="g/mole" value="112.904400"/>  </isotope>
        <isotope name="Cd114Cd" N="66" Z="48"> <atom unit="g/mole" value="113.903357"/>  </isotope>
        <isotope name="Cd116Cd" N="68" Z="48"> <atom unit="g/mole" value="115.904755"/>  </isotope>
        <element name="cadmium">
                <!-- isotopes taken in the natural abundance -->
                <!-- taken from https://www.webelements.com/cadmium/isotopes.html -->
                <fraction ref="Cd106Cd" n="0.0125"/>
                <fraction ref="Cd108Cd" n="0.0089"/>
                <fraction ref="Cd110Cd" n="0.1249"/>
                <fraction ref="Cd111Cd" n="0.1280"/>
                <fraction ref="Cd112Cd" n="0.2413"/>
                <fraction ref="Cd113Cd" n="0.1222"/>
                <fraction ref="Cd114Cd" n="0.2873"/>
                <fraction ref="Cd116Cd" n="0.0749"/>
        </element>

        <isotope name="Te120Te" N="68" Z="52"> <atom unit="g/mole" value="119.904048"/>  </isotope>
        <isotope name="Te122Te" N="70" Z="52"> <atom unit="g/mole" value="121.903050"/>  </isotope>
        <isotope name="Te123Te" N="71" Z="52"> <atom unit="g/mole" value="122.9042710"/>  </isotope>
        <isotope name="Te124Te" N="72" Z="52"> <atom unit="g/mole" value="123.9028180"/>  </isotope>
        <isotope name="Te125Te" N="73" Z="52"> <atom unit="g/mole" value="124.9044285"/>  </isotope>
        <isotope name="Te126Te" N="74" Z="52"> <atom unit="g/mole" value="125.9033095"/>  </isotope>
        <isotope name="Te128Te" N="76" Z="52"> <atom unit="g/mole" value="127.904463"/>  </isotope>
        <isotope name="Te130Te" N="78" Z="52"> <atom unit="g/mole" value="129.906229"/>  </isotope>
        <element name="tellurium">
                <!-- see https://www.webelements.com/tellurium/isotopes.html -->
                <fraction ref="Te120Te" n="0.0009"/>
                <fraction ref="Te122Te" n="0.0255"/>
                <fraction ref="Te123Te" n="0.0089"/>
                <fraction ref="Te124Te" n="0.0474"/>
                <fraction ref="Te125Te" n="0.0707"/>
                <fraction ref="Te126Te" n="0.1884"/>
                <fraction ref="Te128Te" n="0.3174"/>
                <fraction ref="Te130Te" n="0.3408"/>
        </element>

        <isotope name="Pb208" N="126" Z="82"> <atom unit="g/mole" value="207.9766521"/>  </isotope>
        <isotope name="Pb207" N="125" Z="82"> <atom unit="g/mole" value="206.9758969"/>  </isotope>
        <isotope name="Pb206" N="124" Z="82"> <atom unit="g/mole" value="205.9744653"/>  </isotope>
        <isotope name="Pb204" N="122" Z="82"> <atom unit="g/mole" value="203.9730430"/>  </isotope>
        <element name="lead">
                <!-- see https://en.wikipedia.org/wiki/Isotopes_of_lead -->
                <fraction ref="Pb208" n="0.524"/>
                <fraction ref="Pb207" n="0.221"/>
                <fraction ref="Pb206" n="0.241"/>
                <fraction ref="Pb204" n="0.014"/>
        </element>


    
        <!--          -->
        <!-- vacuum   -->
        <!--          -->
        <material formula=" " name="Vacuum">
            <D value="1.e-25" unit="g/cm3" />
            <fraction n="1.0" ref="videRef" />
        </material>



        <!--           -->
	<!-- materials -->
        <!--           -->

        <!-- FR4 submaterials -->

        <material name="EpoxyResin" formula="C38H40O6Br4">
            <D value="1.1250" unit="g/cm3"/>
            <composite n="38" ref="carbon"/>
            <composite n="40" ref="hydrogen"/>
            <composite n="6" ref="oxygen"/>
            <composite n="4" ref="bromine"/>
        </material>

        <material name="SiO2" formula="SiO2">
            <D value="2.2" unit="g/cm3"/>
            <composite n="1" ref="silicon"/>
            <composite n="2" ref="oxygen"/>
        </material>

        <material name="Al2O3" formula="Al2O3">
            <D value="3.97" unit="g/cm3"/>
            <composite n="2" ref="aluminum"/>
            <composite n="3" ref="oxygen"/>
        </material>

        <material name="Fe2O3" formula="Fe2O3">
            <D value="5.24" unit="g/cm3"/>
            <composite n="2" ref="iron"/>
            <composite n="3" ref="oxygen"/>
        </material>

       <material name="CaO" formula="CaO">
           <D value="3.35" unit="g/cm3"/>
           <composite n="1" ref="calcium"/>
           <composite n="1" ref="oxygen"/>
       </material>

       <material name="MgO" formula="MgO">
           <D value="3.58" unit="g/cm3"/>
           <composite n="1" ref="magnesium"/>
           <composite n="1" ref="oxygen"/>
       </material>

       <material name="Na2O" formula="Na2O">
           <D value="2.27" unit="g/cm3"/>
           <composite n="2" ref="sodium"/>
           <composite n="1" ref="oxygen"/>
       </material>

       <material name="TiO2" formula="TiO2">
           <D value="4.23" unit="g/cm3"/>
           <composite n="1" ref="titanium"/>
           <composite n="2" ref="oxygen"/>
       </material>

       <material name="FibrousGlass">
           <D value="2.74351" unit="g/cm3"/>
           <fraction n="0.600" ref="SiO2"/>
           <fraction n="0.118" ref="Al2O3"/>
           <fraction n="0.001" ref="Fe2O3"/>
           <fraction n="0.224" ref="CaO"/>
           <fraction n="0.034" ref="MgO"/>
           <fraction n="0.010" ref="Na2O"/>
           <fraction n="0.013" ref="TiO2"/>
       </material>

       <material name="FR4">
           <D value="1.98281" unit="g/cm3"/>
           <fraction n="0.47" ref="EpoxyResin"/>
           <fraction n="0.53" ref="FibrousGlass"/>
       </material>  
  
 
       <!-- Glue (DC3140, Dow Corning) sub materials -->
   
       <material name="dimethylsiloxane_hydroxy_terminated" formula="HOSiCH3CH3OH">
           <D value="0.98" unit="g/cm3"/>
           <composite n="2" ref="oxygen"/>
           <composite n="8" ref="hydrogen"/>
           <composite n="2" ref="carbon"/>
           <composite n="1" ref="silicon"/>
       </material>  
   
       <material name="trimethylated_silica" formula="O2Si">
           <D value="2.6" unit="g/cm3"/>
           <composite n="2" ref="oxygen"/>    
           <composite n="1" ref="silicon"/>
       </material>  
   
       <material name="methyltrimethoxysilane" formula="C4H12O3Si">
           <D value="0.955" unit="g/cm3"/>
           <composite n="3"  ref="oxygen"/>
           <composite n="12" ref="hydrogen"/>
           <composite n="4"  ref="carbon"/>
           <composite n="1"  ref="silicon"/>
       </material>
   
       <material name="DC3140">
           <D value="1.2" unit="g/cm3"/>
           <fraction n="0.60" ref="dimethylsiloxane_hydroxy_terminated"/>
           <fraction n="0.30" ref="trimethylated_silica"/>
           <fraction n="0.10" ref="methyltrimethoxysilane"/>    
       </material>  
   

      <!-- Conductive materials for PCB -->
   
      <material name="Copper" state="solid">
           <D value="8.960" unit="g/cm3"/>
           <fraction n="1." ref="copper"/>
      </material>
   
     <material name="Gold" state="solid">
           <D value="19.32" unit="g/cm3"/>
           <fraction n="1." ref="gold"/>
     </material>
   
   
     <material name="Nickel" state="solid">
           <D value="8.96" unit="g/cm3"/>
           <fraction n="1." ref="nickel"/>
     </material>

     <material name="Titanium" state="solid">
           <!--http://www.rsc.org/periodic-table/element/22/titanium -->
           <D value="4.506" unit="g/cm3"/>
           <fraction n="1." ref="titanium"/>
     </material>


     <material name="Silver" state="solid">
           <!-- see https://en.wikipedia.org/wiki/Silver -->
           <D value="10.49" unit="g/cm3"/>
           <fraction n="1." ref="silver"/>
     </material>

     <material name="Cadmium" state="solid">
           <!-- see https://www.lenntech.com/periodic/elements/cd.htm -->
           <D value="8.7" unit="g/cm3"/>
           <fraction n="1." ref="cadmium"/>
     </material>

     <material name="Palladium" state="solid">
           <!-- see http://www.rsc.org/periodic-table/element/46/palladium -->
           <D value="12.0" unit="g/cm3"/>
           <fraction n="1." ref="palladium"/>
     </material>

     <material name="Tin" state="solid">
           <!-- see http://www.rsc.org/periodic-table/element/50/tin -->
           <D value="7.287" unit="g/cm3"/>
           <fraction n="1." ref="tin"/>
     </material>

     <material name="Tellurium" state="solid">
           <!-- see http://www.rsc.org/periodic-table/element/52/tellurium -->
           <D value="6.232" unit="g/cm3"/>
           <fraction n="1." ref="tellurium"/>
     </material>

     <material name="Lead" state="solid">
           <!-- see https://en.wikipedia.org/wiki/Lead -->
           <D value="11.34" unit="g/cm3"/>
           <fraction n="1." ref="lead"/>
     </material>

     <material name="Q235" state="solid">  <!-- STEEL -->
           <!-- density, see: https://www.chinesesteelgrades.com/q235-steel/ -->
           <D value="7.85" unit="g/cm3"/>
           <fraction n="0.980" ref="iron"/>
           <fraction n="0.014" ref="manganese"/>
           <fraction n="0.004" ref="silicon"/>
           <fraction n="0.002" ref="carbon"/>
     </material>

     <material name="AL5052-H32" state="solid">  <!-- ALUMINUIM ALLOY -->
           <D value="2.68" unit="g/cm3"/>
           <fraction n="0.969" ref="aluminum"/>
           <fraction n="0.025" ref="magnesium"/>
           <fraction n="0.003" ref="iron"/>
           <fraction n="0.002" ref="chromium"/>
           <fraction n="0.001" ref="silicon"/>
     </material>

     <material name="Brass" state="solid"> <!-- brass: http://www.aatongdiao.com/en/new/new-73-571.html -->
           <D value="8.73" unit="g/cm3"/>
           <fraction n="0.61" ref="copper"/>
           <fraction n="0.39" ref="zink"/>
     </material>

     <material name="Platinum" state="solid">
           <!-- see http://www.rsc.org/periodic-table/element/78/platinum -->
           <D value="21.5" unit="g/cm3"/>
           <fraction n="1." ref="platinum"/>
     </material>


     <!-- Passivation -->

     <material name="AlNO" state="solid" formula="AlNO">
           <!-- Aluminum oxynitride -->
           <!-- see https://en.wikipedia.org/wiki/Aluminium_oxynitride -->
           <!-- see https://webbook.nist.gov/cgi/formula?ID=B1000046&Mask=800 -->
           <D value="3.6935" unit="g/cm3"/>
           <composite n="1" ref="aluminum"/>
           <composite n="1" ref="nitrogen"/>
           <composite n="1" ref="oxygen"/>
     </material>

     <!-- Bonding -->

     <material name="SAC305" state="solid">
           <!-- see https://www.aimsolder.com/sites/default/files/alloy_sac305_tds.pdf -->
           <!-- see https://cdn.sos.sk/productdata/73/d6/578230e0/sac305-sn96-5ag3cu0-5-0-7mm-1kg.pdf -->
           <D value="7.37" unit="g/cm3"/>
           <fraction n="0.965" ref="Tin"/>
           <fraction n="0.030" ref="Silver"/>
           <fraction n="0.005" ref="Copper"/>
     </material>


   
   
     <!-- Kapton -->
   
     <material name="Kapton" state="solid">
           <D value="1.42" unit="g/cm3"/>
           <fraction n="0.0273" ref="hydrogen"/>
           <fraction n="0.7213" ref="carbon"/>
           <fraction n="0.0765" ref="nitrogen"/>
           <fraction n="0.1749" ref="oxygen"/>
     </material>
   


      <!-- Aluminum, Hineycomb, Carbon fibre, etc. (simple materials) -->

      <material formula="Al" name="Aluminum" state="solid">
           <D value="2.700" unit="g/cm3"/>
           <fraction n="1." ref="aluminum"/>
      </material>
        
      <material name="CarbonFibre" state="solid">      
           <D unit="g/cm3" value="1.55"/>
           <fraction n="0.85" ref="carbon"/>      
           <fraction n="0.03" ref="hydrogen"/>      
           <fraction n="0.04" ref="nitrogen"/>
           <fraction n="0.08" ref="oxygen"/>
      </material>     

      <material name="Honeycomb" state="solid">
           <D value="0.030" unit="g/cm3"/>
           <fraction n="1." ref="aluminum"/>
      </material>

      <!-- Silicon -->
      <material name="Silicon" state="solid">
           <D value="2.333" unit="g/cm3"/>
           <fraction n="1." ref="silicon"/>
      </material>

      <!-- Tungsten -->
      <material name="Tungsten" state="solid">
          <D value="19.3" unit="g/cm3"/>
          <fraction n="1." ref="tungsten"/>
      </material> 

     <!-- Cadmium Telluride -->
     <material name="CdTe" state="solid">
           <!--https://www.azom.com/article.aspx?ArticleID=8408-->
           <D value="5.85" unit="g/cm3"/>
           <composite n="1" ref="cadmium"/>
           <composite n="1" ref="tellurium"/>
     </material>

      <!-- PMT -->
      <!--sylgard 170, Silicon Rubber Polydimethylsiloxane(PDMS)-->
      <material name="PDMS" formula="SiOC2H6" >
          <D value="1.34" unit="g/cm3" />
          <composite n="1" ref="silicon" />
          <composite n="1" ref="oxygen" />
          <composite n="2" ref="carbon" />
          <composite n="6" ref="hydrogen" />
      </material>

      <material name="Glass" formula="SiO2" >
          <D value="2.5" unit="g/cm3" />
          <composite n="1" ref="silicon" />
          <composite n="2" ref="oxygen" />
      </material>

      <material name="PMT" state="solid">
         <D value="2.524" unit="g/cm3"/>
         <fraction n="0.7" ref="aluminum"/>
         <fraction n="0.2" ref="Glass"/>
         <fraction n="0.1" ref="PDMS"/>
      </material>

      <!-- BGO -->
      <material name="BGO" formula="Bi4Ge3O12" >
         <D value="7.13" unit="g/cm3" />
         <composite n="4" ref="bismuth" />
         <composite n="3" ref="germanium" />
         <composite n="12" ref="oxygen" />
      </material>


     <!-- BC254 (neutron detector) -->
     <material name="BC254" state="solid">
        <MEE unit="eV" value="173"/>
        <D unit="g/cm3" value="1.026"/>
        <fraction n="0.2492" ref="carbon"/>
        <fraction n="0.7475" ref="hydrogen"/>
        <fraction n="0.0033" ref="B"/>
     </material>

     <!-- CdWO4 -->  
     <!-- see https://www.tandfonline.com/doi/pdf/10.1080/00223131.2008.10875862 -->
     <!-- see https://www.convertunits.com/molarmass/CdWO4 -->
     <material name="CdWO4" state="solid">
        <D unit="g/cm3" value="7.9"/>
        <fraction n="0.510" ref="tungsten"/>
        <fraction n="0.312" ref="cadmium"/>
        <fraction n="0.178" ref="oxygen"/>
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


    Materials:
 
            Material are encoded in the stl file name
            For instance, my_geometry_part_Aluminum.stl - this part will be parsed as made of aluminum
            See  %s --materials to display list of available materials
              
	
'''%(MODULE_NAME,MODULE_NAME,MODULE_NAME)






def __is_help__():
	ishelp = False 
	for arg in sys.argv:
		if "-h" in arg.lower() and arg[0]=="-": ishelp = True 
		if "help" in arg.lower(): ishelp = True
	if ishelp: print (HELP_MESSAGE)


def __print_error__(text):
	print (text)


def __print__(text):
	print (text)


def __print_progress_bar__(text,percentage):
	sys.stdout.write("\r%s %5.1f%%"%(text,percentage))
	sys.stdout.flush()
	if percentage==100.: print()


def __print_and_terminate__(text):
	__print_error__(text + " ==> terminating the program!")
	__print__(ERROR_CONTACT)
	raise SystemExit
	

def __str_to_float__(text):
	try:
		return ast.literal_eval(text)
	except Exception as e:
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


#def __get_orientation__(norm, vertex1, vertex2, vertex3):
#	v1 = np.array(vertex1)
#	v2 = np.array(vertex2)
#	v3 = np.array(vertex3)
#	vec1 = v2 - v1
#	vec2 = v3 - v2
#	norm1 = np.cross(vec1,vec2)
#	return 1 if np.inner(norm,norm1)>0 else -1

def __vectr_subtr__(vector1, vector2):
	return [x[0]-x[1] for x in zip(vector1,vector2)]

def __vector_cross__(vector1, vector2):
	return [
                  vector1[1]*vector2[2] - vector1[2]*vector2[1],
                - vector1[0]*vector2[2] + vector1[2]*vector2[0],
                  vector1[0]*vector2[1] - vector1[1]*vector2[0],
                        ]

def __vector_inner__(vector1,vector2):
	return sum([x[0]*x[1] for x in zip(vector1,vector2)])

def __get_orientation__(norm, v1, v2, v3):
	vec1 = __vectr_subtr__(v2, v1)
	vec2 = __vectr_subtr__(v3, v2)
	norm1 = __vector_cross__(vec1,vec2)
	return 1 if __vector_inner__(norm,norm1)>0 else -1

def __get_inputname_base__(fname):
	return fname.split("/")[-1].split(".stl")[0]


def get_triangles(fname):
	f=open(fname,"r")
	solid = None

	lines  = f.readlines()
	nlines = len(lines)
	for l in xrange(nlines):
		__print_progress_bar__("Processing file     %s: "%fname,100.*(l+1)/nlines)
		line = lines[l].lower()
	

		# start facet 
		if "facet " in line:
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


def guess_material(fname):
	target = fname.lower()
	materials = [m["name"] for m in MATERIALS_LIST if m["name"].lower() in target]
	if len(materials)>1:
		__print__("    Ambigous materials for file: %s:"%fname)
		[__print__("        %s"%x) for x in materials]
		__print__("        ... please specify name properly - assigning Vacuum to this volume!")
		return MATERIALS_LIST[0]["name"]
	elif not materials:
		__print__("    Could not parse material for the file %s: - asigning Vacuum to this volume!"%fname)
		return MATERIALS_LIST[0]["name"]
	
	__print__("    File %s - material parsed: %s"%(fname,materials[0]))
	return materials[0]

def stl_to_gdml(fname):
	outname = __get_inputname_base__(fname)
	outsolidname = outname+"-SOL"

	# sort vertices
	triangles = []
	sortedvertexes = []
	for triangle in get_triangles(fname):
		triangles.append(triangle)
		for vertex in triangle["vertex"]:
			x = __float_to_str__(vertex[0])
			y = __float_to_str__(vertex[1])
			z = __float_to_str__(vertex[2])
			thekey = x+y+z
			sortedvertexes.append(thekey)

	#__print__("Soring vertices - may take some time...")
	sortedvertexes = sorted(sortedvertexes)
	#__print__("... done sorting")

	# remove duplicates from verticves
	previous = None
	sortednoduplicates = []
	vertexidnoduplicates = []
	for tmpvertex in sortedvertexes:
		if tmpvertex == previous: continue
		sortednoduplicates.append(tmpvertex)
		vertexidnoduplicates.append(None)
		previous = tmpvertex
	
	# create gdml vertices
	# create gdml solids
	vertices = '\n    <define>\n'
	solids   = '\n    <solids>\n'
	solids  += '        <tessellated aunit="%s" lunit="%s" name="%s">\n'%(AUNIT,LUNIT,outsolidname)
	vertexid = 0
	for i in xrange(len(triangles)):
		triangle = triangles[i]
		__print_progress_bar__("generating gdml for %s: "%fname,100.*(i+1)/len(triangles))
		if len(triangle["vertex"])!=3:
			__print_and_terminate__("Illegal number of vertices per triangle: "+str(triangle["vertex"]))
		ids = []
		for vertex in triangle["vertex"]:
			x = __float_to_str__(vertex[0])
			y = __float_to_str__(vertex[1])
			z = __float_to_str__(vertex[2])
			thekey = x+y+z
			theitem = bisect(sortednoduplicates, thekey)-1
			assert(theitem>=0)
			# add vertex to gdml
			if vertexidnoduplicates[theitem] is None: 
				vertices+='        <position name="%s_v%d" unit="%s" x="%s" y="%s" z="%s"/>\n'%	(outname,
														vertexid,
														LUNIT,
														x,
														y,
														z
														) 
				vertexidnoduplicates[theitem] = vertexid
				vertexid+=1
			#  add vertex to facet
			ids.append(vertexidnoduplicates[theitem])

		# create facet
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

	# material
	material = guess_material(fname) # "Vacuum"


	# structure
	structure = STRUCTURE%(outname, material, outsolidname,"")

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
	outname = outname+".gdml"
	fout = open(outname,"w")
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
if "--materials" in sys.argv:
	__print__(MATERIALS_INFO)
	raise SystemExit
if len(sys.argv)<3:
	__print__('Not enough argumnets provided! see  "python %s -h" for more details'%MODULE_NAME)
	raise SystemExit
matchnames = [item for item in sys.argv[2:] if sys.argv[1].lower().split('.gdml')[0] == item.lower().split('.stl')[0]]
if matchnames:
	__print__('[out_name] should not coincide with one of the input .stl file names  "python %s -h" for more details'%MODULE_NAME)
	__print__('[out_name] = ' + sys.argv[1] + ' mathces with ' + matchnames[0] + ' - please use different name for the [out_name], for example "top.gdml"')
	raise SystemExit
if ".stl" in sys.argv[1]:
	__print__('Please provide output file name! see  "python %s -h" for more details'%MODULE_NAME)
	raise SystemExit
creat_gdml_bundle(sys.argv[1].split('.gdml')[0],sys.argv[2:])
	
	
	
