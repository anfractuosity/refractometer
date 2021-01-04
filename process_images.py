#!/usr/bin/python3

import os
import cv2
import csv
import numpy as np
import math
from decimal import Decimal
from scipy import signal
import matplotlib.pyplot as plt

# Font for temperature text 
font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (100,100)
fontScale              = 2
fontColor              = (0,0,255)
lineType               = 2

# Parameters used for cropping image 
x = 1300
y = 50
w = 1024
h = 1500

# Top of scale
tpos = 182

# Zero position
zpos = 1350

# Process csv file and images of refractometer
# 
# Outputs tuple of temperatures and distance of brix line from top of scale
def process_dataset(csvname, output):

    imcount = 0
    counter = 0

    temps = []
    diffs = []

    f = open(output, 'w') 
    csv_dict = {"diff": -1, "temp": -1, "scaleheight": -1}
    wr = csv.DictWriter(f, csv_dict.keys())
    wr.writeheader()

    try:
        os.mkdir("/tmp/imgs")
    except FileExistsError:
        print("Delete /tmp/imgs first")
        quit()

    datasetfile = open(csvname)
    datasetreader = csv.reader(datasetfile)

    for row in datasetreader:

        tmp = Decimal(row[1]).quantize(Decimal("0.01")) 
        textv = "%s C" % tmp

        filen = "dataset2/%s.jpg" % row[0]
        img = cv2.imread(filen, cv2.IMREAD_GRAYSCALE)
        if img is None:
            break
        
        rows,cols = img.shape
        M = cv2.getRotationMatrix2D((cols/2,rows/2),160,1)
        dst = cv2.warpAffine(img,M,(cols,rows))

        crop_img = dst[y:y+h, x:x+w]
        img = crop_img

        # Get mean across horizontal axis
        m = np.mean(crop_img[0:0+h, 0:0+w], axis=1)    

        # Find last important peak
        sig, _ = signal.find_peaks(-m)
        prominences = signal.peak_prominences(-m, sig)[0]
        z = np.argwhere(prominences > 0.5)
        pos_x = sig[z[-1][0]]
 
        # Add lines denoting current position of brix line etc.
        crop_img = np.swapaxes(np.array([m]*w),0,1)
        crop_img = cv2.cvtColor(crop_img.astype(np.uint8), cv2.COLOR_GRAY2BGR)
        crop_img = cv2.line(crop_img, (0, pos_x), (w, pos_x), (0, 0, 255), 4)
        crop_img = cv2.line(crop_img, (0, zpos), (w, zpos), (0, 255, 0), 4)
        crop_img = cv2.line(crop_img, (0, tpos), (w, tpos), (255, 0, 0), 4)

        cv2.putText(crop_img,textv, 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)

        img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_GRAY2BGR)
        img = cv2.line(img, (0, zpos), (w, zpos), (0, 255, 0), 4)
        img = cv2.line(img, (0, tpos), (w, tpos), (255, 0, 0), 4)

        # Only use first 100 images in dataset and only write image if detected line is below zero line (as it 
        # must be during calibration)
        if counter <= 100 and pos_x > zpos:
            current_diff_from_top_scale = pos_x - tpos
            scale_height = zpos - tpos
            if True:
            #if len(diffs) == 0 or current_diff_from_top_scale > diffs[-1]:
                temps.append(float(tmp))
                diffs.append(current_diff_from_top_scale)
                csv_dict = {"diff": current_diff_from_top_scale, "temp": tmp, "scaleheight": scale_height}
                print(csv_dict)
                wr.writerow(csv_dict)
                f.flush()

                cv2.imwrite('/tmp/imgs/%s_a.jpg' % row[0], cv2.hconcat([crop_img, img]))
                cv2.imwrite('/tmp/imgs/%d.jpg' % imcount, cv2.hconcat([crop_img, img]))

                imcount += 1

        counter += 1

    return temps, diffs

def temp_correction(temps, diffs, temp):

    p = np.polyfit(temps, diffs, 3)
    polynomial = np.poly1d(p)

    x_axis = np.linspace(20,70)
    y_axis = polynomial(x_axis)
    plt.figure(1)
    plt.plot(x_axis, y_axis)
    plt.show()

    return np.poly1d(p)(temp)

if __name__ == "__main__":
    temps, diffs = process_dataset("dataset2.csv", "out.csv")
    
    current_diff_from_top_scale = 1284
    current_temp = 70.31
    scale_height = 1170
    
    brix = (1 - ((current_diff_from_top_scale - (temp_correction(temps, diffs, current_temp) - scale_height)) / scale_height)) * 32
    print(brix,"brix")
