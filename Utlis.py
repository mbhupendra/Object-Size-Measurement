import cv2
import numpy as np
 
## TO STACK ALL THE IMAGES IN ONE WINDOW
def stackImages(imgArray,scale,lables=&#91;]):
    rows = len(imgArray)
    cols = len(imgArray&#91;0])
    rowsAvailable = isinstance(imgArray&#91;0], list)
    width = imgArray&#91;0]&#91;0].shape&#91;1]
    height = imgArray&#91;0]&#91;0].shape&#91;0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray&#91;x]&#91;y] = cv2.resize(imgArray&#91;x]&#91;y], (0, 0), None, scale, scale)
                if len(imgArray&#91;x]&#91;y].shape) == 2: imgArray&#91;x]&#91;y]= cv2.cvtColor( imgArray&#91;x]&#91;y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = &#91;imageBlank]*rows
        hor_con = &#91;imageBlank]*rows
        for x in range(0, rows):
            hor&#91;x] = np.hstack(imgArray&#91;x])
            hor_con&#91;x] = np.concatenate(imgArray&#91;x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray&#91;x] = cv2.resize(imgArray&#91;x], (0, 0), None, scale, scale)
            if len(imgArray&#91;x].shape) == 2: imgArray&#91;x] = cv2.cvtColor(imgArray&#91;x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape&#91;1] / cols)
        eachImgHeight = int(ver.shape&#91;0] / rows)
        print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables&#91;d])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables&#91;d],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver
 
def reorder(myPoints):
 
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)
 
    myPointsNew&#91;0] = myPoints&#91;np.argmin(add)]
    myPointsNew&#91;3] =myPoints&#91;np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew&#91;1] =myPoints&#91;np.argmin(diff)]
    myPointsNew&#91;2] = myPoints&#91;np.argmax(diff)]
 
    return myPointsNew
 
 
def biggestContour(contours):
    biggest = np.array(&#91;])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 5000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest,max_area
def drawRectangle(img,biggest,thickness):
    cv2.line(img, (biggest&#91;0]&#91;0]&#91;0], biggest&#91;0]&#91;0]&#91;1]), (biggest&#91;1]&#91;0]&#91;0], biggest&#91;1]&#91;0]&#91;1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest&#91;0]&#91;0]&#91;0], biggest&#91;0]&#91;0]&#91;1]), (biggest&#91;2]&#91;0]&#91;0], biggest&#91;2]&#91;0]&#91;1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest&#91;3]&#91;0]&#91;0], biggest&#91;3]&#91;0]&#91;1]), (biggest&#91;2]&#91;0]&#91;0], biggest&#91;2]&#91;0]&#91;1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest&#91;3]&#91;0]&#91;0], biggest&#91;3]&#91;0]&#91;1]), (biggest&#91;1]&#91;0]&#91;0], biggest&#91;1]&#91;0]&#91;1]), (0, 255, 0), thickness)
 
    return img
 
def nothing(x):
    pass
 
def initializeTrackbars(intialTracbarVals=0):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Threshold1", "Trackbars", 200,255, nothing)
    cv2.createTrackbar("Threshold2", "Trackbars", 200, 255, nothing)
 
 
def valTrackbars():
    Threshold1 = cv2.getTrackbarPos("Threshold1", "Trackbars")
    Threshold2 = cv2.getTrackbarPos("Threshold2", "Trackbars")
    src = Threshold1,Threshold2
    return src