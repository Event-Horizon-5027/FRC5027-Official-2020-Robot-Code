'''
12/13/2020 12:26 AM
No Raspberry Pi communication with roboRIO. We will implement SSH to execute Robot commands with Java. Possible resource: https://www.chiefdelphi.com/t/executing-files-by-sshing-into-the-roborio/148131/2.

The ball detection works, albeit poorly. I think it is adequate for our use case though and it would be great if it could be tested to see if the ball detection works for the yellow FRC ball when it is put directly in front of the webcam. 

What does this code do? 
This code detects a ball in the game and instructs the robot to pick up the ball with the shooter mechanism.
When a ball is detected with OpenCV, the robot picks up the ball by moving forward to pick up the ball with the shooter.
Please refer to the Robot Code Developing and Testing Methodology for reporting bugs and comments.

How can we test this code?
To test:
1. SSH into the Raspberry Pi
2. Load the script with FileZilla's SCP Function (If you are using Windows) (macOS or Linux has a SCP client built in)
3. Use Pypi to install the opencv-python package.
4. Run script with python3 getball.py and see if console prints True. If it does so satisfactorily, the program is functional.
5. Take notes on robot behavior and comment on this commit.
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
