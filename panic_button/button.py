#! /usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as gpio
import time
import signal
import sys

# GPIO numbers
green_led = 15
yellow_led = 13
red_led = 11
blue_led = 40
p_button = 37

def init():
    gpio.setmode(gpio.BOARD)

def setup():
    gpio.setup(p_button, gpio.IN, pull_up_down = gpio.PUD_DOWN)
    gpio.setup(blue_led, gpio.OUT)
    gpio.setup(green_led, gpio.OUT)
    gpio.setup(yellow_led, gpio.OUT)
    gpio.setup(red_led, gpio.OUT)

def my_callback(channel):
    print("Button Clicked!")
    gpio.output(blue_led, gpio.HIGH)
    time.sleep(1)
    gpio.output(blue_led, gpio.LOW)

if __name__ == '__main__':
    init()
    setup()
    gpio.add_event_detect(p_button, gpio.RISING, callback=my_callback, bouncetime=300)

    # Add other routines
    while True:
        pass
