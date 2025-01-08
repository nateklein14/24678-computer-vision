import cv2
import numpy as np
import argparse

# check size (bounding box) is square
def isSquare(siz):
    ratio = abs(siz[0] - siz[1]) / siz[0]
    #print (siz, ratio)
    if ratio < 0.1:
        return True
    else:
        return False

# chekc circle from the arc length ratio
def isCircle(cnt):
    (x,y),radius = cv2.minEnclosingCircle(cnt)
    len = cv2.arcLength(cnt, True)
    ratio = abs(len - np.pi * 2.0 * radius) / (np.pi * 2.0 * radius)
    #print(ratio)
    if ratio < 0.1:
        return True
    else:
        return False

if __name__ == "__main__":
    #
    parser = argparse.ArgumentParser(description='Hough Circles')
    parser.add_argument('-i', '--input', default = 'ps6-1/all-parts.png')

    args = parser.parse_args()
    # Read image
    img = cv2.imread(args.input)

    # Convert to gray-scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Binary
    thr,dst = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)

    # clean up
    for i in range(1):
        dst = cv2.erode(dst, None)
    for i in range(4):
        dst = cv2.dilate(dst, None)

    # find contours with hierachy
    cont, hier = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # each contoure
    for i in range(len(cont)):
        c = cont[i]
        h = hier[0,i]
        if h[2] == -1 and h[3] == 0:
            # no child and parent is image outer
            img = cv2.drawContours(img, cont, i, (0,0,255),-1)
        elif h[3] == 0 and hier[0,h[2]][2] == -1:
            # with child
            if isCircle(c):
                if isCircle(cont[h[2]]):
                    # double circle
                    img = cv2.drawContours(img, cont, i, (0,255,0),-1)
                else:
                    # outer contour circle, inner contour not circle
                    img = cv2.drawContours(img, cont, i, (255, 0, 255), -1)
            else:
                # 1 child 
                if hier[0,h[2]][0] == -1 and hier[0,h[2]][1] == -1:
                    # find centroid of the contour and its child
                    M = cv2.moments(c)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    M_int = cv2.moments(cont[h[2]])
                    cX_int = int(M_int["m10"] / M_int["m00"])
                    cY_int = int(M_int["m01"] / M_int["m00"])
                    # if parent and child contours are concentric
                    if abs(cX - cX_int) <= 2 and abs(cY - cY_int) <= 2:
                        img = cv2.drawContours(img, cont, i, (0, 255, 255), -1)
                    else:
                        img = cv2.drawContours(img, cont, i, (255,0, 0),-1)
                    

    cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
    cv2.imshow("Image", img)    

    cv2.imwrite("ps6-1/all-parts-output.png", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
