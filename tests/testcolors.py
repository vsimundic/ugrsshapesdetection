import cv2
import colordetermination.colordeterminator as cld
import numpy as np

test_image = cv2.imread('/home/valentin/FAKS/UGRS/images/test_images/kvadar0011c2.jpg')
# test_image = cv2.imread('imgs/gray_shades.png')

cv2.imshow("Doggg", test_image)
r = cv2.selectROI("Doggg", test_image)

cropped_im = test_image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
cv2.imshow("Cropped", cropped_im)
cv2.waitKey(0)
cv2.destroyAllWindows()

cropped_im = cv2.cvtColor(cropped_im, cv2.COLOR_BGR2LAB)

r = int(np.mean(cropped_im[:, :, 0]))
g = int(np.mean(cropped_im[:, :, 1]))
b = int(np.mean(cropped_im[:, :, 2]))

print(str(r) + ', ' + str(g) + ', ' + str(b))
print(min(cld.colors.items(), key=cld.NearestColorKey((r, g, b))))
