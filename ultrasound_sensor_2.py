# Importing the required libraries
import RPi.GPIO as GPIO
import time
from libdw import pyrebase

# Set up firebase
url = "https://dw-keyboard-warriors.firebaseio.com/"
apikey = "AIzaSyCho_88MLCkNDOGGEE9tmGvObj54HKFd8Q"
config = {"apiKey": apikey, "databaseURL": url}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

 
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
# Set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # Set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # Set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # Save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # Save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # Time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # Multiply with the speed of sound (34300 cm/s)
    # Divide it by 2, because it is reflected back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
# 
if __name__ == '__main__':
    try:
        while True:
            # Measure the distance from the ultrasound sensor
            dist = distance()
            # Upload the information onto firebase
            db.child("1D_final").child("MS2").set(dist)
            # Print out the measured distance
            print("Measured Distance 2 = {:.1f} cm".format(dist))
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()