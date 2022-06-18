# credits of original eye tracker via gradient to author. 
# Sergio Canu,  https://pysource.com/2019/01/04/eye-motion-tracking-opencv-with-python/

# Due to constraints of hardware and lack of machine learning implementation
# instead of pupil, iris will be detected instead
# in iteration 1, only a square contour will be drawned along with the x,y axis indicating middle of contour 

"""
This iteration has basic eye track with open cv gradient 
"""

"""Import necessary libraries"""
import cv2
import numpy as np

"""videoCapture(1) indicates usage of webcam, 0 for laptop built-in, or video file name"""
"""CAP_DSHOW is DirectShow, removes the delay of opening cam"""
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while True:
    ret, frame = cap.read()
    
    roi = frame
    rows, cols, _ = roi.shape

    """
    because of the nature of this way of finding the pupil (darkest area of the eye), 
    grayscale is needed to find the threshold and contour via RETR_TREE
    """
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)

    """
    50 is the value of gradient difference between 1 shade to another
    reduce to find get darkest area 
    more info read https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
    """
    _, thresh = cv2.threshold(gray_roi, 10, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    """sorted is to remove noise/ get contour with the highest weight (the iris)"""
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

    for cnt in contours: 
        """img, contour, contourID, colour, thickness"""
        # cv2.drawContours(roi, [cnt], -1, (0,0,255), 2) #draw directly at the gradient difference (appears circular)

        (x,y,w,h) = cv2.boundingRect(cnt)
        cv2.rectangle(roi, (x,y), (x+w, y+h), (0,0,255), 2)
        cv2.line(roi, (x+int(w/2), 0), (x+int(w/2), rows), (0,255,0), 2) #y-axis
        cv2.line(roi, (0, y+int(h/2)), (cols, y+int(h/2)), (0,255,0), 2) #x-axis
        break

    cv2.imshow("threshold", thresh)
    cv2.imshow("roi", roi)
    key = cv2.waitKey(30)
    if key == 27:
        break


cv2.destroyAllWindows()