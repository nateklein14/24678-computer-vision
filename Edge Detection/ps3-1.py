import numpy as np
import cv2 as cv

'''
A sharpening filter reduces the image blur, but cannot fully recapture the detail of the ground truth image.
'''
circuitboard = cv.imread("circuitboard.png", cv.IMREAD_COLOR)
# Define a sharpening filter
n = -1
kernel = np.array([[n, n, n],
                   [n, 8*abs(n)+1, n],
                   [n, n, n]])
circuitboard_improved = cv.filter2D(circuitboard, -1, kernel)
cv.imshow("circuit filtered", circuitboard_improved)
cv.imwrite("circuitboard-improved.png", circuitboard_improved)

'''
A median filter removes the black speckle noise from the image without reducing the overall fidelity of the image
'''
wedding = cv.imread("wedding.png", cv.IMREAD_COLOR)
wedding_filtered = cv.medianBlur(wedding, 3)
cv.imshow("wedding filtered", wedding_filtered)
cv.imwrite("wedding-improved.png", wedding_filtered)

'''
Combining a median blur and a sharpening filter removes the spike noise throughout the image and then emphasizes the edges of the image.
'''
pcb = cv.imread("pcb.png", cv.IMREAD_COLOR)
n = -1
kernel = np.array([[n, n, n],
                   [n, 8*abs(n)+1, n],
                   [n, n, n]])
pcb_filtered = cv.filter2D(cv.medianBlur(pcb, 3), -1, kernel)
cv.imshow("pcb filtered", pcb_filtered)
cv.imwrite("pcb-improved.png", pcb_filtered)

dog = cv.imread("dog.png", cv.IMREAD_COLOR)
n = -1
kernel = np.array([[n, n, n],
                   [n, 8*abs(n)+1, n],
                   [n, n, n]])
dog_filtered = cv.filter2D(cv.medianBlur(dog, 5), -1, kernel)
cv.imshow("dog filtered", dog_filtered)
cv.imwrite("dog-improved.png", dog_filtered)

cv.waitKey(0)
cv.destroyAllWindows()