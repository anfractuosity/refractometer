#!/usr/bin/python3

import datetime
from picamera import PiCamera
from time import sleep
from fractions import Fraction
from temp import *
import csv

sec = 0.1

camera = PiCamera(resolution=(2592, 1944),framerate=Fraction(1.0/sec))
camera.shutter_speed = int(1000000 * sec)
camera.iso = 100
camera.exposure_mode = 'off'
   
csvf = open('images.csv', 'w', newline='\n') 

fieldnames = ['time','temp','image']
writer = csv.DictWriter(csvf, fieldnames=fieldnames,quoting=csv.QUOTE_NONNUMERIC)

writer.writeheader()
 
def takephoto(imgstr):
    camera.capture(imgstr)

while True:

    ctime = datetime.datetime.now().timestamp()
    tempv = read_temp()
    imgstr = "images/%d.jpg" % ctime 
    
    takephoto(imgstr)

    writer.writerow({'time': ctime, 'temp': tempv[0],'image':imgstr})

    csvf.flush()
     
    sleep(10)
