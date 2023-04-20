import cv2
import torch
import torchvision
import numpy as np
import time
import sheet_finder_warper as warper

#variables
points = []

# Load the YOLO model from a local directory
test_model = torch.hub.load('yolov5', 'custom', path='test_corrector10_3.pt', source='local')
corner_model = torch.hub.load('yolov5', 'custom', path='corner4.pt', source='local')

# Load the input image
def pre_process(image , iteration):

    gray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,101, 8)
    erode = cv2.erode(thresh , (8 , 8) , iterations=iteration)
    image = cv2.resize(erode , (640 , 640))
    return image


def detect_test(image , draw = False):
        
    # image = cv2.imread(image)
    image = cv2.resize(image , (640 , 640))

    # Convert the image from OpenCV format to PyTorch tensor format
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Run the inference on the input image using the loaded YOLO model
    outputs = test_model(image)

    # Parse the outputs and extract the predicted bounding boxes, class labels, and confidence scores
    results = outputs.xyxy[0].numpy()
    boxes = results[:, :4]
    labels = results[:, 5]
    scores = results[:, 4]

    # Apply NMS to filter out overlapping bounding boxes
    iou_threshold = 0.6
    keep = torchvision.ops.nms(torch.tensor(boxes), torch.tensor(scores), iou_threshold)

    # Select the bounding boxes and corresponding scores and labels that were kept after NMS
    boxes = boxes[keep]
    scores = scores[keep]
    labels = labels[keep]

    # Visualize the predicted bounding boxes on the input image using OpenCV
    class_names = test_model.names
    for i in range(len(boxes)):
        box = boxes[i]
        label = int(labels[i])
        score = scores[i]
        class_name = class_names[label]
        color = (0, 255, 0)  # green
        red = (255 , 0 , 0)
        x1, y1, x2, y2 = box.astype(np.int32)

        # the middle points of the detections
        if score > 0.6:
            mid_x = int(((x2 - x1) / 2) + x1)
            mid_y = int(((y2 - y1) / 2) + y1)

            point_dict = {"class" : class_name , "x" : mid_x , "y" : mid_y}
            points.append(point_dict)

            if draw:

                if class_name == "marked":
                    cv2.rectangle(image, (x1, y1), (x2, y2), color, 1)
                    cv2.circle(image , (mid_x , mid_y) , 5 , color , -1)
                else :
                    cv2.rectangle(image, (x1, y1), (x2, y2), red, 1)
                    cv2.circle(image , (mid_x , mid_y) , 5 , red , -1)

    # Show the resulting image
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # sort the dictionaries by the value of y
    sorted_pointsXY = sorted(points, key=lambda d: d['y'])
    sorted_points_x = sorted(points , key= lambda d: d['x'])
    points.clear()

    return sorted_points_x , sorted_pointsXY , image

def detect_corners(image , draw = False):

    corner_points = []
    image = cv2.resize(image , (640 , 640))

    # Convert the image from OpenCV format to PyTorch tensor format
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Run the inference on the input image using the loaded YOLO model
    outputs = corner_model(image)

    # Parse the outputs and extract the predicted bounding boxes, class labels, and confidence scores
    results = outputs.xyxy[0].numpy()
    boxes = results[:, :4]
    labels = results[:, 5]
    scores = results[:, 4]

    # Visualize the predicted bounding boxes on the input image using OpenCV
    for i in range(len(boxes)):
        box = boxes[i]
        score = scores[i]
        color = (0, 255, 0)  # green
        x1, y1, x2, y2 = box.astype(np.int32)

        # the middle points of the detections
        if score > 0.6:
            mid_x = int(((x2 - x1) / 2) + x1)
            mid_y = int(((y2 - y1) / 2) + y1)

            point_tup = (mid_x , mid_y)
            corner_points.append(point_tup)

            if draw:
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 1)
                cv2.circle(image , (mid_x , mid_y) , 10 , color , -1)

    return image , len(corner_points) ,  warper.rearange_points(corner_points)

if __name__ == '__main__':

    image = cv2.imread(r"C:\python\open_cv\object_detection\test_corrector\aug\ann\2.jpg")
    cv2.imshow("image" , detect_test(image)[2])
    cv2.waitKey(0)
