# Logging service application to know the status of the network connection of the Lora gateway
# and know network health status

# the relevant libraries: MQTT client library for python and time module
from paho.mqtt import client as mqtt
import time

#the MQTT client is defined
client = mqtt.Client()

# and the connection status which is set to false hence client is not yet connected
connected = False

#the MQTT broker host and port details 
broker_address = "broker.emqx.io"
broker_port = 1883

# function for handling the connection event 
def connection(client, userdata, flags, rc):
    # rc is an integer that indicates the result of the connection attempt 
    # if rc=0, connection was successful
    global connected
    if rc == 0:
        print("Connected to MQTT broker")
        # connection status is set to true
        connected = True
    else:
        # if connection fails, we retry after 5 seconds
        print("Connection failed. Retrying in 5 seconds")
        # sleep suspends execution of the current thread for a given number of seconds
        time.sleep(5)

        try:
            client.connect(broker_address,broker_port) #connect to broker
        except:
            print("connection failed")
            exit(1) 

# function for handling the disconnection event 
def disconnection(client, userdata, rc):
    global connected
    print("Disconnected from MQTT broker!")
    # # connection status is set to true
    connected = False

# calling the connection and disconnection functions to connect to mqtt broker
client.on_connect = connection
client.on_disconnect = disconnection
try:
    client.connect(broker_address,broker_port) #connect to broker
except:
    print("connection failed")
    exit(1) 

# using a loop for the network statistics
while True:
    if connected:
        # to record the time it got a connection using time module
        # returns the number of seconds since point where time begins
        time_connected = time.time()
        
        # sending network statistics to MQTT broker
        re_tries = client.reconnects()
        client.publish("lora-gateway/status","Time of connection: {time_connected}. Number of retries: {re_tries}")
    else:
        # recording the time it lost connection
        time_disconnected = time.time()

# wait 60 seconds before sending network statistics again
    time.sleep(60) 