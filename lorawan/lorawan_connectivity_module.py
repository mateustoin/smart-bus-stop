from RoboCore_SMW_SX1262M0 import SMW_SX1262M0, CommandResponse
import os

# LoRaWAN paratrization and credentials for ABP
DEVADDR = "00000000"
APPSKEY = "00000000000000000000000000000000"
NWKSKEY = "00000000000000000000000000000000"
MODE_ABP = 0 # 0 = ABP / 1 = OTAA
lorawan = SMW_SX1262M0("/dev/serial0")

# Named pipe definitions
fifo_path = "/tmp/lorawan_comm"

################
# Main program #
################

# Named pipe creation
os.system('mkfifo /tmp/lorawan_comm')

# Read LoRaWAN credentials from file
with open("lorawan_comm.txt", "r") as file_lorawan_comm:
    lines = file_lorawan_comm.readlines()

DEVADDR = lines[0].strip()
APPSKEY = lines[1].strip()
NWKSKEY = lines[2].strip()

print("- Configuracao do SMW-SX1262M0 em modo ABP")

lorawan.reset()

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
    print(" LoRaWAN module (SMW-SX1262M0) configuration has been saved")
else:
    print("Fail to save LoRaWAN module (SMW-SX1262M0) configuration")

lorawan.join()    

# Constantly listens for messages in named pipe.
# When a new message is received, it's forwarded to project's cloud application over LoRaWAN
with open(fifo_path, "r") as fifo:
    while True:
        msg = fifo.readline()
        if msg:
            print(f"A new message has been received from LoRaWAN named pipe: {msg.strip()}")

            # Envia a mensagem por LoRaWAN
            if (lorawan.isConnected()):

                returnCode = lorawan.sendX(12, msg.strip())
                
                if returnCode == CommandResponse.OK:
                    print("[SUCCESS] The message has been successfully sent over LoRaWAN")
                else:
                    print("[ERROR] Failed to send the message over LoRaWAN")    