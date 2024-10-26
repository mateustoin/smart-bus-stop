# Imports
from RoboCore_SMW_SX1262M0 import SMW_SX1262M0, CommandResponse
import os
import threading
import queue

# Constants and Variables
# LoRaWAN credentials for ABP
DEVADDR = "00000000"
APPSKEY = "00000000000000000000000000000000"
NWKSKEY = "00000000000000000000000000000000"
MODE_ABP = 0  # 0 = ABP / 1 = OTAA
lorawan = SMW_SX1262M0("/dev/serial0")

# Named pipe definitions
fifo_people_counter_path = "/tmp/people_counter"
fifo_panic_button_path = "/tmp/panic_button"

# People counter
people_counter = 0

# Event codes
event_people_counter_value = "00"
event_panic_button_trigger = "01"

# LoRaWAN timer variables
lorawan_timer = None
lorawan_timer_value = 30 #s

# Variable to check if there's a panic button event registered
is_there_any_panic_button_event = 0

# Queue to send messages to the LoRaWAN control thread
message_queue = queue.Queue()

############
# Functions
############

# LoRaWAN timer callback function
def lorawan_callback_timer_func():
    global is_there_any_panic_button_event
    global people_counter

    print("LoRaWAN timer callback has been triggered. Checking if there's panic button message to be sent...")

    if (is_there_any_panic_button_event == 1):
        msg_hexstring = event_panic_button_trigger + f'{people_counter:x}'
        print(f"Hex-string panic button message: {msg_hexstring}")
        message_queue.put(msg_hexstring)
        is_there_any_panic_button_event = 0 # Indicates panic button event has been sent
    
# LoRaWAN timer start
def start_lorawan_timer():
    global lorawan_timer

    # If timer is already under execution, cancel it
    if lorawan_timer is not None:
        lorawan_timer.cancel()

    # Start a new timer
    lorawan_timer = threading.Timer(lorawan_timer_value, lorawan_callback_timer_func)
    lorawan_timer.start()
    print("LoRaWAN timer is started. Timer value: "+ str(lorawan_timer_value))

# Function for sending and receiving data from LoRaWAN module
def lorawan_control_thread():
    while True:
        msg = message_queue.get()
        if msg:
            print(f"Sending message via LoRaWAN: {msg}")
            if lorawan.isConnected():
                returnCode = lorawan.sendX(12, msg.strip())
                if returnCode == CommandResponse.OK:
                    print("[SUCCESS] Message sent over LoRaWAN")
                else:
                    print("[ERROR] Failed to send message over LoRaWAN")
            else:
                print("[ERROR] LoRaWAN module not connected")

# Function for reading people counter value from FIFO, and for redirecting it
# to LoRaWAN control thread through a queue
def read_fifo_people_counter():
    global people_counter
    global event_people_counter_value

    print("People counter thread is on")
    with open(fifo_people_counter_path, "r") as fifo:
        while True:
            msg = fifo.readline().strip()
            if msg:
                people_counter = int(msg)
                print(f"Message from people counter named pipe: {msg}")
                msg_hexstring = event_people_counter_value + f'{people_counter:x}'
                print(f"Hex-string people counter message: {msg_hexstring}")
                message_queue.put(msg_hexstring)

                # Start LoraWAN timer
                start_lorawan_timer()

# Function for reading panic button events from FIFO, and for redirecting them
# to LoRaWAN control thread through a queue
def read_fifo_panic_button():
    
    global event_panic_button_trigger
    global is_there_any_panic_button_event

    print("Panic Button thread is on")
    with open(fifo_panic_button_path, "r") as fifo:
        while True:
            msg = fifo.readline().strip()
            is_there_any_panic_button_event = 1
            print(f"Message from panic button named pipe: {msg}")

##############
# Main program
##############

# Create named pipes
os.system(f'mkfifo {fifo_people_counter_path}')
os.system(f'mkfifo {fifo_panic_button_path}')

# Read LoRaWAN credentials from file
with open("lorawan_comm.txt", "r") as file_lorawan_comm:
    lines = file_lorawan_comm.readlines()
    DEVADDR, APPSKEY, NWKSKEY = [line.strip() for line in lines[:3]]

print("- Configuring SMW-SX1262M0 in ABP mode")

# LoRaWAN module (SMW-SX1262M0) configuration
if lorawan.set_JoinMode(MODE_ABP) == CommandResponse.OK:
    print("Join mode: ABP")
else:
    print("Failed to configure join mode as ABP")

if lorawan.set_DevAddr(DEVADDR) == CommandResponse.OK:
    print("Device Address successfully configured")
else:
    print("Failed to configure Device Address")

if lorawan.set_AppSKey(APPSKEY) == CommandResponse.OK:
    print("Application Session Key successfully configured")
else:
    print("Failed to configure Application Session Key")

if lorawan.set_NwkSKey(NWKSKEY) == CommandResponse.OK:
    print("Network Session Key successfully configured")
else:
    print("Failed to configure Network Session Key")

if lorawan.set_ADR(1) == CommandResponse.OK:
    print("ADR set to ON")
else:
    print("Failed to configure ADR to ON state")

if lorawan.set_DR(0) == CommandResponse.OK:
    print("ADR DR set to 0")
else:
    print("Failed to configure DR to 0")

if lorawan.save() == CommandResponse.OK:
    print("Configuration saved")
else:
    print("Failed to save configuration")

lorawan.join()

# Create and start threads
thread_lorawan_control = threading.Thread(target=lorawan_control_thread)
thread_people_counter = threading.Thread(target=read_fifo_people_counter)
thread_panicbutton = threading.Thread(target=read_fifo_panic_button)

thread_lorawan_control.start()
thread_people_counter.start()
thread_panicbutton.start()

# Wait for all threads to finish (they will run indefinitely)
thread_lorawan_control.join()
thread_people_counter.join()
thread_panicbutton.join()
