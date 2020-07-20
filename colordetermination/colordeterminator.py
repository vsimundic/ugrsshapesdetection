import cv2
from math import sqrt

# YCrCb colorspace - Y, Cr, Cb
colors = {'red': (76, 255, 85),
          'green': (150, 21, 44),
          'blue': (29, 107, 255),
          'yellow': (226, 149, 0),
          'orange': (151, 202, 43),
          'white': (255, 128, 128),
          'black': (0, 128, 128),
          'gray': (127, 128, 128),
          'pink': (165, 192, 106),
          'purple': (67, 171, 234)
          }


def BGR2YUV(image):
    cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    return image


def YCrCb2BGR(image):
    cv2.cvtColor(image, cv2.COLOR_YCrCb2BGR)
    return image


def distance(left, right):
    return sum((l - r) ** 2 for l, r in zip(left, right)) ** 0.5


class NearestColorKey(object):
    def __init__(self, goal):
        self.goal = goal

    def __call__(self, item):
        return distance(self.goal, item[1])
