import cv2
import os
import yolodetection.yolo as yl

os.chdir(os.getenv('DARKNET_PATH'))
print(os.getcwd())
yl.detect("./darknet detector test obj.data ugrs/customcfgs/yolov3-obj.cfg backup/yolov3-obj_best_40.weights -ext_output -dont_show -out result.json < frames.txt")

detections_data = yl.readJSONDetections(path='/result.json')
yl.reset_class_scores()

objects = []
frame_id = 0

for detections_in_frame in detections_data:
    objects = yl.readJSONObjects(detections_in_frame)

    for frame_object in objects:
        name = frame_object["name"]
        confidence = frame_object["confidence"]

        yl.add_to_class_score(name, confidence)

CLASS_NAME = yl.get_most_confident_class()

# loop through detections and get coordinates
relative_coords = {}
for detections_in_frame in detections_data:
    objects = yl.readJSONObjects(detections_in_frame)

    for frame_object in objects:
        if CLASS_NAME in frame_object.values():
            print(frame_object)
            relative_coords = frame_object["relative_coordinates"]
            frame_id = detections_in_frame["frame_id"]
            break

if relative_coords:
    # yolo gives center coordinates and width/height
    center_x, center_y, width, height = yl.readBBoxCoordinates(relative_coords)
    print(center_y, center_x)
    frame_for_color = None
    if frame_id == 1:
        frame_for_color = cv2.imread("frame1.jpg")
    elif frame_id == 2:
        frame_for_color = cv2.imread("frame0.jpg")

    # frame_for_color = cv2.cvtColor(frame_for_color, cv2.COLOR_GRAY2BGR)
    area_for_color = cv2.imread("predictions.jpg", cv2.IMREAD_GRAYSCALE)
    area_for_color = cv2.cvtColor(area_for_color, cv2.COLOR_GRAY2BGR)
    offset = 50
    area_for_color[center_y - offset:center_y + offset, center_x - offset:center_x + offset, :] = \
        frame_for_color[center_y - offset:center_y + offset, center_x - offset:center_x + offset, :].copy()

    area_for_color = cv2.circle(area_for_color, (center_x, center_y), 10, (255, 0, 0), -1)

    cv2.imshow("Colored area", area_for_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
