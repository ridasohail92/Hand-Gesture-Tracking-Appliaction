
# import open CV
import cv2

# cvzone is using mediapipe package at backend
from cvzone.HandTrackingModule import HandDetector


# class to create buttons
class Button:

    # initialization
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    # Drawing method
    def draw(self, img):
        # button
        # inputs: img, position, width x height, colour
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (225, 225, 225), cv2.FILLED)
        # adding border
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
        # text on image
        cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)


    def checkClick(self, x, y):
        #  if starting point is greater than x1 and less than x2(=x1+width)
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            # change the colour of the button and text
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 255, 255), cv2.FILLED)
            # adding border
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
            # text on image
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 75), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)

            # return true if button was clicked
            return True
        else:
            return False



# Webcam
cap = cv2.VideoCapture(0)

# set the dimensions of the video
cap.set(3, 1280)  # width
cap.set(4, 720)  # height

# initialization
# confident = 80 %
detector = HandDetector(detectionCon=0.8, maxHands=1)


# creating Buttons

buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]

buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x*100 + 800
        ypos = y*100 + 150
        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))


# variables
myEquation = ''
delayCounter = 0





# Looping through each frame of our video
while True:
    # get image from webcam
    success, img = cap.read()

    # flip image horizontally
    img = cv2.flip(img, 1)

    # Detection of hand
    hands, img = detector.findHands(img, flipType=False)

    # DRAWING ALL BUTTONS

    # drawing result rectangle
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100), (225, 225, 225), cv2.FILLED)
    # adding border to result
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100), (50, 50, 50), 3)


    # drawing calclator buttons
    for button in buttonList:
        button.draw(img)

    # Processing
    # Check for hands
    if hands:
        # find distance b/w fingers
        # point 8 and 12 are the ones that concerns us
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        #print(length)
        x, y = lmList[8][:2]
        # check which location was clicked when less distance
        if length < 60:
            for i, button in enumerate(buttonList):
                # check if the specific button was clicked
                if button.checkClick(x, y) and delayCounter == 0:
                    # the exact value being used, we did this because it is a list and we split the row and column
                    # print(buttonListValues[int(i%4)][int(i/4)])
                    myValue = buttonListValues[int(i%4)][int(i/4)]
                    # avoid printing = sign
                    if myValue == '=':
                        # evaluating the equation in string as a formula by using eval
                        myEquation = str(eval(myEquation))
                    else:
                        myEquation += myValue

                    delayCounter = 1  # starting the counter

    # avoid duplicates when clicking

    if delayCounter != 0:  # means it has started
        delayCounter += 1
        if delayCounter > 10:  # i.e. 10 frames have passed
            delayCounter = 0

    # Display the equation/result
    # text on result
    cv2.putText(img, myEquation, (810, 120), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    # Display Image
    cv2.imshow("Image", img)

    # adding a wait of 1 millisecond
    key = cv2.waitKey(1)

    if key == ord('c'):
        myEquation = ''

