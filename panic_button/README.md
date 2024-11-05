# Panic Button Feature

This folder contains all the files related to the physical panic button feature for the smart bus stop.
Here you will find the **source code**, **hardware** needed and **schematic images**.

The panic button has two sources to generate an occurrence: the Raspberry and an ESP32. On the Raspberry, when the panic button is clicked, the Lorawan script is responsible for sending the message to the cloud and at the same time, as redundancy, the button script also sends the location and event to a Telegram channel. Meanwhile, the panic button example with the ESP32 also generates an automatic message in a Telegram channel exclusively for sending occurrences.

## Dependencies

### Raspberry 
If you're using raspbian, all dependencies must be installed:

- Python3
- RPi GPIO package
- pyTelegramBot (https://github.com/eternnoir/pyTelegramBotAPI)
    - Chat ID is exclusive from the chat that you want to send messages. How to get this info: https://gist.github.com/nafiesl/4ad622f344cd1dc3bb1ecbe468ff9f8a
    - To get the Token and get the token, this must be do through the BotFather. How to: https://core.telegram.org/bots/features#botfather

In case the execution of the script causes any error related to the button callback, the RPi package may be changed. You can perform the following commands:

```bash
sudo apt remove python3-rpi.gpio
sudo apt update
sudo apt install python3-rpi-lgpio
```

This will not change the behavior of the package or any functions.

### ESP32

- Universal Telegram Bot (https://docs.arduino.cc/libraries/universaltelegrambot/)
- Chat ID and Telegram Token (same as raspberry used on python script)

### List of materials

- Push Button

### Circuit Schematics

For this example the following kit was used with the Button A as a panic button trigger:
![alt text](img/devkit.webp)

## Usage

Before using `button.py` script, the `lorawan_connectivity_module.py` script must be executed.