########################################
#### BerryRocket ####
# On-board code for BR Micro-Avionic
# Louis Barbier
# MIT License
########################################

import time
from machine import Pin, I2C, PWM

from lib.bmp180.bmp180 import BMP180
from lib.mpu6050.mpu6050 import *

#### Initialisation
# I2C connection init
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
# Barometer init
bmp = BMP180(i2c)
# IMU init
imu = MPU6050(bus=0, sda=Pin(4), scl=Pin(5), freq=400000, gyro=GYRO_FS_2000, accel=ACCEL_FS_16)

# Variables
launch_detected = False

# Infinite loop
while True:
    # Get time in second
    timetag = time.ticks_ms()/1000.0

    # Read sensor values
    pressure = bmp.pressure
    temperature = bmp.temperature
    ax, ay, az, gx, gy, gz = imu.data

    # Create one line with revelant values from sensors
    relevant_data = "Time: {:.2f} s | AccY: {:.2f} g | Baro: {:.2f} mBar | Temperature: {:.2f} °C".format(timetag, ay, pressure, temperature)

    # Detection of launch is acceleration of Y axis is greater than 1.5 g
    if ay > 1.5:
          launch_detected = True
    
    # Write data to file after launch
    if launch_detected == True:
        with open('data.txt', 'a') as fp:
            fp.write(relevant_data + "\r\n")

    # Print data in terminal (optional, can be ommited to speed up the program)
    print(relevant_data + "\r\n")
