# LoRaWAN connectivity module

This folder contains the LoRaWAN connectivity module from Smart Bus Stop project.
Here you'll find both its source-code and instructions to prepare your embedded Linux to inbteract with this module.

## Hardware info

Here follows detailed information about LoRaWAN module hardware:

* LoRaWAN module: SMW-SX1262M0
* LoRaWAN module vendor: Smart Modular
* In this project, we've used the "LoRaWAN HAT para Raspberry Pi" devkit, which containing this LoRaWAN module.
More info on this devkit can be obtained in: https://www.robocore.net/hat-raspberry-pi/lorawan-hat-para-raspberry-pi?gad_source=1&gclid=Cj0KCQjwi5q3BhCiARIsAJCfuZm063ZTYEaf3Bp039azjAWr2IPruBn8mocZ8ETrZjCFsqQL_G9AiBgaAt0PEALw_wcB
* Operational frequency: two frequency ranges: from 902 to 907.4MHz and from 915.2 to 927.8MHz
* Antenna type: helical antenna
* Supported communication modes: P2P ("pure" LoRa communication) and LoRaWAN
* Supported activation modes when using LoRaWAN: ABP and OTAA

## Dependencies install

Use the commands below to install all dependencies:

``
pip3 install RoboCore_SMW-SX1262M0
``

More information on libraries can be found at https://github.com/RoboCore/RoboCore_SMW-SX1262M0_Python

## Usage

The LoRaWAN connectivity module from Smart Bus Stop project can be used a stand-alone LoRaWAN piece for sending LORaWAN messagem to the cloud over LoRaWAN connectivity. 

Here follows the instruction to run this module:

1) Place the "lorawan_connectivity_module.py" file in /home/pi folder.
2) Place the "lorawan_connectivity_service_file.service" file in "/etc/systemd/system/" folder and execute the command below:

``
sudo systemctl daemon-reload
``

3) Execute the following command to enable LoRaWAN connectivity module as a service (handled by systemd) in Linux:

``
sudo systemctl enable lorawan_connectivity_service_file
``

It'll also automatically start the LoRaWAN connectivity module when Raspberry Pi boots.


4) Execute the following command to start LoRaWAN connectivity module as a service (handled by systemd) in Linux:

``
sudo systemctl start lorawan_connectivity_service_file
``

After following the steps above, the LoRaWAN connectivity module is ready to be used. All programs running in the same Linux instance can send a LoRaWAN message by writing it in a named pipe, which is constantly listened by LoRaWAN connectivity module.

Therefore, once LoRaWAN connectivity module is active, all you need to do to send a LoRaWAN message to the project's cloud application is to write the desired message to the **lorawan_comm** named pipe, as seen in example below:

``
echo "Message" > /tmp/lorawan_comm
``

IMPORTANT: 
1) Before use this module, you need to create a TXT file names "lorawan_comm.txt" (in the same folder as this module's .py file is) containing:
   * Device Address in the first line (hex-string format, no : nor - allowed)
   * Application Session Key in the second line (hex-string format, no : nor - allowed)
   * Network Session Key in the third line (hex-string format, no : nor - allowed)
2) All messages MUST be in hex-string format. Example: if you need to send the "ABCD" message, the correspondent hex-string for this is "41424344" (in ASCII table: A=0x41, B=0x42, C=0x43 and D=0x44).


## Operational conditions

The LoRaWAN connectivity module from Smart Bus Stop project has the following operational conditions

* Only uplink messages are supported
* LoRaWAN communication is established using ABP activation mode, which means the credentials are hard-coded in this module
* LoRaWAN Class: A
* LoRaWAN ADR: off
* Maximum TX power: 22dBm
* SMW-SX1262M0 is manufactured to work in Brazil, so it uses AU915-928A (RX1 = 1s, RX2 = 2s) or LA915-928A (RX1 = 5s, RX2 = 6s) LoRaWAN regions