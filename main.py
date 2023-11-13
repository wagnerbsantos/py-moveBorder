import pyautogui
from time import sleep, time
import cv2
import numpy
from skimage.measure import euler_number

mouseDown = False
dst = None
state = set()
count = 0


def getColorPos(image, color):
    for x in range(image.width):
        for y in range(image.height):
            if (image.getpixel((x, y)) == color):
                return (x, y)


def throw():
    #pyautogui.mouseDown()
    sleep(0.5)
    #pyautogui.mouseUp()
    sleep(2)


def startFishing(image):
    global mouseDown
    global count
    baitPos = getColorPos(image, (129, 115, 100))
    if (baitPos != None):
        if (baitPos[0] < 120):
            #pyautogui.mouseDown()
            mouseDown = True
        elif (baitPos[0] > 120):
            #pyautogui.mouseUp()
            mouseDown = False
        # print(myScreenshot)
    elif(mouseDown):
        #pyautogui.mouseUp()
        mouseDown = False
    else:
        count = count + 1
        if ("minigame" in state and count > 5):
            state.remove("minigame")
            sleep(2)
            count = 0


winname = 'window'
cv2.namedWindow(winname)        # Create a named window
cv2.moveWindow(winname, 2000, 500)   # Move it to (x,y)
#cv2.imshow(winname, img)

while (True):
    startTime = time()
    # print(state)
    myScreenshot = pyautogui.screenshot()
    # myScreenshot.save('temp.png')
    fish = myScreenshot.crop((850, 559, 1070, 565))
    mousePos = pyautogui.position()
    mouseOffset = 50
    mouseArea = myScreenshot.crop((mousePos.x - mouseOffset, mousePos.y -
                                  mouseOffset, mousePos.x + mouseOffset, mousePos.y + mouseOffset))
    mouseArea = myScreenshot
    if ("minigame" in state):
        startFishing(fish)
    if ("waiting" in state):
        temp = numpy.array(mouseArea)
        mask = cv2.threshold(temp, 150, 255, cv2.THRESH_BINARY)[1][:, :, 0]
        if dst is None:
            dst = mask.copy().astype(float)
        mask = mask.copy().astype(float)
        weighted = cv2.accumulateWeighted(mask, dst, 0.5)
        btnot = cv2.absdiff(weighted, mask)
        euler = euler_number(weighted, 3)
        white = cv2.countNonZero(btnot)
        cv2.imshow(winname, btnot)
        cv2.waitKey(1)
        print(white)
        count = count + 1
        if (white >= 410 or white == 0 and count != 1):
            #pyautogui.click()
            state.remove("waiting")
            state.add("minigame")
            dst = None
            print(white)
            sleep(0.2)
            count = 0

    if (len(state) == 0):
        throw()
        state.add("waiting")
    #print(time() - startTime)
