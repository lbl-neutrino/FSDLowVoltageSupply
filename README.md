# FSDLowVoltageSupply
python code that controls the low voltage (lv) power supply for the charge readout system of Dune's Near Detector FSD's (Full Scale Detector) prototype. Instructions for connecting and controlling the power supply can be found in the link below

https://docs.google.com/document/d/1bcHnaWUtny-otrnCrakMsa6pT0x58ps5APOoRVoo058/edit?usp=sharing

# on_lv.py 
  turns on the low voltage power supply (Wiener PL506) and configures it to send power (24V) to the 4 pacman controllers

# monitor_lv.py 
  sends power supply information (voltage/current settings/outputs) to the slow control database (InfluxDB). This script is an endless loop that must be stopped with Control-C

# off_lv.py 
  turns off the low voltage power supply 
