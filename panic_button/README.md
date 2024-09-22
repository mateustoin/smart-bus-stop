# Panic Button Feature

This folder contains all the files related to the physical panic button feature for the smart bus stop.
Here you will find the **source code**, **hardware** needed and **schematic images**.

## Dependencies

If you're using raspbian, all dependencies must be installed:

- Python3
- RPi GPIO package

In case the execution of the script causes any error related to the button callback, the RPi package may be changed. You can perform the following commands:

```bash
sudo apt remove python3-rpi.gpio
sudo apt update
sudo apt install python3-rpi-lgpio
```

This will not change the behavior of the package or any functions.

## Hardware Info

### List of materials

- LED
- Button
- etc

### Circuit Schematics

TODO: Add circuit schematics

## Usage

TODO: Add script usage