# credits of original eye tracker via gradient to author.
# Sergio Canu,  https://pysource.com/2019/01/04/eye-motion-tracking-opencv-with-python/

# Due to constraints of hardware and lack of machine learning implementation
# instead of pupil, iris will be detected instead
# in iteration 1, only a square contour will be drawned along with the x,y axis indicating middle of contour

# btw x is width, y is height

"""
This iteration is used for 1 time use implementation
will run capture when called by other sources (EG Html request get, discord listen event or command)
better resource saving
"""

"""Import necessary libraries"""
import cv2
import numpy as np
import time

""" (A) intersection  between 2 lines, returns a tuple """


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def intersectf(A, B, C, D):
    a1 = B.y - A.y
    b1 = A.x - B.x
    c1 = a1*(A.x) + b1*(A.y)

    a2 = D.y - C.y
    b2 = C.x - D.x
    c2 = a2*(C.x) + b2*(C.y)

    determ = a1*b2 - a2*b1
    xis = (b2*c1 - b1*c2) / determ
    yis = (a1*c2 - a2*c1) / determ
    return xis, yis


""" 
get bounding box of video
currently only 50% of width and height as 4 boxes of reference
50% height, height, 50% width, width
"""


"""TODO FIND A BETTER PRACTICE/METHOD"""
""" (B) Get category """
def Category(ratiois):
    # print(f"ratiois is {ratiois}")
    """better practice if getting midpoint from a lot of conditions?"""
    if ratiois[0] < 50 and ratiois[1] < 50:
        return 'A'
    elif ratiois[0] < 50 and ratiois[1] <= 100:
        return 'C'
    elif ratiois[0] <= 100 and ratiois[1] < 50:
        return 'B'
    elif ratiois[0] <= 100 and ratiois[1] <= 100:
        return 'D'




""" main loop """
def returnvalue(camis):
    """videoCapture(1) indicates usage of webcam, 0 for laptop built-in, or video file name"""
    """CAP_DSHOW is DirectShow, removes the delay of opening cam"""
    cap = cv2.VideoCapture(camis, cv2.CAP_DSHOW)
    capheight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    capwidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

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
    
    if camis == 0:
        camisthresh = 80
    if camis == 1:
        camisthresh = 20
    _, thresh = cv2.threshold(gray_roi, camisthresh, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    """sorted is to remove noise/ get contour with the highest weight (the iris)"""
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    for cnt in contours:
        """img, contour, contourID, colour, thickness"""
        # cv2.drawContours(roi, [cnt], -1, (0,0,255), 2) #draw directly at the gradient difference (appears circular)

        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(roi, (x, y), (x+w, y+h), (0, 0, 255), 2)

        """ (A) to get midpoint as pseudo pupil """
        A = Point(x+int(w/2), 0)
        B = Point(x+int(w/2), rows)
        C = Point(0, y+int(h/2))
        D = Point(cols, y+int(h/2))
        midpt = intersectf(A, B, C, D)
        # print(midpt)

        """ (B) to differentiate which box midpoint is looking at """
        ratiois = (int((midpt[0] / capwidth) * 100), int((midpt[1] / capheight) * 100))
        print(Category(ratiois))

        return Category(ratiois)
