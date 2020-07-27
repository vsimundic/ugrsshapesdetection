import cv2
from math import sqrt

# # YCrCb colorspace - Y, Cr, Cb
# colors = {'red': (76, 255, 85),
#           'green': (150, 21, 44),
#           'blue': (29, 107, 255),
#           'yellow': (226, 149, 0),
#           'orange': (151, 202, 43),
#           'white': (255, 128, 128),
#           'black': (0, 128, 128),
#           'gray': (127, 128, 128),
#           'pink': (165, 192, 106),
#           'purple': (67, 171, 234)
#           }

# RGB
colors = {'Crvena': (255, 0, 0),
          'Zelena': (0, 255, 0),
          'Plava': (0, 0, 255),
          'Zuta': (255, 255, 0),
          # 'orange': (255, 127, 0),
          # 'Bijela': (255, 255, 255),
          # 'Crna': (0, 0, 0),
          # 'gray': (127, 127, 127),
          # 'pink': (255, 127, 127),
          'Ljubicasta': (127, 0, 255)}


def ImageBGR2YCrCb(image):
    cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    return image


def ImageYCrCb2BGR(image):
    cv2.cvtColor(image, cv2.COLOR_YCrCb2BGR)
    return image


def PixelBGR2YCrCb(R, G, B):
    Y = int(round(0.299 * R + 0.587 * G + 0.114 * B))
    Cb = int(round(128 - 0.169 * R - 0.331 * G + 0.500 * B))
    Cr = int(round(128 + 0.5 * R - 0.419 * G - 0.081 * B))

    if Y > 255:
        Y = 255
    if Cb > 255:
        Cb = 255
    if Cr > 255:
        Cr = 255
    return Y, Cr, Cb


def distance(left, right):
    return sum((l - r) ** 2 for l, r in zip(left, right)) ** 0.5


class NearestColorKey(object):
    def __init__(self, goal):
        self.goal = goal

    def __call__(self, item):
        return distance(self.goal, item[1])
