from RoboCore_SMW_SX1262M0 import SMW_SX1262M0, CommandResponse
import os
import threading
import queue

# LoRaWAN paratrization and credentials for ABP
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

# Events
event_people_counter_value = "00"
event_panic_button_trigger = "01"

# Create the named pipes
os.system(f'mkfifo {fifo_people_counter_path}')
os.system(f'mkfifo {fifo_panic_button_path}')

# Read LoRaWAN credentials from file
with open("lorawan_comm.txt", "r") as file_lorawan_comm:
    lines = file_lorawan_comm.readlines()

DEVADDR = lines[0].strip()
APPSKEY = lines[1].strip()
NWKSKEY = lines[2].strip()

print("- Configuracao do SMW-SX1262M0 em modo ABP")

#lorawan.reset()

# LoRaWAN module (SMW-SX1262M0) configuration
returnCode = lorawan.set_JoinMode(MODE_ABP)
if returnCode == CommandResponse.OK:
    print("Join mode: ABP")
else:
    print("Failed to configure join mode as ABP")

returnCode = lorawan.set_DevAddr(DEVADDR)
if returnCode == CommandResponse.OK:
    print("Device Address successfully configured")
else:
    print("Failed to configure Device Address")

returnCode = lorawan.set_AppSKey(APPSKEY)
if returnCode == CommandResponse.OK:
    print("Application Session Key successfully configured")
else:
    print("Failed to configure Application Session Key")

returnCode = lorawan.set_NwkSKey(NWKSKEY)
if returnCode == CommandResponse.OK:
    print("Network Session Key successfully configured")
else:
    print("Failed to configure Network Session Key")

returnCode = lorawan.save()
if returnCode == CommandResponse.OK:
    print("LoRaWAN module (SMW-SX1262M0) configuration has been saved")
else:
    print("Fail to save LoRaWAN module (SMW-SX1262M0) configuration")

lorawan.join()

# Queue to send messages to the LoRaWAN control thread
message_queue = queue.Queue()

# Function for the LoRaWAN UART control thread
def lorawan_control_thread():
    while True:
        # Wait for a message from the queue
        msg = message_queue.get()

        if msg:
            print(f"Sending message via LoRaWAN: {msg}")

            # Send the message over LoRaWAN
            if lorawan.isConnected():
                returnCode = lorawan.sendX(12, msg.strip())
                if returnCode == CommandResponse.OK:
                    print(f"[SUCCESS] The message has been successfully sent over LoRaWAN")
                else:
                    print(f"[ERROR] Failed to send the message over LoRaWAN")
            else:
                print("[ERROR] LoRaWAN module not connected")

# Function to read from people counter named pipe
def read_fifo_people_counter():
    global people_counter

    print("People counter thread is on")
    with open(fifo_people_counter_path, "r") as fifo:
        while True:
            msg = fifo.readline()
            msg_str = msg.strip()

            if msg:
                # Update people counter value
                people_counter = int(msg_str)

                print(f"A new message has been received from people counter named pipe: {msg_str}")

                # Format the message into a hex-string, adding event byte
                msg_hexstring = event_people_counter_value + f'{people_counter:x}'
                print(f"Hex-string people counter message: {msg_hexstring}")
                
                # Add the hex-string message to the queue for the LoRaWAN control thread
                message_queue.put(msg_hexstring)               
                

# Function to read from panic button named pipe
def read_fifo_panic_button():
    global people_counter

    print("Panic button thread is on")
    with open(fifo_panic_button_path, "r") as fifo:
        while True:
            msg = fifo.readline()
            if msg:
                print(f"A new message has been received from panic button named pipe: {msg.strip()}")
                print(f"Last people counter value: "+str(people_counter))

                # Format the message into a hex-string, adding event byte and most recent people counter value
                msg_hexstring = event_panic_button_trigger + f'{people_counter:x}'
                print(f"Hex-string people counter message: {msg_hexstring}")

                # Add the message to the queue for the LoRaWAN control thread
                message_queue.put(msg.strip())                

# Create and start the thread for LoRaWAN UART control
thread_lorawan_control = threading.Thread(target=lorawan_control_thread)
thread_lorawan_control.start()

# Create and start threads to read from both named pipes
thread_people_counter = threading.Thread(target=read_fifo_people_counter)
thread_panicbutton = threading.Thread(target=read_fifo_panic_button)
thread_people_counter.start()
thread_panicbutton.start()

# Wait for all threads to finish (they will run indefinitely)
thread_people_counter.join()
thread_panicbutton.join()
thread_lorawan_control.join()
