#!/usr/bin/python3

import sys
import os


output_device = int(input("Which device? 0 for built-in speakers, 1 for headphones: "))
if output_device == 0:
    print("Built-in audio selected")
elif output_device == 1:
    print("Headphones selected")
else:
    print("Invalid output_device selected. Please enter 0 or 1")
    exit()

volume = int(input("What volume level? (ex. 150): "))

if 0 <= volume <= 200:
    print("Setting volume to " + str(volume))
    my_command = "pactl set-sink-volume " + str(output_device) + " " + str(volume) + "%"
    output = os.popen(my_command).read()

else:
    print("Please enter integer between 0 and 200")
