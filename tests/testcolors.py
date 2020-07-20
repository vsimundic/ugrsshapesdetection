import cv2


def convertBGR2YCrCb(R, G, B):
    Y = int(round(0.299 * R + 0.587 * G + 0.114 * B))
    Cb = int(round(128 - 0.169*R - 0.331*G + 0.500*B))
    Cr = int(round(128 + 0.5*R - 0.419*G - 0.081*B))

    if Y > 255:
        Y = 255
    if Cb > 255:
        Cb = 255
    if Cr > 255:
        Cr = 255
    return Y, Cr, Cb


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

print(convertBGR2YCrCb(127,0,255))
