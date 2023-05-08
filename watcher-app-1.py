from paho.mqtt import client as mqtt
# MQTT client library for python
import time

#Defining the MQTT broker host and port details 
broker_address = "broker.emqx.io"
broker_port = 1883

# Defining the MQTT client
client = mqtt.Client()
# and the connection status which is set to false hence client is not yet connected
connected = False

#
# function for handling the connection event 
def connection(client, userdata, flags, rc):
    # rc is an integer that indicates the result of the connection attempt 
    # if rc=0, connection is successful
    global connected
    if rc == 0:
        print("Connected to MQTT broker")
        # connection status is set to true
        connected = True
    else:
        # if connection fails, we retry after 5 seconds
        print("Connection failed. Retrying in 5 seconds")
        time.sleep(5)
        client.connect(broker_address, broker_port)

# function for handling the disconnection event 
def disconnection(client, userdata, rc):
    global connected
    print("Disconnected from MQTT broker!")
    # # connection status is set to true
    connected = False

# Connect to MQTT broker by calling the connection and disconnection functions
client.on_connect = connection
client.on_disconnect = disconnection
# to connect to MQTT broker and pass the broker host address and port number
try:
    client.connect(broker_address,broker_port) #connect to broker
except:
    print('connection failed')
    exit(1) 


# using a loop for the network statistics
while True:
    if connected:
        # Record the time it got a connection
        time_connected = time.time()
        
        # Send network statistics to MQTT broker
        retries = client.reconnects()
        client.publish("lora-gateway/status", f"Connected at {time_connected}. Retries: {retries}")
    else:
        # Record the time it lost connection
        time_disconnected = time.time()

    time.sleep(60) # Wait 60 seconds before sending network statistics again