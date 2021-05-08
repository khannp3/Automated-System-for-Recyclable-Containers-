import time
import random
import sys
sys.path.append('../')

from Common_Libraries.p3b_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim():
    try:
        my_table.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

### Constants
speed = 0.2 #Qbot's speed

### Initialize the QuanserSim Environment
my_table = servo_table()
arm = qarm()
arm.home()
bot = qbot(speed)

##---------------------------------------------------------------------------------------
## STUDENT CODE BEGINS
##---------------------------------------------------------------------------------------
container_load = 0
total_mass = 0
container_att = 0
coordinates = 0
bin_ids = []
dispense = False

# Dispense random container and determine attributes.
def dispense_container():
    global container_load
    global total_mass
    global container_att
    global coordinates
    global dispense

    if dispense == False:
        container_att = my_table.container_properties(random.randrange(1,6))
        my_table.dispense_container()
        dispense = True

    if container_load == 0: coordinates = [-0.08, -0.395, 0.3769]
    elif container_load == 1: coordinates = [0.0, -0.3900, 0.3769]
    elif container_load == 2: coordinates = [0.08, -0.3900, 0.37]
    
    container_load += 1
    total_mass += container_att[1]
    bin_ids.append(container_att[2])
    
    return container_att, total_mass, container_load, coordinates



def load_container():    
    global container_load
    global total_mass
    global bin_ids
    global coordinates
    global dispense
    
#If statements return False do not do anything, if True move to pickup:
    while True:

        if bin_ids[0] != bin_ids[-1]:     # A container with a different ID is in the hopper
            container_load = 0
            total_mass = 0
            print("Different bin ID")
            return False
    
        elif container_load > 3:               # Three containers are already in the hopper.
            container_load = 0
            total_mass = 0
            print("3 containers on qbot")
            return False
    
        elif total_mass > 90:                # Total mass of all container are less than 90 grams.
            total_mass = 0
            container_load = 0
            print("Mass exceeded")
            return False
        else:
            time.sleep(0.8)
            arm.move_arm(0.6333, 0.0, 0.2390)
            time.sleep(0.8)
            arm.control_gripper(45)
            time.sleep(0.8)
            arm.rotate_shoulder(-30)
            time.sleep(0.8)
            arm.move_arm(coordinates[0],coordinates[1],coordinates[2])
            time.sleep(0.8)
            arm.control_gripper(-20)
            time.sleep(0.8)
            arm.rotate_elbow(-50)
            time.sleep(0.8)
            arm.home()
            dispense = False

            dispense_container()

    
            

# transfers container to the correct recycling station
def transfer_container(bin_id):
    
    lines = 0
    bot.activate_ultrasonic_sensor()
    
    if bin_id is "Bin01":
        dist = 0.5
        time = 2
    elif bin_id is "Bin02":
        dist = 0.4
        time = 1.9
    elif bin_id is "Bin03":
        dist = 0.3
        time = 1.8
    elif bin_id is "Bin04":
        dist = 0.2
        time = 1.7

    while lines < 3:
        lines, velocity = bot.follow_line(0.2)
        bot.forward_velocity(velocity)
        distance = bot.read_ultrasonic_sensor(bin_id)
        
        if dist >= distance:
            bot.forward_time(time)
            bot.stop()
            bot.deactivate_ultrasonic_sensor()
            break


#qbot moves adjacent to the bin and dumps out the contents
def deposit_container(bin_id):
    
    bot.rotate(90)
    
    if bin_id is "Bin01": time = 2.1
    elif bin_id is "Bin02": time = 1.6
    elif bin_id is "Bin03": time = 1
    elif bin_id is "Bin04": time = 0.5
        
    bot.forward_time(time)
    bot.rotate(-90)

    bot.activate_actuator()
    bot.dump()
    bot.deactivate_actuator()

    bot.rotate(-90)
    bot.forward_time(time)
    bot.rotate(90)


#qbot follows trajectory of yellow line until returning to home position
def return_home():
    print("Returning home")
    global bin_ids
    lines = 0
    
    while lines < 4:
        lines, velocity = bot.follow_line(0.15)
        bot.forward_velocity(velocity)
    bot.forward_time(0.5)
    bot.rotate(187)
    bin_ids = [bin_ids[-1]]


#calling upon the functions

while True:
    print("Starting next round")
    dispense_container()
    load_container()
    transfer_container(bin_ids[0])
    deposit_container(bin_ids[0])
    return_home()
    print("I have returned home")


##---------------------------------------------------------------------------------------
## STUDENT CODE ENDS
##---------------------------------------------------------------------------------------
update_thread = repeating_timer(2,update_sim)

