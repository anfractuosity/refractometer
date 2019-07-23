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

```
pip3 install opencv-python
```

 
