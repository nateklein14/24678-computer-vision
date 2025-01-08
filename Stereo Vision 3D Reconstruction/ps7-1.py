import numpy as np
import cv2 as cv
import sys
import open3d as o3d

filename_left = sys.argv[1]
filename_right = sys.argv[2]

left = cv.imread(filename_left)
right = cv.imread(filename_right)

# Get the disparity map of the left and right images
window_size = 9
min_disp = 16
num_disp = 16*8
stereo = cv.StereoSGBM_create(minDisparity = min_disp,
        numDisparities = num_disp,
        blockSize = 16,
        P1 = 8*3*window_size**2,
        P2 = 32*3*window_size**2,
        disp12MaxDiff = 1,
        uniquenessRatio = 10,
        speckleWindowSize = 100,
        speckleRange = 1
    )
disparity_map = stereo.compute(cv.cvtColor(left, cv.COLOR_BGR2GRAY), cv.cvtColor(right, cv.COLOR_BGR2GRAY)).astype(np.float32) / 16.0

cv.imwrite(filename_left.split('-')[0] + "-disparity.png", disparity_map)

# Disparity to depth constant of proportionality
r = 5

# Get depth of each point and write the PLY text
points = []
data = ""

for i in range(left.shape[0]):
    for j in range(left.shape[1]):
        X = left.shape[1] - j
        Y = i
        Z = r*disparity_map[i, j]
        points.append([X, Y, Z])
        # XYZ of each point and the color of it pulled from the original left image
        data += str(X) + " " + str(Y) + " " + str(Z) + " " + str(left[i, j, 2]) + " " + str(left[i, j, 1]) + " " + str(left[i, j, 0]) + "\n"

# PLY file header
header = "ply\nformat ascii 1.0\ncomment made by CVE\nelement vertex " + str(len(points)) + "\nproperty float32 x\nproperty float32 y\nproperty float32 z\nproperty uint8 red\nproperty uint8 green\nproperty uint8 blue\nend_header\n"

f = open(filename_left.split('-')[0] + ".ply", "w")
f.write(header + data)
f.close()

path = filename_left.split('-')[0] + ".ply"
ply = o3d.io.read_point_cloud(path)
o3d.visualization.draw_geometries([ply])