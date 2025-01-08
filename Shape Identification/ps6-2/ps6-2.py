import cv2 as cv
import numpy as np

# Read image and prepare for contour detection
img = cv.imread("ps6-2/spade-terminal.png")
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
thr,dst = cv.threshold(gray, 60, 255, cv.THRESH_BINARY)

for i in range(1):
    dst = cv.erode(dst, None)
for i in range(1):
    dst = cv.dilate(dst, None)

# Find contours and select one to be the template for a non-defective terminal (done by visual inspection)
cont, hier = cv.findContours(dst, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
template = cont[1]

# Set a similarity threshold for detecting defects. Done by examination of the values of all contours
similarity_thresh = 1.0

# Loop through every contour
for i in range(len(cont)):
    c = cont[i]
    h = hier[0, i]
    # Check only contours with no children and who's parent is the image frame
    if h[2] == -1 and h[3] == 0:
        # Find the similarity with the template
        d = cv.matchShapes(c, template, cv.CONTOURS_MATCH_I2, 0)
        # If the similarity value is too high, highlight the terminal as defective
        if d > similarity_thresh:
            img = cv.drawContours(img, [c], -1, (0,0,255), -1)

cv.imwrite("ps6-2/spade-terminal-output.png", img)
cv.imshow('defective terminals', img)
cv.waitKey(0)
cv.destroyAllWindows()