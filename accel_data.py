import serial
import time
import csv
import numpy as np
from pathlib import Path
import os

global home 

home = 'C:/users/salbertson/Documents/Make/Accelerometer/Data/'

ser = serial.Serial('COM8', baudrate = 9600, timeout = 1)
time.sleep(1)

def getValues(num_vals):
    """Get data from single serial output
    
    num_vals: a number of times to cycle through the data search, determined by number of 
        outputs specified in the Arduino code

    Returns: array containing a list with single entry that is a list containing
        time, accel.x, accel.y, accel.z as strings separated by commas
    """

    ser.write(b'g') # Send a 'g' to the Arduino to ask for data, length should match "num_vals"    
    arduinoData = [] # initialize data list
    for n in range(num_vals):
        new_val = ser.readline().decode('ascii').split('\r\n')[0]
        arduinoData.append(new_val) 

    return [arduinoData] #wrap return list in another set of brackets so csv module can interpret

def write(filename, time_tot):
    """Cycle through a specified number of serial outputs and write it to a file
    
    filename: the full path of the file

    time_tot: the total time desired for the experiment to run

    """
    userInput = input('Get data point?') # wait for user input to start taking data
    if userInput == 'y':

        with open(filename, 'w', newline = '') as writeFile: # Open new file object for writing
            writer = csv.writer(writeFile) # Create writer object with csv module
            first_data = getValues(4) # Get the first data sample
            print(first_data)
            time_start = first_data[0][0] # Define the time where data collection starts
            writer.writerows(first_data) # Write this data to the file

            while 1:
                step_data = getValues(4)
                print(step_data)
                writer.writerows(step_data)
                if float(step_data[0][0]) - float(time_start) > time_tot:
                    break

def writeFile(filePath, time_tot, time_step):
    """Calls write, mostly used to get deal with getting the desired file path for writing
    """

    if not os.path.exists(filePath):
        os.mkdir(filePath)

    index = len(os.listdir(filePath))

    csvFile = filePath + 'take' + '_' + str(index) + '.csv'

    write(csvFile, time_tot)


writeFile(home, 3, .01)