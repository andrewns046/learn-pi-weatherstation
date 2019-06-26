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
from threading import Event
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

# Setup shutdown event
shutdown = Event()

# Define system variables
freq = 1.8    #2 seconds
time_elap = 0
data_buf = []

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
    global data_buf
    global time_elap
    time_elap = -2
    del data_buf[:]
    print 'Resetting system ... \t' +  str(data_buf)
    GPIO.output(reset_led, GPIO.LOW)

# Stop button has been pressed stop main loop
def stop_event(channel):
    GPIO.output(stop_led, GPIO.HIGH)
    global shutdown
    shutdown.set() #trigger event shutdown
    print('Halting system ...\nLast value recorded will be printed but not added to data:')

#attach interrupts to buttons
GPIO.add_event_detect(reset_btn, GPIO.FALLING, callback=reset_event)
GPIO.add_event_detect(stop_btn, GPIO.FALLING, callback=stop_event)


# sends data to text file that can be imported to Excel/LibreOffice
def to_file():
    print('sent to file')

# initialize LEDs
GPIO.output(heat_led, GPIO.LOW)
GPIO.output(less23_led, GPIO.LOW)
GPIO.output(reset_led, GPIO.LOW)
GPIO.output(stop_led, GPIO.LOW)

print('Time(Seconds)\tTemperature(C)\tHumidity(%)')
# Main loop
while not shutdown.is_set():
    # AQUIRE Data
    # Returns values every 2 seconds due to .5Hz temp sensor
    humid, temp = Adafruit_DHT.read_retry(sensor, data_pin)

    # PROCESS and RECORD data
    row = str(time_elap) + '\t' + str(temp) + '\t' + str(humid)
    data_buf.append(row)
    time_elap += freq

    #DISPLAY data
    print(row)
    # Change LED states
    if temp > 23:
        GPIO.output(heat_led, GPIO.HIGH)
        GPIO.output(less23_led, GPIO.LOW)
    else:
        GPIO.output(heat_led, GPIO.LOW)
        GPIO.output(less23_led, GPIO.HIGH)

# initialize shutdown sequence
GPIO.output(heat_led, GPIO.LOW)
GPIO.output(less23_led, GPIO.LOW)
GPIO.output(reset_led, GPIO.LOW)
# send data to formatted text file
to_file()
GPIO.cleanup() # end program
