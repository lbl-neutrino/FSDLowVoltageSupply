########################################################################
# This script turns on and initializes a Wiener PL506 power supply (which
# is used to provide 24V to 4 pacmans in the FSD's charge readout system`
########################################################################

# os is used to issue system commands (in this case SNMP commands) via
# python code, as needed to control the Wiener PL506
import os

#######################################################################
# Initialize the PL506 power supply
#######################################################################

# turn on the power supply using the following command & arguments
#    "snmpset" - snmp command to assign settings
#    "-v 2c" - version of SNMP understood by WIENER
#    "-m+WIENER-CRATE-MIB" - Wiener specific SNMP text file
# 	 "-c private" or "-c guru" - must be used in write commands
#	 "192.168.1.2" - ip address of the Wiener power supply
#    "sysMainSwitch" - SNMP command to turn on the supply
#    "i 1" - assigns an integer input of 1 (the "on" setting) 
cmd = "snmpset -v 2c -m+WIENER-CRATE-MIB -c private 192.168.1.2 sysMainSwitch.0 i 1"
os.system(cmd)

# turn on chosen channel. Five chanels are available, but only 1 will be
# used by FSD (channel 0) as indicated by 'u0' 
cmd = "snmpset -v 2c -m+WIENER-CRATE-MIB -c guru 192.168.1.2 outputSwitch.u0 i 1"
os.system(cmd)

# set the desired voltage (24.0V) on the chose channel(s)
cmd = "snmpset -v 2c -m+WIENER-CRATE-MIB -c guru 192.168.1.2 outputVoltage.u0 F 24.0"
os.system(cmd)

# set the desired current limit on the chose channel(s)
cmd = "snmpset -v 2c -m+WIENER-CRATE-MIB -c guru 192.168.1.2 outputCurrent.u0 F 15.0"
os.system(cmd)

# set minimum and maximum terminal and sense voltages
cmd = "snmpset -v 2c -m+WIENER-CRATE-MIB -c guru 192.168.1.2 outputSupervisionMinSenseVoltage.u0 F 0.0" 
os.system(cmd)
cmd = "snmpset -v 2c -m+WIENER-CRATE-MIB -c guru 192.168.1.2 outputSupervisionMaxSenseVoltage.u0 F 28.0"
os.system(cmd)
cmd = "snmpset -v 2c -m+WIENER-CRATE-MIB -c guru 192.168.1.2 outputSupervisionMaxTerminalVoltage.u0 F 28.0"
os.system(cmd)

# set the maximum current limit 
cmd = "snmpset -v 2c -m+WIENER-CRATE-MIB -c guru 192.168.1.2 outputSupervisionMaxCurrent.u0 F 15.5"
os.system(cmd)

# set what happens  when max/min are exceeded. "0" indicates "ignore the failure" 
cmd = "snmpset -v 2c -m+WIENER-CRATE-MIB -c guru 192.168.1.2 outputSupervisionBehaviour.u0 i 0"
os.system(cmd)

# a moderate regulation mode (indicated by the "1") is used for cables >1m in length. 
cmd = "snmpset -v 2c -m+WIENER-CRATE-MIB -c guru 192.168.1.2 outputRegulationMode.u0 i 1"
os.system(cmd)

