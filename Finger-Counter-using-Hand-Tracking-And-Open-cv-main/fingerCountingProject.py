# -*- coding: utf-8 -*-
"""
Modified version for recognizing 0 to 9 hand gestures with speech output.
"""
import cv2
import time
import pyttsx3
import handTrackingModule as htm

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to map finger states to digits 0-9
def getNumber(finger_states):
    s = "".join(map(str, finger_states))
    
    if s == "00000":
        return 0  # All fingers down
    elif s == "01000":
        return 1  # Only index finger up
    elif s == "01100":
        return 2  # Index and middle fingers up
    elif s == "01110":
        return 3  # Index, middle, and ring fingers up
    elif s == "01111":
        return 4  # Index, middle, ring, and pinky fingers up
    elif s == "11111":
        return 5  # All fingers up
    elif s == "10000":
        return 6  # Only thumb up
    elif s == "11000":
        return 7  # Thumb and index finger up
    elif s == "11100":
        return 8  # Thumb, index, and middle fingers up
    elif s == "11110":
        return 9  # Thumb, index, middle, and ring fingers up
    else:
        return -1  # Undefined gesture

# Camera setup
wcam, hcam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)

pTime = 0
detector = htm.handDetector(detectionCon=0.75)
last_spoken_number = -1  # Keep track of the last spoken number to avoid repetition

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)
    
    tipIds = [4, 8, 12, 16, 20]  # Finger tip landmark IDs
    
    if len(lmList) != 0:
        fingers = []
        
        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Other four fingers
        for id in range(1, len(tipIds)):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        # Get the number from the finger configuration
        number = getNumber(fingers)
        
        # Display number on the screen
        if number != -1:  # Only display valid numbers
            cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(number), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 20)
            
            # Speak the number if it hasn't been spoken recently
            if number != last_spoken_number:
                engine.say(str(number))
                engine.runAndWait()
                last_spoken_number = number  # Update last spoken number
    
    # Display FPS on the screen
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 3)
    
    cv2.imshow("image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
