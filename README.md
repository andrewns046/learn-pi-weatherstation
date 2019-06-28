# Learn to Build a Raspberry Pi Weather Station !
Part List:
- DHT11 (Temperature & Humidity Sensor)
- 2 Buttons
- 4 LEDs
- 4 43 Ohm resistors
- 2 10k Ohm resistors
- 1 4.7k Ohm resistor
- Jumper Wires
- Breadboard
- Raspberry Pi

### Wiring Diagram
TODO

### Example output
TODO

### System State Diagram/Flowchart
The diagram below demonstrates the logic of our system and the processes that
take place when events are triggered.
![alt text](https://raw.githubusercontent.com/tonikhd/learn-pi-weatherstation/master/weatherstation_flowchart.png)

### Installation
Installing libraries with Python 3 and pip:
```
sudo apt-get update
sudo apt-get install python3-pip
sudo python3 -m pip install --upgrade pip setuptools wheel

sudo pip3 install Adafruit_DHT
```
Clone this repository into your working directory:
```
git clone https://github.com/tonikhd/learn-pi-weatherstation.git
cd learn-pi-weatherstation
```

### Running the program
Before you run:

Once everything is installed locate the weatherstation.py script by looking at
the contents of your directory:
`ls -l`

Open the script and located the section labeled **STUDENT EDIT HERE*** towards
the bottom of the script. Make sure to follow the instructions and save the file
by hitting CtrlX -> type[y] -> press [enter]:
`sudo nano weatherstation.py`

Run the program with:
`sudo python3 weatherstation.py`
