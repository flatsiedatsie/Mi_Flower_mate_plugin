# Mi_Flower_mate_plugin
A plugin for Domoticz, the open source home automation software, which allows it to easily connect to Xiaomi Mi Flower Mate devices

INSTALLATION

Install the plugin as usual. See: https://www.domoticz.com/wiki/Using_Python_plugins

You also need the Bluepy library to be installed:

  sudo apt-get install python3-pip libglib2.0-dev
  sudo pip3 install bluepy


Scan for your Flower Mates to find their mac-addresses:

  sudo hcitool lescan


It builds on the work by Daniel Matuschek, who created a great library for the Flower Mate devices.
https://pypi.python.org/pypi/miflora

As well as the original domoticz script created by Tristan:
https://github.com/Tristan79/miflora
