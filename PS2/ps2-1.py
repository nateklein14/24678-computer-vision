import cv2 as cv
import numpy as np
import math

file = input("Enter the name of a grayscale image (extension included): ")

img = cv.imread(file, cv.IMREAD_GRAYSCALE)
cv.imshow("original", img)
cv.waitKey(10)

# Find minimum and maximum intensities in the grayscale image
i_min = np.min(img)
i_max = np.max(img)

# Set parameters for each channel's tone curve
lut = []
k_br = 0.5
k_g = 0.1
span = i_max - i_min
br_mid = 1/2.3
g_mid = 1/4
for i in range(span + 1):
    # Define logistic function tone curves for each color channel. This eliminates the need for piecewise functions which require checks on the
    # intensity value to figure out with branch of the function it should be in
    b = int(round(255.0 - 255.0 / (1 + math.exp(-k_br*(i - br_mid * span))), 0))
    g = int(round(255.0 * (1 / (1 + math.exp(-k_g*(i - g_mid * span))) - 1 / (1 + math.exp(-k_g*(i - (1 - g_mid) * span)))), 0))
    r = int(round(255.0 / (1 + math.exp(-k_br*(i - (1 - br_mid) * span))), 0))
    lut.append([b, g, r])


w, h = img.shape
pseudo = np.ndarray((w, h, 3))

x_maxes = []
y_maxes = []

# Find all the positions of the pixels with the max intensity in the image
for i in range(w):
    for j in range(h):
        pseudo[i][j] = lut[img[i][j] - i_min]
        if img[i][j] == i_max:
            x_maxes.append(j)
            y_maxes.append(i)

# Calculate the center of mass of the brightest pixels by averaging their x and y coordinates, then draw a crosshair at that point
com = (int(sum(x_maxes) / len(x_maxes)), int(sum(y_maxes) / len(y_maxes)))
cv.circle(pseudo, com, 20, (255, 255, 255), 2)
cv.line(pseudo, (com[0] - 25, com[1]), (com[0] + 25, com[1]), (255, 255, 255), 2)
cv.line(pseudo, (com[0], com[1] - 25), (com[0], com[1] + 25), (255, 255, 255), 2)

cv.imwrite(file.split('.')[0] + "-color." + file.split('.')[1], pseudo)
cv.imshow("pseudocolored", pseudo)
cv.waitKey(0)