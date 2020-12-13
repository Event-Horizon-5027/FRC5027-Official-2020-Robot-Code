'''
What does this code do? 
This code detects a ball in the game and instructs the robot to pick up the ball with the shooter mechanism.
When a ball is detected with OpenCV, the robot picks up the ball by moving forward to pick up the ball with the shooter.

How can we test this code?
Please deploy the Java code with FRC Driver Station. 
Then, turn on the Raspberry Pi by plugging it in to its power supply.  
Please refer to the Robot Code Developing and Testing Methodology for reporting bugs and comments.

How does it work?
The Java code is deployed and will call on the Python code when needed. 
The Raspberry Pi's startup script will run the code and communicate with the roboRIO via I2C when it is called on by the Java Program.
'''

import cv2
import time	
import numpy as np

frame_rate = 5
prev = 0
forward = False

cap = cv2.VideoCapture(0)

while True:
	time_elapsed = time.time() - prev
	_, frame = cap.read()

	if time_elapsed > 1./frame_rate:
		
		prev = time.time()
		
		blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
		grayimg = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY) # Makes img grayscale
				
		lower_yellow = np.array([0, 0, 0]) # Boundaries for color detection HSV
		upper_yellow = np.array([255, 255, 255]) # Boundaries for color detection HSV
		mask = cv2.inRange(blurred_frame, lower_yellow, upper_yellow)
		
		tresh1, binaryimage = cv2.threshold(grayimg, 127, 255, cv2.THRESH_BINARY) #+cv2.THRESH_OTSU
			
		contours, hierarchy = cv2.findContours(grayimg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) # Only accepts binary - cannot accept thresholded image
		cv2.drawContours(tresh1, contours, -1, (0, 255, 0), 10)                

		circles = cv2.HoughCircles(grayimg, cv2.HOUGH_GRADIENT, 1, grayimg.shape[0] / 8,
						param1=100, param2=30,
						minRadius=1, maxRadius=30)
	
		if circles is not None:
			forward = True
			print(forward)

	cv2.imshow("Manipulated", grayimg) # Manipulated with overlaid contours

	key = cv2.waitKey(1)

	if key == 27:
			break

cap.release()
cv2.destroyAllWindows()
