import RPi.GPIO as GPIO
import time

class BlinkCounter():
    
    # pin list refers to the GPIO pins we are using for the photo gates
    # ex. [21, 16, 6, 12, 24, 17]
    # pin 21 should be PHOTO GATE #1, pin 16 should be PHOTO GATE #2,
    # pin 6 should be PHOTO GATE #3, ...
    def __init__(self, ir_pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ir_pin, GPIO.IN)
        self.ir_pin = ir_pin
        
        # self.photo_gates = pin_list
        
        '''
        # setup all photo gates
        for gate in self.photo_gates:
            GPIO.setup(gate, GPIO.IN)
            GPIO.add_event_detect(gate, GPIO.RISING, callback=self.ris_trigger)
        '''
        GPIO.add_event_detect(ir_pin, GPIO.RISING, callback=self.ris_trigger)
        
        self.edge_count = 0
    
    # trigger when rising is detected
    def ris_trigger(self, channel):
        self.edge_count += 1
        print('Yeet !')  # I love Bobby <3
    
    # Description:
    # Step 1: Drop marble into marble track
    # Step 2: Start timing when marble reaches PHOTO GATE #1
    def start_exp(self, timeout):pass
        
    
    # define a shutdown process
    def shutdown(self):
        print('Stopping IR Sensor ...')
        print('Counted %d times' % (self.edge_count))
        GPIO.cleanup()
