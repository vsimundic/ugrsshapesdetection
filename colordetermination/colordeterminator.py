import cv2
from math import sqrt
import numpy as np

# YCrCb colorspace - Y, Cr, Cb
colors_ycrcb = {'red': (76, 255, 85),
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

# RGB
colors_rgb = {'Crvena': (200, 0, 0),
              'Zelena': (0, 200, 0),
              'Plava': (0, 0, 200),
              'Zuta': (200, 200, 0),
              'Bijela': (200, 200, 200),
              'Crna': (25, 25, 25),
              'Ljubicasta': (115, 0, 200)}

# LAB
colors_lab = {'Crvena0': (119, 189, 169),
              'Crvena1': (82, 180, 172),
              'Crvena2': (125, 197, 173),
              'Crvena3': (49, 163, 152),
              'Crvena4': (51, 152, 144),
              'Crvena5': (47, 164, 154),
              'Crvena6': (99, 189, 177),
              'Crvena7': (93, 182, 172),
              'Crvena8': (113, 194, 185),
              # 'Crvena9': (125, 168, 154),

              'Zelena0': (162, 73, 174),
              'Zelena1': (231, 78, 206),
              'Zelena2': (82, 105, 161),
              'Zelena3': (227, 82, 193),
              'Zelena4': (173, 81, 164),
              'Zelena5': (185, 99, 169),
              'Zelena6': (155, 64, 187),
              'Zelena7': (72, 102, 151),
              # 'Zelena8': (123, 102, 162),
              'Zelena9': (224, 91, 143),

              'Plava0': (95, 155, 90),
              'Plava1': (12, 158, 85),
              'Plava2': (40, 145, 88),
              'Plava3': (74, 177, 50),
              'Plava4': (107, 186, 37),
              'Plava5': (84, 150, 69),
              'Plava6': (186, 110, 86),
              # 'Plava7': (194, 120, 91),
              'Plava8': (232, 80, 113),
              # 'Plava9': (203, 115, 103),

              'Zuta0': (181, 151, 201),
              'Zuta1': (223, 126, 215),
              'Zuta2': (238, 119, 188),
              'Zuta3': (204, 141, 210),
              'Zuta4': (248, 106, 223),
              'Zuta5': (200, 110, 207),
              'Zuta6': (244, 115, 187),
              'Zuta7': (249, 123, 150),
              'Zuta8': (207, 138, 211),
              'Zuta9': (200, 110, 207),

              'Bijela0': (255, 128, 128),
              'Bijela1': (254, 125, 135),
              'Bijela2': (252, 123, 126),
              'Bijela3': (248, 127, 124),
              'Bijela4': (252, 130, 129),
              'Bijela5': (248, 127, 124),
              'Bijela6': (249, 126, 142),
              'Bijela7': (245, 124, 140),
              'Bijela8': (249, 126, 142),
              'Bijela9': (225, 128, 128),

              'Crna0': (0, 128, 128),
              'Crna1': (3, 128, 130),
              'Crna2': (7, 128, 130),
              # 'Crna3': (36, 129, 133),
              'Crna4': (10, 130, 131),
              'Crna5': (5, 130, 130),

              'Ljubicasta0': (168, 184, 76),
              'Ljubicasta1': (27, 164, 95),
              'Ljubicasta2': (122, 211, 51),
              'Ljubicasta3': (80, 193, 67),
              'Ljubicasta4': (147, 200, 63),
              'Ljubicasta5': (93, 200, 60),
              'Ljubicasta6': (41, 172, 87),
              'Ljubicasta7': (132, 209, 54),
              'Ljubicasta8': (139, 204, 58),
              'Ljubicasta9': (86, 199, 54),

              # 'Siva0': (217, 128, 128),
              # 'Siva1': (187, 128, 128),
              # 'Siva2': (153, 128, 128),
              'Siva3': (107, 128, 128),
              'Siva4': (78, 129, 128),
              'Siva5': (40, 129, 128),
              # 'Siva6': (),
              # 'Siva7': (),
              # 'Siva8': (),
              # 'Siva9': (),
              }


def ImageBGR2YCrCb(image):
    cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    return image


def ImageYCrCb2BGR(image):
    cv2.cvtColor(image, cv2.COLOR_YCrCb2BGR)
    return image


def PixelBGR2LAB(b, g, r):
    bgrpixel = np.zeros((1, 1, 3), np.uint8)
    bgrpixel[0, 0, 0] = b
    bgrpixel[0, 0, 1] = g
    bgrpixel[0, 0, 2] = r

    return cv2.cvtColor(bgrpixel, cv2.COLOR_BGR2LAB)


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


def detectRGBColorArea(area, rgb=False):
    new_area = area.copy()

    if not rgb:
        new_area = cv2.cvtColor(area, cv2.COLOR_BGR2RGB)

    print(new_area[:, :, 0])

    r = int(np.mean(new_area[:, :, 0]))
    g = int(np.mean(new_area[:, :, 1]))
    b = int(np.mean(new_area[:, :, 2]))

    COLOR_NAME = min(colors_rgb.items(), key=NearestColorKey((r, g, b)))
    return COLOR_NAME[0]


def detectLABColorArea(area, bgr=False):
    if bgr:
        area = cv2.cvtColor(area, cv2.COLOR_BGR2LAB)

    l = int(np.mean(area[:, :, 0]))
    a = int(np.mean(area[:, :, 1]))
    b = int(np.mean(area[:, :, 2]))

    COLOR_NAME = min(colors_lab.items(), key=NearestColorKey((l, a, b)))
    return COLOR_NAME[0][:-1]
