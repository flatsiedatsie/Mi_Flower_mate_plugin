"""
<plugin key="Mi_flower_mate" name="Xiaomi Mi Flower Mate" author="blauwebuis" version="1.0.0" wikilink="https://www.domoticz.com/wiki/Plugins/Mi_flower_mate" externallink="https://www.domoticz.com/forum/viewtopic.php?f=65&t=22281">
	<description>
		This plugin connects to Mi Flower Mate flower sensors over Bluetooth LE. It requires the BluePy library to be installed on the system.
	</description>
	<params>
		<param field="Mode1" label="Devices mac adresses, capitalised and comma separated" width="300px" required="true" default="C4:7C:8D:62:50:34"/>
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
		#Domoticz.Debugging(1)   
		return 

	def onStart(self):
		sys.path.append("/usr/local/lib/python3.4/dist-packages")
		sys.path.append("/usr/local/lib/python3.5/dist-packages")
	   
		if bluepyError == 1:
			Domoticz.Log("error loading Flora libraries")
		
		self.domoticzServer=Parameters["Address"]
		self.port=Parameters["Port"]
		self.webPath=str(self.domoticzServer) + ":" + str(self.port)
		self.macs = parseCSV(Parameters["Mode1"])
		
		Domoticz.Debug("macs = {}".format(self.macs))

		Domoticz.Log("Mi Flora - Macs = " + str(Parameters["Mode1"]))
		Domoticz.Log("Mi Flora - devices made so far (max 255): " + str(len(Devices)))
		
		# create the listen-toggle-switch. This controls the making of new RF switches.
		if 1 not in Devices:
			Domoticz.Log("Creating the master Mi Flower Mate poll switch. Flip it to poll the sensors.")
			Domoticz.Device(Name="Flip to update Mi Flowermates", Unit=1, TypeName="Switch", Image=9, Used=1).Create()
		
		
		if ((len(Devices) - 1)/4) < len(self.macs):
			Domoticz.Log("Creating new sensors")
			# Create the sensors. Later we get the data.
			for idx, mac in enumerate(self.macs):
				Domoticz.Log("Creating devices for mac: "+str(mac))
				sensorBaseName = "#" + str(idx) + " "

				#moisture

				sensorNumber = (idx*4) + 2
				if sensorNumber not in Devices:
				
					sensorName = sensorBaseName + "Moisture"
					Domoticz.Log("Creating first sensor, #"+str(sensorNumber))
					Domoticz.Log("Creating first sensor, name: "+str(sensorName))
					Domoticz.Device(Name=sensorName, Unit=sensorNumber, TypeName="Percentage", Used=1).Create()   
					Domoticz.Log("Created device: "+Devices[sensorNumber].Name)

					#temperature

					sensorNumber = (idx*4) + 3
					sensorName = sensorBaseName + "Temperature"
					Domoticz.Device(Name=sensorName, Unit=sensorNumber, TypeName="Temperature", Used=1).Create()
					Domoticz.Log("Created device: "+Devices[sensorNumber].Name)

					#light

					sensorNumber = (idx*4) + 4
					sensorName = sensorBaseName + "Light"
					Domoticz.Device(Name=sensorName, Unit=sensorNumber, TypeName="Illumination", Used=1).Create()
					Domoticz.Log("Created device: "+Devices[sensorNumber].Name)			

					#fertility		

					sensorNumber = (idx*4) + 5
					sensorName = sensorBaseName + "Conductivity"
					Domoticz.Device(Name=sensorName, Unit=sensorNumber, TypeName="Custom", Used=1).Create()
					Domoticz.Log("Created device: "+Devices[sensorNumber].Name)			


	def onStop(self):
		Domoticz.Log("onStop called")

	def onConnect(self, Connection, Status, Description):
		Domoticz.Log("onConnect called")

	def onMessage(self, Connection, Data, Status, Extra):
		Domoticz.Log("onMessage called")

	def onCommand(self, Unit, Command, Level, Hue):
		Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))		
		
		# flip the switch icon, and then get the plant data.

		if Unit == 1:
			if str(Command) == "On":
				Devices[Unit].Update(nValue=1,sValue="On")
			if str(Command) == "Off":
				Devices[Unit].Update(nValue=0,sValue="Off")
			  
			self.getPlantData()
		  
	
	def onHeartbeat(self):
		pass

	
	def getPlantData(self):
		for idx, mac in enumerate(self.macs):
			Domoticz.Log("getting data from sensor: "+str(mac))
		 
			poller = MiFloraPoller(str(mac), BluepyBackend)
			Domoticz.Log("Firmware: {}".format(poller.firmware_version()))
			
			val_bat  = int("{}".format(poller.parameter_value(MI_BATTERY)))
			nValue = 0
			
			#moisture
			
			sensorNumber1 = (idx*4) + 2
			val_moist = "{}".format(poller.parameter_value(MI_MOISTURE))
			Devices[sensorNumber1].Update(nValue=nValue, sValue=val_moist, BatteryLevel=val_bat)
			Domoticz.Log("moisture = " + str(val_moist))
			
			#temperature
			
			sensorNumber2 = (idx*4) + 3
			val_temp = "{}".format(poller.parameter_value(MI_TEMPERATURE))
			Devices[sensorNumber2].Update(nValue=nValue, sValue=val_temp, BatteryLevel=val_bat)
			Domoticz.Log("temperature = " + str(val_temp))
			
			#light
			
			sensorNumber3 = (idx*4) + 4	
			val_lux = "{}".format(poller.parameter_value(MI_LIGHT))
			Devices[sensorNumber3].Update(nValue=nValue, sValue=val_lux, BatteryLevel=val_bat)
			Domoticz.Log("light = " + str(val_lux))
			
			#fertility		
		
			sensorNumber4 = (idx*4) + 5	
			val_cond = "{}".format(poller.parameter_value(MI_CONDUCTIVITY))
			Devices[sensorNumber4].Update(nValue=nValue, sValue=val_cond, BatteryLevel=val_bat)
			Domoticz.Log("conductivity = " + str(val_cond))
			
			# give bluetooth a little breathing room
			time.sleep(0.2)

	
	
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


