import cv2
import numpy as np
import os
import pickle

contour = []
name_dump = "variablescontour_cam1.pickle"
draw_circ = False

def mouseClick(event, x, y, flags, param):
    global draw_circ
    if event == cv2.EVENT_LBUTTONUP:
        contour.append([x, y])
        draw_circ = True


cap = cv2.VideoCapture(2)
ret, img = cap.read()
cv2.namedWindow("image1")
cv2.setMouseCallback("image1", mouseClick)
img_full = img.copy()

fill_color = [0, 0, 0]
mask_value = 255

while True:
    ret, img = cap.read()
    img_full = img.copy()

    if draw_circ:
        img = cv2.circle(img, (contour[-1][0], contour[-1][1]), 5, (255, 255, 255), 3)
        draw_circ = False

    cv2.imshow("image1", img)
    key = cv2.waitKey(1) & 0xFF

    if key == ord(" "):
        break

cv2.destroyAllWindows()
print(contour)
with open('/home/valentin/FAKS/UGRS_projekt/alexeyAB_darknet/ugrsshapesdetection/data/vars/{}'.format(name_dump), 'wb') as contours_file_:
    pickle.dump(contour, contours_file_)

stencil = np.zeros(img_full.shape[:-1]).astype(np.uint8)
cv2.fillPoly(stencil, [np.array(contour, dtype=np.int32)], mask_value)

sel = stencil != mask_value
img_full[sel] = fill_color

cv2.imshow("Image contoured", img_full)
cv2.imwrite("cam1_contoured.jpg", img_full)
cv2.waitKey(0)
cv2.destroyAllWindows()