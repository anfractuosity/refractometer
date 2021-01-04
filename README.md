# refractometer

Inline refractometer software.  The refractometer.py script captures images from the Pi camera
as well as capturing the temperature and storing information in a CSV file.

See https://www.anfractuosity.com/projects/diy-inline-refractometer/ for more details.

# Pi setup for image capture 

Use raspi-config to enable 1-wire interface and camera.

```
sudo apt-get update
sudo apt-get install python3-pip
pip3 install picamera
```

# Setup for image processing test

You probably need to do something like the following to process the images which you collected:

```
pip3 install opencv-python
python3 process_images.py
```
 
# To Do

* See if the tracking of the brix line can be improved
