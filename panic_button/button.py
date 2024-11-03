#! /usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as gpio
import time
import signal
import sys

import telebot

API_TOKEN = ''

with open('telegram_token.txt', 'r') as file:
    API_TOKEN = file.readline().strip()

tb = telebot.TeleBot(API_TOKEN)
channel_id = -1002306431687
alert_message = 'Acionamento de botao do panico na seguinte localizacao:'

#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

# File name to write
wfile = "/tmp/panic_button"

# GPIO numbers
#green_led = 15
#yellow_led = 13
#red_led = 11
#blue_led = 40
p_button = 37

def send_telegram_info():
    # sendMessage on Channel chat
    tb.send_message(channel_id, alert_message)
    tb.send_location(channel_id, -22.813407, -47.0643614)

def init():
    gpio.setmode(gpio.BOARD)

def setup():
    gpio.setup(p_button, gpio.IN, pull_up_down = gpio.PUD_DOWN)
    #gpio.setup(blue_led, gpio.OUT)
    #gpio.setup(green_led, gpio.OUT)
    #gpio.setup(yellow_led, gpio.OUT)
    #gpio.setup(red_led, gpio.OUT)

def pressed_panic_button_event(channel):
    print("Panic Button Clicked!")
    with open(wfile, 'w') as file:
        file.write('10')
        file.flush()
    send_telegram_info()
    #gpio.output(blue_led, gpio.HIGH)
    #time.sleep(1)
    #gpio.output(blue_led, gpio.LOW)

if __name__ == '__main__':
    init()
    setup()
    gpio.add_event_detect(p_button, gpio.RISING, callback=pressed_panic_button_event, bouncetime=300)

    # Add other routines
    while True:
        pass
