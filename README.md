# Mi_Flower_mate_plugin
A plugin for Domoticz, the open source home automation software, which allows it to easily connect to Xiaomi Mi Flower Mate devices

## INSTALLATION

Install the plugin as usual. See: https://www.domoticz.com/wiki/Using_Python_plugins

You also need the Bluepy library to be installed. If you don't mind that python 3.5 is installed, just enter these commands in the terminal:

  sudo apt-get install python3-pip libglib2.0-dev<br/>
  sudo pip3 install bluepy<br/>

Alternatively, you can try:

wget https://bootstrap.pypa.io/get-pip.py<br/>
sudo python3 get-pip.py<br/>
sudo python3 -m pip install bluepy<br/>

Scan for your Flower Mates to find their mac-addresses:

  sudo hcitool lescan


## Thanks to

This plugin builds on the work by Daniel Matuschek, who created a great library for the Flower Mate devices.<br/>
https://pypi.python.org/pypi/miflora

It also builds onthe original domoticz script created by Tristan:<br/>
https://github.com/Tristan79/miflora
