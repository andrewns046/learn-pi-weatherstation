# TODO blink one led with polling and the other with edge trigger

class BlinkCounter():

    def __init__(self, rled_pin, gled_pin, ir_pin):
        import RPi.GPIO as GPIO
        import time
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(rled_pin, GPIO.OUT)
        GPIO.setup(gled_pin, GPIO.OUT)
        GPIO.setup(ir_pin, GPIO.IN)

        self.rled_pin = rled_pin
        self.ir_pin = ir_pin
        self.gled_pin = gled_pin
        
        GPIO.add_event_detect(ir_pin, GPIO.RISING, callback=self.ris_trigger)
        
        self.poll_count = 0
        self.edge_count = 0
        self.on = True
        
    def ris_trigger(self, channel):
        self.edge_count += 1
        

    # blinks led count amount of times
    def poll(self):
        import RPi.GPIO as GPIO
        import time
        while (self.on):
            if( GPIO.input(self.ir_pin) ):  # if signal is high
                self.poll_count += 1
                # blink red led
                GPIO.output(self.rled_pin, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(self.rled_pin, GPIO.LOW)
            
    # shutdown process
    def shutdown(self):
        import RPi.GPIO as GPIO
        import time
        self.on = False
        print('Stopping IR Sensor ...')
        print('The red led blinked %d times and the green led blinked %d times' % (self.poll_count, self.edge_count))
        GPIO.cleanup()
