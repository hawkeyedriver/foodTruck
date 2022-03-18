"""Configure Touch Display & Run Restaurant Scripts"""

import os
print("Running through command line")
os.system("xinput map-to-output 11 DSI-1")
os.system("xinput map-to-output 10 HDMI-1")
os.system("sudo python3 /home/pi/Desktop/FoodTruck_BackupV2/POS_Python/cashierMain.py " +
"& python3 /home/pi/Desktop/FoodTruck_BackupV2/POS_Python/cookMain.py")


