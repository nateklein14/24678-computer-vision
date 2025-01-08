import numpy as np
import cv2 as cv
import sys
import math

filename = sys.argv[1]

# Read image and convert to binary
img = cv.imread(filename, cv.IMREAD_COLOR)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
th, bin = cv.threshold(gray, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
cv.imwrite(filename.split('.')[0] + "-binary." + filename.split('.')[1], bin)

# Close the image
k_e = cv.getStructuringElement(cv.MORPH_CROSS, (3,3))
blobs = cv.bitwise_not(bin)
erode_iters = 3
for i in range(erode_iters):
    blobs = cv.erode(blobs, k_e)
for i in range(erode_iters):
    blobs = cv.dilate(blobs, k_e)
cv.imwrite(filename.split('.')[0] + "-blobs." + filename.split('.')[1], blobs)

# Detect contours
contours, hier = cv.findContours(blobs, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
hier = hier[0]

# Detect the size of the contour bounding rectangles in order to make the catalog image size
max_w = 0
max_h = 0
for contour in contours:
    rect = cv.minAreaRect(contour)
    if rect[1][0] > max_w:
        max_w = rect[1][0]
    if rect[1][1] > max_h:
        max_h = rect[1][1]

# Catalog image is a grid based on the number of contours and the maximum contour size
max_w = math.ceil(max_w)
max_h = math.ceil(max_h)
grid_size = math.ceil(len(contours) ** 0.5)
cell_h = max_h + 10
cell_w = max_w + 10
catalog_img = np.zeros((cell_h * grid_size, cell_w * grid_size, 3))

# Add padding to the image in order to avoid indexing issues when grabbing the contours
img = cv.copyMakeBorder(img, 10, 10, 10, 10, cv.BORDER_CONSTANT)

cells = 0

# Grab contours, rotate them, and insert them into the catalog image
for comp in zip(contours, hier):
    cont = comp[0]
    hier = comp[1]
    # Only grab outer contours
    if hier[3] < 0:
        cells += 1
        # Mask the original image around the contour to just have the cell
        mask = np.zeros(img.shape[:2], np.uint8)
        cv.drawContours(mask, [cont], -1, (255,255,255), -1)
        result = cv.bitwise_and(img, img, mask=mask)

        # Get min bounding rectangle and use it to rotate the cell
        rect = cv.minAreaRect(cont)
        rot_mat = cv.getRotationMatrix2D(rect[0], 90-rect[2], 1)
        rot_res = cv.warpAffine(result, rot_mat, (result.shape[1], result.shape[0]))

        # Calculate next open grid position in catalog
        row = int(cells / grid_size)
        col = (cells % grid_size) - 1

        # Place the cell into the catalog grid
        catalog_center = (int((col * cell_w + cell_w/2)), int(row * cell_h + cell_h/2))
        catalog_img[catalog_center[0]-int(cell_w/2):catalog_center[0]+int(cell_w/2)][catalog_center[1]-int(cell_h/2):catalog_center[1]+int(cell_h/2)] = \
            rot_res[int(rect[0][1])-int(cell_h/2):int(rect[0][1])+int(cell_h/2)][int(rect[0][0])-int(cell_w/2):int(rect[0][0])+int(cell_w/2)]

cv.imwrite(filename.split('.')[0] + "-catalog." + filename.split('.')[1], catalog_img)