# Mi_Flower_mate_plugin
A plugin for Domoticz, the open source home automation software, which allows it to easily connect to Xiaomi Mi Flower Mate devices

INSTALLATION

Install the plugin as usual. See: https://www.domoticz.com/wiki/Using_Python_plugins

You also need the Bluepy library to be installed:

  sudo apt-get install python3-pip libglib2.0-dev
  sudo pip3 install bluepy


Scan for your Flower Mates to find their mac-addresses:

  sudo hcitool lescan
