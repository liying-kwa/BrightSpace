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
GPIO_TRIGGER = 17
GPIO_ECHO = 23
GPIO_REDLED = 5
GPIO_GREENLED = 6 
GPIO_YELLOWLED = 16
GPIO_BUTTON = 21
 
# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_REDLED, GPIO.OUT)
GPIO.setup(GPIO_GREENLED, GPIO.OUT)
GPIO.setup(GPIO_YELLOWLED, GPIO.OUT)
GPIO.setup(GPIO_BUTTON, GPIO.IN, GPIO.PUD_DOWN)
 
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
 
# If the file being run is the main file
if __name__ == '__main__':
    try:
        # Check initial f3l1 state (whether the seat is occupied or not)
        f3l1 = db.child("1D_final").child("floor3").child("led1").get().val()
        if f3l1 == "occupied":
            # If the seat is occupied, the red LED is lit
            f3l1_state = True
            GPIO.output(GPIO_REDLED, GPIO.HIGH)
            GPIO.output(GPIO_GREENLED, GPIO.LOW)
            GPIO.output(GPIO_YELLOWLED, GPIO.LOW)
        else:
            # If the place is unoccupied, the green LED is lit
            f3l1_state = False
            GPIO.output(GPIO_GREENLED, GPIO.HIGH)
            GPIO.output(GPIO_REDLED, GPIO.LOW)
            GPIO.output(GPIO_YELLOWLED, GPIO.LOW)
        # Initialize the counter as 0
        # The counter represents the number of times in which
        # the reading by both of Ultrasound sensors are consistent
        counter = 0
        while True:
            # Measure the distance from ultrasound sensor
            dist = distance()
            # Obtain the distance measured by the
            # second ultrasound sensor from firebase
            dist2 = db.child("1D_final").child("MS2").get().val()
            # Print out the distances measured by each Ultrasound sensor
            print ("Measured Distance 1 = {:.1f} cm, Measured Distance 2 = {:.1f}".format(dist,dist2))
            
            # If the seat is unoccupied
            if f3l1_state == False:
                # Check if the counter is 3 (3 consistent readings obtained)
                # This suggests that the seat is now occupied
                if counter == 3:
                    #Turn on the red LED, and change the state of the floor
                    f3l1_state = True
                    GPIO.output(GPIO_GREENLED, GPIO.LOW)
                    GPIO.output(GPIO_REDLED, GPIO.HIGH)
                    # Reset the counter to 0
                    counter = 0
                    # Upload the information to firebase
                    db.child("1D_final").child("floor3").child("led1").set("occupied")
                # If both Ultrasound detects that the seat is occupied
                elif dist <  30 and dist2 < 30:
                    # Increase the counter by 1.
                    counter += 1
                # Otherwise, reset the counter to 0
                else:
                    counter = 0
                    
            # If the seat is occupied
            if f3l1_state == True:
                # Check if the counter is 3 (3 consistent readings obtained)
                # This suggests that the seat is now unoccupied
                if counter == 3:
                    # Turn on the green LED, and change the state of the floor
                    f3l1_state = False
                    GPIO.output(GPIO_REDLED, GPIO.LOW)
                    GPIO.output(GPIO_GREENLED, GPIO.HIGH)
                    # Reset the counter to 0
                    counter = 0
                    # Upload the information to firebase
                    db.child("1D_final").child("floor3").child("led1").set("unoccupied")
                # If both Ultrasound detects that the seat is unoccupied
                elif dist > 30 and dist2 > 30:
                    # Increase the counter by 1
                    counter += 1
                # Otherwise, reset the counter to 0
                else:
                    counter = 0
                
                # If the yellow button is pressed while the seat is occupied
                if GPIO.input(GPIO_BUTTON) == GPIO.HIGH:
                    # Print that the button is pressed
                    print("button pressed :)")
                    # Turn on the yellow LED after a 1 second delay
                    time.sleep(1)
                    GPIO.output(GPIO_REDLED, GPIO.LOW)
                    GPIO.output(GPIO_YELLOWLED, GPIO.HIGH)
                    # Initialise the start_time to be the current time
                    start_time = time.time()
                    while True:
                        # Print the state of the button
                        print(GPIO.input(GPIO_BUTTON))
                        # Calculate the time elapsed as the
                        # current time subtracted by the start_time
                        elapsed_time = time.time() - start_time
                        # If the button is pressed again within 10 seconds
                        # break out of the loop
                        if elapsed_time < 10:
                            if GPIO.input(GPIO_BUTTON) == GPIO.HIGH:
                                GPIO.output(GPIO_YELLOWLED, GPIO.LOW)
                                GPIO.output(GPIO_REDLED, GPIO.HIGH)
                                break
                        # Otherwise, break out of the loop after 10 seconds
                        else:
                            GPIO.output(GPIO_YELLOWLED, GPIO.LOW)
                            # Set the counter value as 3
                            counter = 3
                            # Break out of the loop
                            # The LED is set to green by default
                            break
                                
            # Pause the program for 1 second
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()