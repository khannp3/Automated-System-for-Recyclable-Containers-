import sys
sys.path.append('../')
import time
from Common_Libraries.p0_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        my_qbot.ping()
    except Exception as error_update_sim:
        print (error_update_sim)


speed = 0.1 # in m/s
my_qbot = qbot(speed)
update_thread = repeating_timer(2, update_sim)

# ---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
# ---------------------------------------------------------------------------------

start_time = time.time()  # takes initial time

# First leg, leaving start moving west
my_qbot.travel_forward(0.3)
my_qbot.rotate(-90)

# Moving south, turn east
my_qbot.travel_forward(0.25)
my_qbot.rotate(-105)

# Moving east, turn north
my_qbot.travel_forward(0.3)
my_qbot.rotate(-90)

# Moving north, turn west
my_qbot.travel_forward(0.2)
my_qbot.rotate(-100)

# Final leg moving west
my_qbot.travel_forward(0.8)

end_time = time.time()  # takes final time
print(end_time - start_time)  # reports time difference
