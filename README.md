# FSDLowVoltageSupply
python code that controls the low voltage (lv) power supply for the charge readout system of Dune's Near Detector FSD's (Full Scale Detector) prototype

# on_lv.py 
  turns on the low voltage power supply (Wiener PL506) and configures it to send power (24V) to the 4 pacman controllers

# monitor_lv.py 
  sends power supply information (voltage/current settings/outputs) to the slow control database (InfluxDB). This script is an endless loop that must be stopped with Control-C

# off_lv.py 
  turns off the low voltage power supply 
