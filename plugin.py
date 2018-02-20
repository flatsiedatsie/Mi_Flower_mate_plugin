"""
<plugin key="Mi_flower_mate" name="Xiaomi Mi Flower Mate" author="blauwebuis" version="1.0.0" wikilink="https://www.domoticz.com/wiki/Plugins/Mi_flower_mate" externallink="https://www.domoticz.com/forum/viewtopic.php?f=65&t=21567">
	<description>
		This plugin scans adds Mi Flower Mate flower sensors. It requires the BluePy library to be installed on the system.
	</description>
	<params>
		<param field="Address" label="Domoticz IP Address" width="200px" required="true" default="127.0.0.1"/>
		<param field="Port" label="Port" width="40px" required="true" default="8080"/>
		<param field="Mode1" label="Devices mac adresses, capitalised and comma separated" width="300px" required="true" default="C4:7C:8D:62:50:34"/>
	</params>
</plugin>
"""

bluepyError = 0

try:
	import Domoticz
except ImportError:
	import fakeDomoticz as Domoticz
#from subprocess import call
#import platform
#import os
#import subprocess
import time

import sys
#import urllib.request
#import base64
#import shelve
#from miflora.miflora_poller import MiFloraPoller, \
#	MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY
try:	
	from miflora.miflora_poller import MiFloraPoller, \
    	MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY
except:
	bluepyError = 1

try:
	from miflora.backends.bluepy import BluepyBackend
except:
	bluepyError = 1

class BasePlugin:

	def __init__(self):
		#self.platform = platform.system()	
		self.domoticzServer = "127.0.0.1"
		self.port = 8080
		#self.pollFrequency = 1
		#self.dirName = os.path.dirname(__file__)
		return 

	def onStart(self):
		Domoticz.Debugging(1)
	  
		sys.path.append('/home/dietpi/.local/lib/python3.4/site-packages/')
		#sys.path.append('/home/dietpi/domoticz/plugins/mi_flower_mate')
		#Domoticz.Log("Mi Flora - Domoticz IP = " + str(Parameters["Address"]))
		Domoticz.Log("loading error? = " + str(bluepyError))
		
		
		#path = 'the path you want'
		#os.environ['PATH'] += ':'+path
		
		#Domoticz.Log("current path = " + str(os.getcwd())
		#cwd = os.getcwd()
		
		self.domoticzServer=Parameters["Address"]
		self.port=Parameters["Port"]
		self.webPath=str(self.domoticzServer) + ":" + str(self.port)
		self.macs = parseCSV(Parameters["Mode1"])
		
		Domoticz.Debug("macs = {}".format(self.macs))
		
		#self.databaseFile=os.path.join(os.environ['HOME'],'flowermates')
		#self.flowermateDatabase = shelve.open(databaseFile)
		
		Domoticz.Log("Mi Flora - Domoticz IP = " + str(Parameters["Address"]))
		Domoticz.Log("Mi Flora - Domoticz port = " + str(Parameters["Port"]))
		Domoticz.Log("Mi Flora - Macs = " + str(Parameters["Mode1"]))
		Domoticz.Log("Mi Flora - devices made so far (max 255): " + str(len(Devices)))
#		Domoticz.Log("homefolder: " + str(HomeFolder))
		
		
		# create the listen-toggle-switch. This controls the making of new RF switches.
		if 1 not in Devices:
			Domoticz.Log("Creating the master Mi Flower Mate poll switch. Flip it to poll the sensors.")
			Domoticz.Device(Name="Flip to update Mi Flowermates", Unit=1, TypeName="Switch", Image=9, Used=1).Create()
		
		
		if len(Devices) == 1:
			Domoticz.Log("No Flora's exist yet")
			# Create the sensors. Later we get the data.
			for idx, mac in enumerate(self.macs):
				Domoticz.Log("Creating devices for mac: "+str(mac))
				sensorBaseName = "#" + str(idx) + " "

				#moisture

				sensorNumber = (idx*4) + 2
				sensorName = sensorBaseName + "Moisture"
				Domoticz.Log("Creating first sensor, #"+str(sensorNumber))
				Domoticz.Log("Creating first sensor, name: "+str(sensorName))
				Domoticz.Device(Name=sensorName, Unit=sensorNumber, TypeName="Percentage", Used=1).Create()   
				Domoticz.Log("Created device: "+Devices[sensorNumber].Name)
	#			moistureIdx = Devices[sensorNumber].ID

				#temperature

				sensorNumber = (idx*4) + 3
				sensorName = sensorBaseName + "Temperature"
				Domoticz.Device(Name=sensorName, Unit=sensorNumber, TypeName="Temperature", Used=1).Create()
				Domoticz.Log("Created device: "+Devices[sensorNumber].Name)
	#			temperatureIdx = Devices[sensorNumber].ID

				#light

				sensorNumber = (idx*4) + 4
				sensorName = sensorBaseName + "Light"
				Domoticz.Device(Name=sensorName, Unit=sensorNumber, TypeName="Illumination", Used=1).Create()
				Domoticz.Log("Created device: "+Devices[sensorNumber].Name)			
	#			lightIdx = Devices[sensorNumber].ID

				#fertility		

				sensorNumber = (idx*4) + 5
				sensorName = sensorBaseName + "Fertility"
				Domoticz.Device(Name=sensorName, Unit=sensorNumber, TypeName="Custom", Used=1).Create()
				Domoticz.Log("Created device: "+Devices[sensorNumber].Name)			
	#			fertilityIdx = Devices[sensorNumber].ID

				#self.getPlantData()
				# this tells the flowermate script where domoticz is (to communicate back), which Flowermate to poll, and which Domoticz sensors to then update. By doing an external call, Domoticz is nog slowed down by bluetooth time-outs and other issues.
	#			callCommand = "sudo " + str(sys.executable) + " " + str(self.dirName) + "/flowermate.py " + str(self.domoticzServer) + " " + str(self.port) + " " + str(mac) + " " + str(moistureIdx) + " " + str(temperatureIdx) + " " + str(lightIdx)  + " " + str(fertilityIdx)
	#			Domoticz.Log(str(callCommand))
	#			try:
	#				call (callCommand, shell=True)
	#			except:
	#				cloner = os.popen(callCommand).read()


	def onStop(self):
		Domoticz.Log("onStop called")

	def onConnect(self, Connection, Status, Description):
		Domoticz.Log("onConnect called")

	def onMessage(self, Connection, Data, Status, Extra):
		Domoticz.Log("onMessage called")

	def onCommand(self, Unit, Command, Level, Hue):
		Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))		
		
		#first, let's flip the switch.
		if str(Command) == "On":
			Devices[Unit].Update(nValue=1,sValue="On")
		if str(Command) == "Off":
			Devices[Unit].Update(nValue=0,sValue="Off")

		if Unit == 1:
			self.getPlantData()
	
	def onHeartbeat(self):
		pass

	
	def getPlantData(self): #,idx_moist,idx_temp,idx_lux,idx_cond
		for idx, mac in enumerate(self.macs):
			Domoticz.Log("getting data from sensor: "+str(mac))
			Domoticz.Log("BluepyBackend: "+str(BluepyBackend))
		 
			poller = MiFloraPoller(str(mac), BluepyBackend)
			#time.sleep(0.2)  
			Domoticz.Log("Poller started")
			#Domoticz.Log("Firmware: {}".format(poller.firmware_version()))
			#Domoticz.Log("Moisture:"+ str(poller.parameter_value(MI_MOISTURE)))
			
			val_bat  = poller.parameter_value(MI_BATTERY)
			#val_bat  = "{}".format(poller.parameter_value(MI_BATTERY))
			
			#moisture
			
			nValue = 0
			
			sensorNumber1 = (idx*4) + 2
			Domoticz.Log("moisture Device Id: "+str(sensorNumber1))
			val_moist = "{}".format(poller.parameter_value(MI_MOISTURE))
			Domoticz.Log(str(val_moist))
			Devices[sensorNumber1].Update(nValue=nValue, sValue=val_moist, BatteryLevel=val_bat)
			
			#temperature
			
			sensorNumber2 = (idx*4) + 3
			#temperatureIdx = Devices[sensorNumber].ID
			val_temp = "{}".format(poller.parameter_value("temperature"))
			Domoticz.Log(str(val_temp))
			Devices[sensorNumber2].Update(nValue=nValue, sValue=val_temp, BatteryLevel=val_bat)
			
			
			#light
			
			sensorNumber3 = (idx*4) + 4	
			val_lux = "{}".format(poller.parameter_value(MI_LIGHT))
			Domoticz.Log(str(val_lux))
			Devices[sensorNumber3].Update(nValue=nValue, sValue=val_lux, BatteryLevel=val_bat)
			#lightIdx = Devices[sensorNumber].ID
			
			#fertility		
		
			sensorNumber4 = (idx*4) + 5	
			#fertilityIdx = Devices[sensorNumber].ID
			val_cond = "{}".format(poller.parameter_value(MI_CONDUCTIVITY))
			Domoticz.Log(str(val_cond))
			Devices[sensorNumber4].Update(nValue=nValue, sValue=val_cond, BatteryLevel=val_bat)
			
			time.sleep(0.2)  
			#updateFlower(str(mac),sensorNumber1,sensorNumber2,sensorNumber3,sensorNumber4):
			
			# this tells the flowermate script where domoticz is (to communicate back), which Flowermate to poll, and which Domoticz sensors to then update. By doing an external call, Domoticz is nog slowed down by bluetooth time-outs and other issues.
#			callCommand = "sudo " + str(sys.executable) + " " + str(self.dirName) + "/flowermate.py " + str(self.webPath) + " " + str(mac) + " " + str(moistureIdx) + " " + str(temperatureIdx) + " " + str(lightIdx)  + " " + str(fertilityIdx)
#			Domoticz.Log(str(callCommand))
#			try:
#				call (callCommand, shell=True)
#			except:
#				cloner = os.popen(callCommand).read()


	
	
global _plugin
_plugin = BasePlugin()

def onStart():
	global _plugin
	_plugin.onStart()

def onStop():
	global _plugin
	_plugin.onStop()

def onCommand(Unit, Command, Level, Hue):
	global _plugin
	_plugin.onCommand(Unit, Command, Level, Hue)

def onHeartbeat():
	#pass
	global _plugin 
	_plugin.onHeartbeat()
	



def parseCSV(strCSV):
	listvals = []
	for value in strCSV.split(","):
		listvals.append(value)
	return listvals


