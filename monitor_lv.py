########################################################################
# The Wiener PL506 power supply provides 24V to 4 CRS pacmans.
# This code monitors voltage/current settings and outputs, printing them
# to screen & sending them to a slow control InfluxDB account every 10s
########################################################################

import time

# os is used to issue system commands (in this case SNMP commands) via
# python code, as needed to initialize the Wiener PL506
import os

# subprocess is needed to assign SNMP command outputs to variables for 
# sending to InfluxDB
import subprocess

# influxDB is the database on labpix used by grafana to monitor controls
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# urllib3 has functions that will help with timeout url problems
import urllib3

#######################################################################
# Assign global variables
#######################################################################

# initialize values read from the power supply
voltage_set, current_set, voltage, current = 0.0, 0.0, 0.0, 0.0

# Identify InfluxDB account name (org), password (toden), InfluxDB portal
# (url), and tages for data (bucket, measurement and field)
ORG = "lhep"
URL = "http://130.92.128.162:8086"
bucket = "fsd_sc"
measurement = "lv-controls"
TOKEN = "a1gkXTPILBYrhxLFb56DN4zezih1qwliiER5DZB-wZOM3ahy50sbXX0QoCTqjo2V-lefgWQbu-PFKT6p-_Ugow=="

# create InfluxDB names
v1_label = "lv reading"
v2_label = "lv setting"
c1_label = "current reading"
c2_label = "current setting"

#######################################################################
# Initialize the Influx database
#######################################################################

# sign into InfluxDB
client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)

# prepare InfluxDB to accept data
write_api = client.write_api(write_options=SYNCHRONOUS)

#######################################################################
# main
#######################################################################

while(True): 

    # the subprocess commands aren't like the "os" commands. They 
	# require a set of arguments to be sent to the snmp command, hence 
	# the following change in format 
	snmp_cmd = ["snmpget", "-v", "2c", "-m+WIENER-CRATE-MIB", "-c", "public", "192.168.1.2", "outputVoltage.u0"]

	# the other arguments below are needed to capture the output in 
	# a variable instead of it going straight to the screen
	cmd_info = subprocess.run(snmp_cmd, check=False, capture_output=True)

	# various information results from the command, we're only interested
	# in the output (hence the "stdout"). Without the "decode", the command
	# would output ones and zeros. 
	output_string = cmd_info.stdout.decode()
	
	# the output string has a lot of information, we only need the voltage
	# which must be converted to an integer
	voltage_set = float(output_string[52:58])
	
	# follow the same steps for current
	snmp_cmd = ["snmpget", "-v", "2c", "-m+WIENER-CRATE-MIB", "-c", "public", "192.168.1.2", "outputCurrent.u0"]
	cmd_info = subprocess.run(snmp_cmd, check=False, capture_output=True)
	output_string = cmd_info.stdout.decode()
	current_set = float(output_string[52:58])

	# follow the same steps for measured voltage
	snmp_cmd = ["snmpget", "-v", "2c", "-m+WIENER-CRATE-MIB", "-c", "public", "192.168.1.2", "outputMeasurementSenseVoltage.u0"]
	cmd_info = subprocess.run(snmp_cmd, check=False, capture_output=True)
	output_string = cmd_info.stdout.decode()
	voltage = float(output_string[68:74])
		
	# follow the same steps for measured current
	snmp_cmd = ["snmpget", "-v", "2c", "-m+WIENER-CRATE-MIB", "-c", "public", "192.168.1.2", "outputMeasurementCurrent.u0"]
	cmd_info = subprocess.run(snmp_cmd, check=False, capture_output=True)
	output_string = cmd_info.stdout.decode()
	current = float(output_string[63:69])
	
	print(" ")
	print(f"Settings     {voltage_set:.4f} V      {current_set:.4f} A")
	print(f"Readings     {voltage:.4f} V      {current:.4f} A")

	# create data points to send to InfluxDB
	p1 = influxdb_client.Point(measurement).field(v1_label, voltage)
	p2 = influxdb_client.Point(measurement).field(v2_label, voltage_set)
	p3 = influxdb_client.Point(measurement).field(c1_label, current)
	p4 = influxdb_client.Point(measurement).field(c2_label, current_set)

	# push the points into the specified InfluxDB account
	try:
#		write_api.write(bucket=bucket, org=ORG, record=p1)
#		write_api.write(bucket=bucket, org=ORG, record=p2)
#		write_api.write(bucket=bucket, org=ORG, record=p3)
#		write_api.write(bucket=bucket, org=ORG, record=p4)
	except urllib3.exceptions.ReadTimeoutError:
		continue
		
	time.sleep(10)

