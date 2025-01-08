import cv2 as cv
import numpy as np

# Get image file name and highlighting mode
file = input("What image file would you like to process? Include the file extension. ")
mode = input("Highlight darker (d) or lighter (l) regions? ")
threshold = int(input("What should the intensity threshold be for converting to a binary image? "))

# Read in the image and display it
img = cv.imread(file, cv.IMREAD_COLOR)
cv.imshow("image", img)

# Convert the image to grayscale and display/save it
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray_filename = file.split('.')[0] + "_grayscale." + file.split('.')[1]
cv.imwrite(gray_filename, gray)
cv.imshow("grayscale", gray)

# Convert the image to binary based on a threshold intensity value
bin = cv.threshold(gray, threshold, 255, cv.THRESH_BINARY)[1]
bin_filename = file.split('.')[0] + "_binary." + file.split('.')[1]
cv.imwrite(bin_filename, bin)
cv.imshow("binary", bin)

# Color the light or dark region based on input from before
h, w, c = img.shape # Get original image size and shape
out = np.ndarray((h, w, c)) # Create a new, blank template of the same size, shape, and channel count
for i in range(h):
    for j in range(w):
        if mode == 'd': # If highlighting dark areas, look for low intensity pixels
            if bin[i][j] == 0:
                out[i][j] = [0, 0, 255]
            else:
                out[i][j] = img[i][j]
        elif mode == 'l': # If highlighting bright areas, look for high intensity pixels
            if bin[i][j] == 255:
                out[i][j] = [0, 0, 255]
            else:
                out[i][j] = img[i][j]

out_filename = file.split('.')[0] + "_output." + file.split('.')[1]
cv.imwrite(out_filename, out)
cv.imshow("output", out)

cv.waitKey(0)
cv.destroyAllWindows()