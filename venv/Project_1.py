import urllib.request
import cv2
import numpy as np
import urllib.request

# here i have used the commented code i have written previously in the bottom of theis main code to get the right H, S and V.
colors = [[35,151,102,158,255,255],[0,151,102,74,255,255]]
color_values = [[255,0,0], [51,100,255]]
mypoints= []
# Here we define a color detector function for blue and orange markers
def color_detector(img, colors, color_values):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newpoints = []
    for color in colors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        #cv2.imshow(str(color[0]), mask)
        x, y = getContours(mask)
        cv2.circle(img_result, (x, y),5, color_values[count], cv2.FILLED)
        if x!=0 and y!= 0:
            newpoints.append([x, y, count])
        count +=1
    return newpoints

# i defined a function to draw on the screen
def draw(mypoints, color_values):
    for point in mypoints:
        cv2.circle(img_result, (point[0], point[1]),5, color_values[point[2]], cv2.FILLED)


#this function will get the contours and the coordination of each corners, simply put to get the coordination of out marker's head.
def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
                # cv2.drawContours(img_result, cnt, -1, (255, 0, 0), 3)
                peri = cv2.arcLength(cnt,True)
                approx = cv2.approxPolyDP(cnt,0.02*peri,True)
                x, y, w, h = cv2.boundingRect(approx)
    return  x+w//2, y

# i used my smartphone's camera so don't panic and just reach out to me for it's set-up.
while True:
    url = "http://192.168.1.64:8080/shot.jpg"
    img_array = np.array(bytearray(urllib.request.urlopen(url).read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, -1)
    img = cv2.resize(img, (400, 400))
    img_result = img.copy()
    newpoints = color_detector(img, colors, color_values)
    if len(newpoints) != 0 :
        for point in newpoints:
            mypoints.append(point)

    if len(mypoints)!=0:
        draw(mypoints, color_values)
    cv2.imshow('video', img_result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




# this function will give you the Sat and Hue and Value of the color you want.
'''
import urllib.request
import cv2
import numpy as np
import urllib.request



def empty(a):
    pass
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)
while True:
    url = "http://192.168.1.64:8080/shot.jpg"

    img_array = np.array(bytearray(urllib.request.urlopen(url).read()), dtype=np.uint8)

    img = cv2.imdecode(img_array, -1)
    img = cv2.resize(img, (600, 600))
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
    print(h_min)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([img, mask, result])
    cv2.imshow('Horizontal Stacking', hStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
'''