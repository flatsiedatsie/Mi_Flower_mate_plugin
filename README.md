# Mi_Flower_mate_plugin
A plugin for Domoticz, the open source home automation software, which allows it to easily connect to Xiaomi Mi Flower Mate devices.

These are Bluetooth LE plant monitoring devices which cost about 12 dollars. They last up to a year on a coincell battery, and measure moisture, temperature, light and conductivity.
https://wiki.hackerspace.pl/projects:xiaomi-flora

The plugin creates a special switch. Toggle the switch to get fresh data from all sensors. By having a switch to poll for new data, it becomes easy to create timers and other fun integrations in scripts.

The plugin now also has an "automatic" mode, where it will do a bluetooth scan for devices everytime Domoticz starts, and automatically add new devices it finds.


## Links
Detailed installation instructions can be found on the Domoticz wiki:
https://www.domoticz.com/wiki/Plugins/Mi_flower_mate

Discussion about the plugin can be found here:
https://www.domoticz.com/forum/viewtopic.php?f=65&t=22281


## Installation (short version)
Install the plugin as usual. See: https://www.domoticz.com/wiki/Using_Python_plugins

You also need the Bluepy library to be installed.

wget https://bootstrap.pypa.io/get-pip.py<br/>
sudo python3 get-pip.py<br/>
sudo python3 -m pip install bluepy<br/>

Alternatively, you can use apt-get, but might install python 3.5 as well. If you are trying to stay on python 3.4, use the wget method above.

  sudo apt-get install python3-pip libglib2.0-dev<br/>
  sudo pip3 install bluepy<br/>
  

In automatic mode, the plugin will do bluetooth scans at startup, and integrate any Mi Flora Devices it finds. 

In manual mode you can select which devices to add by entering their mac addresses on the hardware page. To find your Flower Mates' mac-addresses do a bluetooth scan:

  sudo hcitool lescan



## Thanks to

This plugin builds on the work by Daniel Matuschek, who created a great library for the Flower Mate devices.<br/>
https://pypi.python.org/pypi/miflora

It also builds on the original domoticz script created by Tristan:<br/>
https://github.com/Tristan79/miflora
