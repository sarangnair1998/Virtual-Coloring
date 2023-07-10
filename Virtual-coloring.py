import cv2
import numpy as np


def findColor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y = Contour(mask)
        cv2.circle(imgContour,(x,y),10,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count +=1
    return newPoints

def Contour(img):
    contours,heirarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h =0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            #cv2.drawContours(imgContour,cnt,-1,(255,0,0),3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y


def drawonCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgContour,(point[0],point[1]),10,myColorValues[point[2]],cv2.FILLED)



width = 640
height = 480
capture = cv2.VideoCapture(0)
capture.set(3,width)
capture.set(4,height)
capture.set(10,150)

myColors = [[48,38,77,154,245,248],
            [46,43,36,165,226,244]]
myColorValues = [[0,100,0],[205,0,0]]
myPoints = []             #[x,y,colorID]

while True:
    success,img = capture.read()
    imgContour = img.copy()
    newPoints = findColor(img,myColors,myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawonCanvas(myPoints,myColorValues)
    cv2.imshow("Output",imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



