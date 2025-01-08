import sys
import cv2 as cv
import numpy as np
from random import randint

# A method to thin all blobs in an image. Follows the technique outline in the ps5-tips
def thin(img):
    k_e = cv.getStructuringElement(cv.MORPH_CROSS, (3,3))
    img1 = img.copy()
    thinned = np.zeros(img1.shape)
    # While the image isn't all black
    while cv.countNonZero(img1) != 0:
        # Erode the image
        er = cv.erode(img1, k_e)
        # Erode it again, then dilate
        op = cv.morphologyEx(er, cv.MORPH_OPEN, k_e)
        # Subtract the "opening" from the eroded image
        subset = er - op
        # Recombine
        thinned = cv.bitwise_or(subset, thinned)
        img1 = er.copy()
    return thinned

filename = sys.argv[1]

# Read and invert the binary image
img = cv.imread(filename, cv.IMREAD_GRAYSCALE)
img_inv = cv.bitwise_not(img)

# Close the image to remove noise around the edges of blobs
k_e = cv.getStructuringElement(cv.MORPH_CROSS, (3,3))
blobs = cv.dilate(img_inv, k_e)
dilations = 3
for i in range(dilations):
    blobs = cv.dilate(blobs, k_e)
blobs = cv.erode(blobs, k_e)
cv.imwrite(filename.split('.')[0] + "-blobs." + filename.split('.')[1], blobs)

# Using an area threshold, keep blobs that could be crack and remove others
thresh = 3000
cont, hier = cv.findContours(blobs, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
contours = cv.cvtColor(blobs, cv.COLOR_GRAY2BGR)
crack_blob = np.zeros(img.shape)
for contour in cont:
    # Draw all contours on one image, and on the other, only draw and fill in the ones that could be cracks
    cv.drawContours(contours, [contour], -1, (randint(0, 255), randint(0, 255), randint(0, 255)), 2)
    if cv.contourArea(contour) > thresh:
        cv.drawContours(crack_blob, [contour], -1, (255,255,255), -1)

cv.imwrite(filename.split('.')[0] + "-contours." + filename.split('.')[1], contours)

# Thin the image with the crack blobs
crack_img = thin(crack_blob)
cv.imwrite(filename.split('.')[0] + "-cracks." + filename.split('.')[1], crack_img)