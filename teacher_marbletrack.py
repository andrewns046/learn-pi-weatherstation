import RPi.GPIO as GPIO
import time

class MarbleTrack():
    
    # pin list refers to the GPIO pins we are using for the photo gates
    # ex. [21, 16, 6, 12, 24, 17]
    # pin 21 should be PHOTO GATE #1, pin 16 should be PHOTO GATE #2,
    # pin 6 should be PHOTO GATE #3, ...
    def __init__(self, pin_list):
        GPIO.setmode(GPIO.BCM)
    
        self.photo_gates = pin_list  # photogate list
        self.time_buf = []  # list to hold times
        self.num_gates = len(pin_list) # number of gates on Marble Track
        self.edge_count = 0
        self.exp_count = 1
        
        # setup all photo gates
        for gate in self.photo_gates:
            GPIO.setup(gate, GPIO.IN)
            GPIO.add_event_detect(gate, GPIO.RISING, callback=self.ris_trigger)
        
    
    # trigger when rising is detected
    def ris_trigger(self, channel):
        self.edge_count += 1  # record edge
        self.time_buf.append(time.time()) # record time
        print('Yeet !')  # I love Bobby <3
    
    # Description:
    # Step 1: Drop marble into marble track
    # Step 2: Start timing when marble reaches PHOTO GATE #1
    def start_exp(self):
        # clear variables
        self.edge_count = 0
        del self.time_buf[:]
        start_time = 0
        
        print('Marble Track Ready !\n\n')
        print('Timeout in 4 seconds ...')
        time.sleep(4)  # wait marble to go through track
        
        print('Experiment %d Success!' % self.exp_count)
        
        # extract times from buffer
        elap_times = []    # list of string formatted times
        for times in self.time_buf:
            # find the elapsed time
            elap = times - self.time_buf[0]  # elap_time = end_time - start_time
            
            # formatting universal time into human readable time
            elap_times.append(time.strftime("%H:%M:%S:%f", time.gmtime(elap)))
     
        # print results to user
        print('##################')
        print('##     TIME     ##')
        print('##    RESULTS   ##')
        print('##################')
        for x in range(0,len(elap_times),1):
            print('TIME # %d \t %s' % (x, elap_times[x]))
        
        # TODO write experiment to file
         
    
    # define a shutdown process
    def shutdown(self):
        print('Stopping IR Sensor ...')
        GPIO.cleanup()

