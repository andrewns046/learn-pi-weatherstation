class BlinkCounter():

    def __init__(self, led_pin, ir_pin):
        import RPI.GPIO as GPIO
        import time
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(led_pin, GPIO.OUT)
        GPIO.setup(ir_pin, GPIO.IN)

        self.led_pin = led_pin
        self.count = 0
        self.on = True


    # blinks led count amount of times
    def poll(self):
        import RPI.GPIO as GPIO
        while(self.on):
            if( GPIO.input(self.ir_pin) ):
                self.count += 1

            # equivalent to all the timing we will be doing
            for i in range(100):pass

    def blink(self, blinks):
        import RPI.GPIO as GPIO
        for i in range(blinks):
            GPIO.output(self.led_pin, GPIO.HIGH)


    def shutdown(self):
        import RPI.GPIO as GPIO
        import time
        self.on = False
        print('Stopping IR Sensor')
        time.sleep(.5)
        print('The led should blink %d times' % self.count)
        self.blink(self.count)
        GPIO.cleanup()
