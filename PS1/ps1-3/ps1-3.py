import cv2 as cv
import numpy as np

# Get image file name and open the image
file = input("What image file would you like to process? Include the file extension. ")
img = cv.imread(file, cv.IMREAD_COLOR)

cv.imshow("Original", img)
cv.waitKey(10)

# Create a blank image of the same form as the original
gc = np.copy(img)
h, w, c = gc.shape

flag = True

# While the corrected image isn't acceptable, continue asking the user for gamma values. Once the user is happy, they can input -1 to save the image
while flag:
    gamma = float(input("Enter a gamma value, or enter -1 if you are happy with the corrected image: "))
    if gamma == -1:
        flag = False
    else:
        for i in range(h):
            for j in range(w):
                # Gamma correction calculation. Color intensities are normalized by 255 before gamma scaling and then are re-cast to 0-255. A = 1 here
                gc[i][j] = ((img[i][j] / 255.0) ** gamma) * 255.0 # V_out = V_in ^ gamma
        cv.imshow("Gamma corrected", gc)
        cv.waitKey(10)

cv.imwrite(file.split('.')[0] + "_gcorrected." + file.split('.')[1], gc)
cv.destroyAllWindows()