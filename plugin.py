"""
<plugin key="Mi_flower_mate" name="Xiaomi Mi Flower Mate" author="blauwebuis" version="1.0.0" wikilink="https://www.domoticz.com/wiki/Plugins/Mi_flower_mate" externallink="https://www.domoticz.com/forum/viewtopic.php?f=65&t=22281">
	<description>
		This plugin connects to Mi Flower Mate flower sensors over Bluetooth LE. It requires the BluePy library to be installed on the system.
	</description>
	<params>
	    <param field="Mode1" label="Device selection" width="300px" required="true">
            <options>
                <option label="Automatic scanning" value="auto" default="true"/>
                <option label="Manual selection (add below)" value="manual"/>
            </options>
        </param>
		<param field="Mode2" label="Devices mac adresses, capitalised and comma separated" width="300px" required="false" default=""/>
	</params>
</plugin>
"""

bluepyError = 0

try:
	import Domoticz
except ImportError:
	import fakeDomoticz as Domoticz
import time
import sys
import shelve
import os
from miflora import miflora_scanner, BluepyBackend
import miflora
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
		self.macs = []
		self.currentlyPolling = 100
		return 

	def onStart(self):
		#Domoticz.Debugging(1)
		
		sys.path.append("/usr/local/lib/python3.4/dist-packages")
		sys.path.append("/usr/local/lib/python3.5/dist-packages")
	   
		if bluepyError == 1:
			Domoticz.Error("Error loading Flora libraries")
		
		
		Domoticz.Debug("Mi Flora - devices made so far (max 255): " + str(len(Devices)))
		
		# create custom icons
		if "Mi-Flower-Mate" not in Images:
			Domoticz.Log("Creating custom icon for the master Mi Flower Mate poll switch")
			Domoticz.Image(Filename="Mi-Flower-Mate.zip").Create()

		if ("Mi-Flower-Mate-Light" not in Images):
			Domoticz.Log("Creating custom icon for the master Mi Flower Mate light switch")
			Domoticz.Image(Filename="Mi-Flower-Mate-Light.zip").Create()

		if ("Mi-Flower-Mate-Moist" not in Images):
			Domoticz.Log("Creating custom icon for the master Mi Flower Mate moisture switch")
			Domoticz.Image(Filename="Mi-Flower-Mate-Moist.zip").Create()

		if ("Mi-Flower-Mate-Temp" not in Images):
			Domoticz.Log("Creating custom icon for the master Mi Flower Mate temperature switch")
			Domoticz.Image(Filename="Mi-Flower-Mate-Temp.zip").Create()

		if ("Mi-Flower-Mate-NPK" not in Images):
			Domoticz.Log("Creating custom icon for the master Mi Flower Mate conductivity switch")
			Domoticz.Image(Filename="Mi-Flower-Mate-NPK.zip").Create()


		# create master toggle switch
		if 1 not in Devices:
			Domoticz.Device(Name="update Mi Flowermates",  Unit=1, Type=17,  Switchtype=9, Image=Images['Mi-Flower-Mate'].ID, Used=1).Create()
		
		# get the mac addresses of the sensors
		if Parameters["Mode1"] == 'auto':
			Domoticz.Log("Automatic mode is selected")
			self.floraScan()
		else:
			Domoticz.Log("Manual mode is selected")
			self.macs = parseCSV(Parameters["Mode2"])
			self.createSensors()
		#Domoticz.Log("macs = {}".format(self.macs))
		
		#Devices[Unit].Update(nValue=1,sValue="Off")

	def onStop(self):
		Domoticz.Log("onStop called")

	def onConnect(self, Connection, Status, Description):
		Domoticz.Log("onConnect called")

	def onMessage(self, Connection, Data, Status, Extra):
		Domoticz.Log("onMessage called")

	def onCommand(self, Unit, Command, Level, Hue):
		#Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))		
		
		Domoticz.Log("amount of Flower Mates to now ask for data: " + str(len(self.macs)) )
		
		# flip the switch icon, and then get the plant data.
		if Unit == 1:
			#Devices[Unit].Update(nValue=1,sValue="Off") # best to always turn it off I guess.

			#By setting this to 0, the polling function will run.
			self.currentlyPolling = 0
		  
	
	def onHeartbeat(self):
		# for now this uses the shelve database as its source of truth.
		if( self.currentlyPolling < len(self.macs) ):
			try:
				self.getPlantData(int(self.currentlyPolling))
				if( self.currentlyPolling == len(self.macs) - 1 ):
					Devices[1].Update(nValue=0,sValue="Off")
			except:
				pass
			self.currentlyPolling = self.currentlyPolling + 1
	
	
	# function to create corresponding sensors in Domoticz if there are Mi Flower Mates which don't have them yet.
	def createSensors(self):
		# create the domoticz sensors if necessary
		if ((len(Devices) - 1)/4) < len(self.macs):
			Domoticz.Debug("Creating new sensors")
			# Create the sensors. Later we get the data.
			for idx, mac in enumerate(self.macs):
				Domoticz.Debug("Creating new sensors for Mi Flower Mate at "+str(mac))
				sensorBaseName = "#" + str(idx) + " "

				#moisture

				sensorNumber = (idx*4) + 2
				if sensorNumber not in Devices:
				
					sensorName = sensorBaseName + "Moisture"
					Domoticz.Debug("Creating first sensor, #"+str(sensorNumber))
					Domoticz.Debug("Creating first sensor, name: "+str(sensorName))
					Domoticz.Device(Name=sensorName, Unit=sensorNumber, TypeName="Percentage", Image=Images['Mi-Flower-Mate-Moist'].ID, Used=1).Create()   
					Domoticz.Log("Created device: "+Devices[sensorNumber].Name)

					#temperature

					sensorNumber = (idx*4) + 3
					sensorName = sensorBaseName + "Temperature"
					Domoticz.Device(Name=sensorName, Unit=sensorNumber, TypeName="Temperature", Image=Images['Mi-Flower-Mate-Temp'].ID, Used=1).Create()
					Domoticz.Log("Created device: "+Devices[sensorNumber].Name)

					#light

					sensorNumber = (idx*4) + 4
					sensorName = sensorBaseName + "Light"
					Domoticz.Device(Name=sensorName, Unit=sensorNumber, TypeName="Illumination", Image=Images['Mi-Flower-Mate-Light'].ID, Used=1).Create()
					Domoticz.Log("Created device: "+Devices[sensorNumber].Name)			

					#fertility		

					sensorNumber = (idx*4) + 5
					sensorName = sensorBaseName + "Conductivity"
					Domoticz.Device(Name=sensorName, Unit=sensorNumber, TypeName="Custom", Used=1,Subtype=31, Image=Images['Mi-Flower-Mate-NPK'].ID, Options={"Custom":"1;µS/cm"}).Create()
					Domoticz.Log("Created device: "+Devices[sensorNumber].Name)


	# function to poll a Flower Mate for its data
	def getPlantData(self, idx):
		#for idx, mac in enumerate(self.macs):
		mac = self.macs[idx]
		Domoticz.Log("getting data from sensor: "+str(mac))
		try:
			poller = MiFloraPoller(str(mac), BluepyBackend)
			Domoticz.Debug("Firmware: {}".format(poller.firmware_version()))
			val_bat  = int("{}".format(poller.parameter_value(MI_BATTERY)))
			nValue = 0
		except:
			Domoticz.Log("poller error")



		#moisture

		sensorNumber1 = (idx*4) + 2
		try:
			val_moist = "{}".format(poller.parameter_value(MI_MOISTURE))
			Devices[sensorNumber1].Update(nValue=int(val_moist), sValue=val_moist, BatteryLevel=val_bat)
			Domoticz.Log("moisture = " + str(val_moist))
		except:
			Domoticz.Log("error getting moisture data")

		#temperature

		sensorNumber2 = (idx*4) + 3
		try:
			val_temp = "{}".format(poller.parameter_value(MI_TEMPERATURE))
			Devices[sensorNumber2].Update(nValue=nValue, sValue=val_temp, BatteryLevel=val_bat)
			Domoticz.Log("temperature = " + str(val_temp))
		except:
			Domoticz.Log("error getting temperature data")

		#light

		sensorNumber3 = (idx*4) + 4
		try:
			val_lux = "{}".format(poller.parameter_value(MI_LIGHT))
			Devices[sensorNumber3].Update(nValue=nValue, sValue=val_lux, BatteryLevel=val_bat)
			Domoticz.Log("light = " + str(val_lux))
		except:
			Domoticz.Log("error getting light data")

		#fertility		

		sensorNumber4 = (idx*4) + 5
		try:
			val_cond = "{}".format(poller.parameter_value(MI_CONDUCTIVITY))
			Devices[sensorNumber4].Update(nValue=nValue, sValue=val_cond, BatteryLevel=val_bat)
			Domoticz.Log("conductivity = " + str(val_cond))
		except:
			Domoticz.Log("Error getting conductivity data")		

	# function to scan for devices, and store and compare the outcome
	def floraScan(self):
		Domoticz.Log("Scanning for Mi Flower Mate sensors")
				
		#databaseFile=os.path.join(os.environ['HOME'],'XiaomiMiFlowerMates')
		# first, let's get the list of devices we already know about
		database = shelve.open('XiaomiMiMates')
		
		try:
			knownSensors = database['macs']
			oldLength = len(knownSensors)
			Domoticz.Debug("Already know something:" + str(oldLength))
			Domoticz.Log("Already known devices:" + str(knownSensors))
		except:
			knownSensors = []
			database['macs'] = knownSensors
			oldLength = 0;
			Domoticz.Debug("No existing sensors in system?")
		
		#Next we scan to look for new sensors
		try:
			foundFloras = miflora_scanner.scan(BluepyBackend, 3)
			Domoticz.Log("Number of devices found via bluetooth scan = " + str(len(foundFloras)))
		except:
			foundFloras = []
			Domoticz.Log("Scan failed")
			
		for sensor in foundFloras:
			if sensor not in knownSensors:
				knownSensors.append(str(sensor))
				Domoticz.Log("Found new device: " + str(sensor))
				
		if len(knownSensors) != oldLength:
			database['macs'] = knownSensors
			Domoticz.Log("Updating database")
		
		database.close()	
	
		self.macs = knownSensors
		self.createSensors()

	
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
	global _plugin 
	_plugin.onHeartbeat()
	

def parseCSV(strCSV):
	listvals = []
	for value in strCSV.split(","):
		listvals.append(value)
	return listvals
