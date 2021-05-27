#!/usr/bin/env python3
from ubidots import ApiClient
import Adafruit_DHT

import RPi.GPIO as GPIO
import tm1637
import threading
import time

tm = tm1637.TM1637(clk=20, dio=21)
sensor=Adafruit_DHT.DHT11

tm.show('----')
ENTER_PIN = 27 #was 23
EXIT_PIN = 23  #was 27
TEMP_PIN = 12

peoplecounter = 0

def setup():
    global people
    global peoplecounter
    global PEOPLECOUNT_ID
    global TEMPCOUNT_ID
    global HUMIDITYCOUNT_ID
    global templevel
    global humiditylevel

    API_KEY = "BBFF-b324f9278c9dd3b78728cd92f16ac5e527e"
    PEOPLECOUNT_ID = "6068cc8a1d847201e0d016f9"
    TEMPCOUNT_ID = "60a990d81d84723522cb7ba4"
    HUMIDITYCOUNT_ID = "60a990de1d847235aae670aa"

    try:
        api = ApiClient(apikey=API_KEY)
        people = api.get_variable(PEOPLECOUNT_ID)
        templevel= api.get_variable(TEMPCOUNT_ID)
        humiditylevel = api.get_variable(HUMIDITYCOUNT_ID)

        peoplecounter = people.get_values()[0]['value']
    except:
        print("Couldn't connect to the API, check your Internet connection")
        print (error)
        exit()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ENTER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(EXIT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    tm.number(int(peoplecounter))

def EXITPIN(countdir):
    global peoplecounter
    global people
    peoplecounter  -=1
    print (peoplecounter)
    tm.number(int(peoplecounter))
    people.save_value({'value':peoplecounter})
#    TEMPCHECK()

def ENTERPIN(ev=None):
    global peoplecounter
    global people
    peoplecounter += 1
    print(peoplecounter)
    tm.number(int(peoplecounter))
    people.save_value({'value':peoplecounter})
#    TEMPCHECK()

def TEMPCHECK():
    global templevel
    global humiditylevel
    humidity, temperature = Adafruit_DHT.read_retry(sensor, TEMP_PIN)
    if humidity is not None and temperature is not None:
        #print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidi$
        tempf = (temperature * 1.8) + 32
        templevel.save_value({'value':tempf})
        humiditylevel.save_value({'value':humidity})
    else:
       print('Failed to get reading. Try again!')


def main():
    GPIO.add_event_detect(ENTER_PIN, edge=GPIO.FALLING, callback=ENTERPIN, boun$
    GPIO.add_event_detect(EXIT_PIN, edge=GPIO.FALLING, callback=EXITPIN, bounce$
    while True:
       time.sleep(600)
       TEMPCHECK()
def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        main()
    except KeyboardInterrupt:
        destroy()
