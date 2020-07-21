import cv2
import colordetermination.colordeterminator as cld
import numpy as np

# image_white = cv2.imread('red.png')
# # cv2.imshow("White color", image_white)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
#
# print(image_white)
# imageycrcb = image_white.copy()
# cv2.cvtColor(image_white, cv2.COLOR_BGR2YCrCb, imageycrcb)
# print("#########################################")
# print(imageycrcb)

print(cld.PixelBGR2YCrCb(127, 0, 255))

test_image = cv2.imread('kvadar0001.jpg')
cv2.imshow("Doggg", test_image)
r = cv2.selectROI("Doggg", test_image)

cropped_im = test_image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
cv2.imshow("Cropped", cropped_im)
cv2.waitKey(0)
cv2.destroyAllWindows()

# image_ycrcb = cld.ImageBGR2YCrCb(cropped_im)
cropped_im = cv2.cvtColor(cropped_im, cv2.COLOR_BGR2RGB)
# rows, cols, _ = image_ycrcb.shape

r = int(np.mean(cropped_im[:, :, 0]))
g = int(np.mean(cropped_im[:, :, 1]))
b = int(np.mean(cropped_im[:, :, 2]))
# print(cropped_im[:, :, 0])

print(b, g, r)
print(min(cld.colors.items(), key=cld.NearestColorKey((r, g, b))))
