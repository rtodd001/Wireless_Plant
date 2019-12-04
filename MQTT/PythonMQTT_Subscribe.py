"""
Python MQTT Subscription client
Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
Written for my Instructable - "How to use MQTT with the Raspberry Pi and ESP8266"
"""
import paho.mqtt.client as mqtt
import os
from time import sleep
from mic_rec import SpeechText
import RPi.GPIO as GPIO


# Don't forget to change the variables for the MQTT broker!
mqtt_username = "rtodd"
mqtt_password = "CS122A"
mqtt_topic = "Your Topic"
mqtt_broker_ip = "192.168.43.220"

client = mqtt.Client()
# Set the username and password for the MQTT client
client.username_pw_set(mqtt_username, mqtt_password)

#button set up
BUTTON = 17

# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
    print ("Connected!", str(rc))
    
    # Once the client has connected to the broker, subscribe to the topic
    client.subscribe(mqtt_topic)
    
def on_message(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
    
    #print "Topic: ", msg.topic + "\nMessage: " + str(msg.payload)
    
    value = SpeechText()
    print("You said: {}".format(value))
    os.system('clear')
    if (value.find("exit") > -1):
        sys.exit()
    if (value.find("status") > -1 or value.find("water") > -1 or value.find("plant") > -1):
        if(int(msg.payload) > 150):
            print ("\n\nPlant has been watered\n\n")
        else:
            print ("\n\nPlease water the plant\n\n")
    else:
        print("you said an invalid command")
    sleep(3)

    ##moved the sleep function below where the loop is called
    #insert the sleep functions here
    #print("before sleep loop")
    #while not GPIO.input(BUTTON):
        #print("Sleeping")
        #sleep(1)
    #print("after sleep loop")

    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata

# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message
client.on_connect = on_connect
client.on_message = on_message

# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using
client.connect(mqtt_broker_ip, 1883)

# Once we have told the client to connect, let the client object run itself
#client.loop_forever()

#create a loop function that waits for button input
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)
while True:
    state = GPIO.input(BUTTON)
    if not state:
        print("looping again")
        client.loop()
    else:
        os.system('clear')
        print("Press button on hat to say a command")
        sleep(1)




client.disconnect()
