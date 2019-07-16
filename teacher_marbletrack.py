import RPi.GPIO as GPIO
import time

class MarbleTrack():
    # constants
    num_pins = 6

    # pin list refers to the GPIO pins we are using for the photo gates
    # ex. [21, 16, 6, 12, 24, 17]
    # pin 21 should be PHOTO GATE #1, pin 16 should be PHOTO GATE #2,
    # pin 6 should be PHOTO GATE #3, ...
    # dist list refers to the distance of each gate in cm. Starting distance 0
    # should be at Gate #1
    # ex. [0, 12, 24, 36, 48, 60]
    def __init__(self, pin_list, dist_list):

        # expected list count error
        if((len(pin_list) is not num_pins) or (len(dist_list) is not num_pins)):
            print('Too few pins or distances were entered')
            print('Fix error and try again')
            break

        GPIO.setmode(GPIO.BCM)
        self.photo_gate_pins = pin_list  # photogate list
        self.photo_gate_distances = dist_list # distances in cm
        self.exp_count = 1

        print('Marble Track Prepping ...')

        # setup all photo gates
        for gate in photo_gate_pins:
            GPIO.setup(gate, GPIO.IN)

        print('Attaching edge listeners to PHOTOGATES ...')
        # attach seperate events
        GPIO.add_event_detect(photo_gate_pins[0], GPIO.RISING, callback=self.gate1_event)
        GPIO.add_event_detect(photo_gate_pins[1], GPIO.RISING, callback=self.gate2_event)
        GPIO.add_event_detect(photo_gate_pins[2], GPIO.RISING, callback=self.gate3_event)
        GPIO.add_event_detect(photo_gate_pins[3], GPIO.RISING, callback=self.gate4_event)
        GPIO.add_event_detect(photo_gate_pins[4], GPIO.RISING, callback=self.gate5_event)
        GPIO.add_event_detect(photo_gate_pins[5], GPIO.RISING, callback=self.gate6_event)

        print('Creating time buffers for each GATE ...')
        self.g1_time_buf = []
        self.g2_time_buf = []
        self.g3_time_buf = []
        self.g4_time_buf = []
        self.g5_time_buf = []
        self.g6_time_buf = []

        print('Done !')
        print('Type exp.start_exp() to start gathering data :)')
        print('or')
        print('To check that all your gates are working try running a marble')
        print('and see if you get all the gates to  Yeet! ')

    def gate1_event(self, channel):
        self.g1_time_buf.append(time.time()) # record time
        print('PHOTOGATE # 1 Yeet !')

    def gate1_event(self, channel):
        self.g2_time_buf.append(time.time()) # record time
        print('PHOTOGATE # 2 Yeet !')

    def gate1_event(self, channel):
        self.g3_time_buf.append(time.time()) # record time
        print('PHOTOGATE # 3 Yeet !')

    def gate1_event(self, channel):
        self.g4_time_buf.append(time.time()) # record time
        print('PHOTOGATE # 4 Yeet !')

    def gate1_event(self, channel):
        self.g5_time_buf.append(time.time()) # record time
        print('PHOTOGATE # 5 Yeet !')

    def gate1_event(self, channel):
        self.g6_time_buf.append(time.time()) # record time
        print('PHOTOGATE # 6 Yeet !')

    # experiment
    def start_exp(self):
        # clear gate time buffers
        del self.g1_time_buf[:]
        del self.g2_time_buf[:]
        del self.g3_time_buf[:]
        del self.g4_time_buf[:]
        del self.g5_time_buf[:]
        del self.g6_time_buf[:]

        start_time = 0

        print('Marble Track Ready, Waiting for you to drop a marble !\n\n')

        # run experiment until last piece of data at gate 6 is collected
        while (len(self.g6_time_buf) is 0):pass

        print('Experiment %d Success!' % self.exp_count)

        # extract times from buffer
        elap_times = []    # list of string formatted times
        for times in self.time_buf:
            # find the elapsed time
            elap = times - self.time_buf[0]  # elap_time = end_time - start_time

            # formatting universal time into human readable time
            elap_times.append(int(round(elap * 1000)))

        # print results to user
        print('##################')
        print('##     TIME     ##')
        print('##    RESULTS   ##')
        print('##################')
        for x in range(0,len(elap_times),1):
            print('TIME # %d \t %s' % (x, str(elap_times[x])))

        # TODO write experiment to file
        self.exp_count += 1

    # define a shutdown process
    def shutdown(self):
        print('Stopping IR Sensor ...')
        GPIO.cleanup()
