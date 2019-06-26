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
import time
import RPI.GPIO as GPIO

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

# Raspberry Pi Setup
GPIO.setmode(GPIO.BCM)
# LEDs
GPIO.setup(reset_led, GPIO.OUT)
GPIO.setup(stop_led, GPIO.OUT)
GPIO.setup(heat_led, GPIO.OUT)
GPIO.setup(less23_led, GPIO.OUT)
# Buttons
GPIO.setup(reset_btn, GPIO.IN)
GPIO.setup(stop_btn, GPIO.IN)
#attach interrupts to buttons
GPIO.add_event_detect(reset_btn, GPIO.FALLING, callback=reset_event)
GPIO.add_event_detect(stop_btn, GPIO.FALLING, callback=stop_event)


# Reset button has been pressed reinitialize data and reset time_elap
def reset_event(channel):
    GPIO.output(reset_led, GPIO.HIGH)
    data_buf.clear()
    time_elap = 0
    GPIO.output(reset_led, GPIO.LOW)

# Stop button has been pressed stop main loop
def stop_event(channel):
    GPIO.output(stop_led, GPIO.HIGH)
    run = False
    GPIO.output(stop_led, GPIO.LOW)

# sends data to text file that can be imported to Excel/LibreOffice
def to_file():
    file f

# Define system variables
freq = 2    # 2 seconds
time_elap = 0
data_buf = []
run = True

print('Time(Seconds)\tTemperature(C)\tHumidity(%)')
# Main loop
while run:
    # Aquire Data
    humid, temp = Adafruit_DHT.read_retry(sensor, data_pin)

    # Change LED states
    if temp > 23:
        GPIO.ouput(heat_led, GPIO.HIGH)
        GPIO.output(less23_led, GPIO.LOW)
    else
        GPIO.ouput(heat_led, GPIO.LOW)
        GPIO.output(less23_led, GPIO.HIGH)

    # Display and record data
    row = time_elap + '\t' + temp + '\t' + humid
    data_buf.append(row)
    print(row)

    time.sleep(2000)  # Wait 2 seconds due to .5Hz temp sensor
    time_elap += 2

# initialize shutdown sequence
GPIO.ouput(heat_led, GPIO.LOW)
GPIO.output(less23_led, GPIO.LOW)
GPIO.ouput(reset_led, GPIO.LOW)
GPIO.output(stop_led, GPIO.HIGH)
# send data to formatted text file
to_file()
GPIO.ouput(stop_led, GPIO.LOW)
GPIO.cleanup() # end program
