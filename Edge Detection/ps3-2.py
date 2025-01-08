import numpy as np
import cv2 as cv
from tkinter import *
from tkinter import ttk

# Function that applies a Sobel filter to an image both horizontally and vertically
def sobel(img):
    h_kernel = (1/8) * np.array([[-1, 0, 1],
                                 [-2, 0, 2],
                                 [-1, 0, 1]])
    v_kernel = (1/8) * np.array([[1, 2, 1],
                                 [0, 0, 0],
                                 [-1, -2, -1]])
    return cv.filter2D(img, -1, v_kernel) + cv.filter2D(img, -1, h_kernel)

'''
Function that applies Canny edge detection to an image with the following params:
upper - Upper bound of the derivative threshold
lower - Lower bound of the derivative threshold
ap - Aperature size, can be 3, 5, or 7
l2 - Boolean indicating whether or not to use L2Gradient magnitude
'''
def canny(file, upper, lower, ap, l2):
    img = cv.imread(file, cv.IMREAD_COLOR)
    img_canny = cv.Canny(img, lower, upper, apertureSize=ap, L2gradient=l2)
    cv.imshow(file + " canny", img_canny)
    filename_canny = file.split('.')[0] + "-canny." + file.split('.')[1]
    cv.imwrite(filename_canny, img_canny)
    cv.waitKey(0)
    cv.destroyAllWindows()

# For each of the input images, apply the Sobel filter and display/save the result
images = ["cheerios.png", "gear.png", "professor.png", "circuit.png"]
for file in images:
    img = cv.imread(file, cv.IMREAD_COLOR)
    img_sobel = sobel(img)
    cv.imshow(file + " sobel", img_sobel)
    filename_sobel = file.split('.')[0] + "-sobel." + file.split('.')[1]
    cv.imwrite(filename_sobel, img_sobel)

cv.waitKey(0)
cv.destroyAllWindows()

# Set up a GUI to select an image and adjust parameters for Canny edge detection
root = Tk()
frm = ttk.Frame(root)
frm.grid()

# Default parameters
ap = IntVar(value = 3)
l2 = BooleanVar(value = 0)
img = StringVar(value = "cheerios.png")
upper = IntVar(value = 150)
lower = IntVar(value = 50)

# Image selection radio buttons
ttk.Label(frm, text="Select Image").grid(column=0, row=0, columnspan=8)
ttk.Radiobutton(frm, text="cheerios", variable=img, value="cheerios.png").grid(column=0, row=1, columnspan=2)
ttk.Radiobutton(frm, text="gear", variable=img, value="gear.png").grid(column=2, row=1, columnspan=2)
ttk.Radiobutton(frm, text="professor", variable=img, value="professor.png").grid(column=4, row=1, columnspan=2)
ttk.Radiobutton(frm, text="circuit", variable=img, value="circuit.png").grid(column=6, row=1, columnspan=2)

# Upper and lower threshold sliders
ttk.Label(frm, text="Lower Threshold").grid(column=0, row=2, columnspan=4)
lower_scale = ttk.Scale(frm, from_=0, to=500, orient=HORIZONTAL, variable=lower)
lower_scale.grid(column=0, row=3, columnspan=3)
lower_scale.set(lower.get())
ttk.Label(frm, textvariable=lower).grid(column=3, row=3)
ttk.Label(frm, text="Upper Threshold").grid(column=4, row=2, columnspan=4)
upper_scale = ttk.Scale(frm, from_=0, to=500, orient=HORIZONTAL, variable=upper)
upper_scale.grid(column=4, row=3, columnspan=3)
upper_scale.set(upper.get())
ttk.Label(frm, textvariable=upper).grid(column=7, row=3)

# Aperature size radio buttons
ttk.Label(frm, text="Aperture Size").grid(column=0, row=4, columnspan=4)
ttk.Radiobutton(frm, text="3", variable=ap, value=3).grid(column=0, row=5)
ttk.Radiobutton(frm, text="5", variable=ap, value=5).grid(column=1, row=5)
ttk.Radiobutton(frm, text="7", variable=ap, value=7).grid(column=2, row=5)

# L2Gradient check box
ttk.Label(frm, text="L2Gradient?").grid(column=4, row=4, columnspan=4)
ttk.Checkbutton(frm, variable = l2, onvalue=1, offvalue=0).grid(column=4, row=5, columnspan=4)

# Button to display and save result
ttk.Button(frm, text="Update Image", command=lambda: canny(img.get(), int(upper.get()), int(lower.get()), int(ap.get()), l2.get())).grid(column=0, row=6, columnspan=8)
root.mainloop()