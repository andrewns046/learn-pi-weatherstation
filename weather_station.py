'''
Author: Andrew N. Sanchez
Date: June 25, 2019
Last Modified: June 25, 2019
Title: Weather Station

Project Description: Raspberry Pi weather station that gathers data and prepares
text file that can be imported to Excel/LibreOffice.
'''
import sys
import Adafruit_DHT
import datetime
from threading import Event
from threading import Thread
import time
import RPi.GPIO as GPIO

# Initialize DHT11 sensor
sensor = Adafruit_DHT.DHT11;

# System pinout
reset_led = 23
stop_led = 24
heat_led = 13
less23_led = 6  # LED indicating Room Temperature( < 23 C)
reset_btn = 26
stop_btn = 19
data_pin = 21

# Setup events
shutdown = Event()
reset = Event()

# Define system variables
period = 2   # delay seconds for sensor
sens_r = 15   # sensor retries
time_elap = 0
temp_limit = 23 # DEFAULT temp limit room temperature 23 C
data_buf = []
humid = 0.0
temp = 0.0

# Raspberry Pi Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# LEDs
GPIO.setup(reset_led, GPIO.OUT)
GPIO.setup(stop_led, GPIO.OUT)
GPIO.setup(heat_led, GPIO.OUT)
GPIO.setup(less23_led, GPIO.OUT)
# Buttons
GPIO.setup(reset_btn, GPIO.IN)
GPIO.setup(stop_btn, GPIO.IN)

# Reset button has been pressed reinitialize data and reset time_elap
def reset_event(channel):
    GPIO.output(reset_led, GPIO.HIGH)
    global reset
    reset.set() # trigger reset event

# Stop button has been pressed stop main loop
def stop_event(channel):
    GPIO.output(stop_led, GPIO.HIGH)
    global shutdown
    shutdown.set() # trigger shutdown event

def take_measurement():
    global humid
    global temp
    humid, temp = Adafruit_DHT.read_retry(sensor, data_pin, sens_r, period)

#attach interrupts to buttons
GPIO.add_event_detect(reset_btn, GPIO.FALLING, callback=reset_event)
GPIO.add_event_detect(stop_btn, GPIO.FALLING, callback=stop_event)

# initialize LEDs
GPIO.output(heat_led, GPIO.LOW)
GPIO.output(less23_led, GPIO.LOW)
GPIO.output(reset_led, GPIO.LOW)
GPIO.output(stop_led, GPIO.LOW)

print('Time(Seconds)\tTemperature(C)\tHumidity(%)')

# Main loop
while not shutdown.is_set():
    # AQUIRE data at a frequency of .5Hz
    #humid, temp = Adafruit_DHT.read_retry(sensor, data_pin, sens_r, period)

    measure_t = Thread(target=take_measurement)
    counter = 0
    measure_t.start()
    print('|', end='')
    while measure_t.is_alive():
        print('|', end='', flush=True)
        counter += 1
        time.sleep(1)
    print('|')
    time_elap += (counter) # increment time

    if not humid == None and not temp == None: # run if data recieved

        if reset.is_set():  # clear data and reset time
            del data_buf[:]
            time_elap = 0
            reset.clear() # reset internal flag to false
            GPIO.output(reset_led, GPIO.LOW)

    # PROCESS and RECORD data
        row = str(time_elap) + ', ' + str(temp) + ', ' + str(humid)
        data_buf.append(row)

    # DISPLAY data and change LED Indicators
        print('%4.2f seconds,\t %4.2f *Celsius,\t %4.2f percent' % (time_elap, temp, humid))
        if temp > temp_limit:
            GPIO.output(heat_led, GPIO.HIGH)
            GPIO.output(less23_led, GPIO.LOW)
        else:
            GPIO.output(heat_led, GPIO.LOW)
            GPIO.output(less23_led, GPIO.HIGH)
    else:
        print('Sensor missed data for\t t = %4.2f seconds' % (time_elap))

# initialize shutdown sequence
print('Halting system ...\nLast Value Recorded:\t')
GPIO.output(heat_led, GPIO.LOW)
GPIO.output(less23_led, GPIO.LOW)
GPIO.output(reset_led, GPIO.LOW)

# Prepare .csv file to be imported into excel
# *** STUDENTS EDIT HERE *** to send data to formatted text file
# replace string with your "lastname,firstname" below.
filename = "sanchez,andrew" + str(datetime.datetime.now()) + ".csv"
file = open(filename , "w")
file.write('Time(Seconds), Temperature(C), Humidity(%)\n') # write header
for row in range(len(data_buf)): # write data in buffer
    file.write(data_buf[row] + '\n')
print("Sent to File:\t" + filename)
file.close()

GPIO.cleanup() # end program
