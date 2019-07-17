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
        if((len(pin_list) is not self.num_pins) or (len(dist_list) is not self.num_pins)):
            print('Too few pins or distances were entered')
            print('Fix error and try again')

        GPIO.setmode(GPIO.BCM)
        self.photo_gate_pins = pin_list  # photogate list
        self.photo_gate_distances = dist_list # distances in cm
        self.exp_count = 1

        print('Marble Track Prepping ...')

        # setup all photo gates
        for gate in pin_list:
            GPIO.setup(gate, GPIO.IN)

        print('Attaching edge listeners to PHOTOGATES ...')
        # attach seperate events
        GPIO.add_event_detect(pin_list[0], GPIO.RISING, callback=self.gate1_event)
        GPIO.add_event_detect(pin_list[1], GPIO.RISING, callback=self.gate2_event)
        GPIO.add_event_detect(pin_list[2], GPIO.RISING, callback=self.gate3_event)
        GPIO.add_event_detect(pin_list[3], GPIO.RISING, callback=self.gate4_event)
        GPIO.add_event_detect(pin_list[4], GPIO.RISING, callback=self.gate5_event)
        GPIO.add_event_detect(pin_list[5], GPIO.RISING, callback=self.gate6_event)

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

    def gate2_event(self, channel):
        self.g2_time_buf.append(time.time()) # record time
        print('PHOTOGATE # 2 Yeet !')

    def gate3_event(self, channel):
        self.g3_time_buf.append(time.time()) # record time
        print('PHOTOGATE # 3 Yeet !')

    def gate4_event(self, channel):
        self.g4_time_buf.append(time.time()) # record time
        print('PHOTOGATE # 4 Yeet !')

    def gate5_event(self, channel):
        self.g5_time_buf.append(time.time()) # record time
        print('PHOTOGATE # 5 Yeet !')

    def gate6_event(self, channel):
        self.g6_time_buf.append(time.time()) # record time
        print('PHOTOGATE # 6 Yeet !')

    # format a for row
    def __f_row__(self, gate_num, time_buf):
        row = ""
        for x in time_buf:
            elap_time = x - self.g1_time_buf[0]
            row = str(self.exp_count) + "," + gate_num + ',' + str(int(round(elap_time*1000)))
            print(str(self.exp_count) + "\t" + gate_num + '\t' + str(int(round(elap_time*1000))))
        return row

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

        # print results to user
        print('##################')
        print('##     TIME     ##')
        print('##    RESULTS   ##')
        print('##################')

        print('\n\n\nRUN\tGATE #\tTIME(MILIS)')

        # prep data
        data_buf = []
        data_buf.append( self.__f_row__(1,self.g1_time_buf) )
        data_buf.append( self.__f_row__(2,self.g2_time_buf) )
        data_buf.append( self.__f_row__(3,self.g3_time_buf) )
        data_buf.append( self.__f_row__(4,self.g4_time_buf) )
        data_buf.append( self.__f_row__(5,self.g5_time_buf) )
        data_buf.append( self.__f_row__(6,self.g6_time_buf) )

        # increment experiment
        self.exp_count += 1

        # TODO write experiment to file
        # Prepare .csv file to be imported into excel
        # *** STUDENTS EDIT HERE *** to send data to formatted text file
        # replace string with your "lastname,firstname" below.
        filename = "sanchez,andrew" + str(datetime.datetime.now()) + ".csv"
        file = open(filename , "w")
        file.write('RUN,GATE #, TIME(MILIS)\n' % self.exp_count) # write header
        for row in range(len(data_buf)): # write data in buffer
            file.write(data_buf[row] + '\n')
        print("Sent to File:\t" + filename)
        file.close()


    # define a shutdown process
    def shutdown(self):
        print('Stopping IR Sensor ...')
        GPIO.cleanup()
