### box finder and sliscer

import cv2
import numpy as np 

# variables
red = (0 ,0 ,255 )
blue = (255 ,0 ,0)
green = (0 ,255 ,0 )
magenta = (255 ,0 ,255)
warped_h = width = 640
warped_w = height = 640
detected = False 


def warp(image , four_points):

        # four_points = rearange_points(points)
        points1 = np.float32(four_points)
        points2 = np.float32([[0, 0], [warped_w, 0], [warped_w, warped_h],[0, warped_h]])

        #warping the image and putting text on it
        transformation_matrix = cv2.getPerspectiveTransform(points1, points2)
        warped_img = cv2.warpPerspective(image, transformation_matrix, (warped_w, warped_h))

        return warped_img , points1 , points2


def rewarp(image , points1 , points2 , warped_img):

        #creating the mask 
        mask = np.zeros(image.shape, dtype=np.uint8)
        roi_corners = np.int32(points1)
        mask = cv2.fillConvexPoly(mask, roi_corners, (255, 255, 255))
        mask = cv2.bitwise_not(mask)

        #bitwise_and operation
        bitwise_and_img = cv2.bitwise_and(mask , image)

        # rewarped doc image
        transformation_matrix = cv2.getPerspectiveTransform(points2, points1)
        # print("widht " + str(width) + "height " + str(height) )
        rewarped_img = cv2.warpPerspective(warped_img, transformation_matrix, (width, height))

        # bitwise or to get the final image 
        final_img = cv2.bitwise_or(rewarped_img , bitwise_and_img)
        # final_img = cv2.addWeighted(bitwise_and_img , 0.5 , rewarped_img , 0.5 , 0)
        image = final_img
        return image
    

def rearange_points(points):
    
    sorted_pts = np.zeros((4, 2), dtype="int32")
    s = np.sum(points, axis=1)
    sorted_pts[0] = points[np.argmin(s)]
    sorted_pts[2] = points[np.argmax(s)]

    diff = np.diff(points, axis=1)
    sorted_pts[1] = points[np.argmin(diff)]
    sorted_pts[3] = points[np.argmax(diff)]

    return sorted_pts

def find_four_points(image , processed_image , draw= False , circle = False):

#### needed variable
    square_points = [] # where we keep our four points of square
    final_img = None

#### finding the contours 
    contours, hierarchy = cv2.findContours(processed_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    # cv2.drawContours(image, cnt, -1, (0, 255, 255), 3)

#### searching for the biggest rectangle or the square in the image
    epsilon = 0.1 * cv2.arcLength(cnt , True)
    approximations = cv2.approxPolyDP(cnt, epsilon, True)
    i, j = approximations[0][0] 
    if len(approximations) == 4:

######## square detected
        detected = True

######## setting th opsitoins
        left_top = (int(approximations[0][0][0]) , int(approximations[0][0][1]))
        left_bottom = (int(approximations[1][0][0]) , int(approximations[1][0][1]))
        right_bottom = (int(approximations[2][0][0]) , int(approximations[2][0][1]))
        right_top = (int(approximations[3][0][0]) , int(approximations[3][0][1]))
        square_points = [left_top , right_top , right_bottom , left_bottom]
        square_points = rearange_points(square_points)

######## if drawing the four points was intended
        if draw and not circle:

            cv2.line(image , square_points[0] , left_bottom , red , 3) # left_top
            cv2.line(image ,square_points[1] , right_bottom , blue , 3) # right_top
            cv2.line(image , square_points[2] , right_top , green , 3) # right_ bottom
            cv2.line(image , square_points[3] , left_top , magenta , 3) # left_bottom

        if draw and circle :

            cv2.circle(image , square_points[0] , 10 , red , -1)
            cv2.circle(image , square_points[1] , 10 , blue , -1)
            cv2.circle(image , square_points[2] , 10 , green , -1)
            cv2.circle(image , square_points[3] , 10 , magenta , -1)

    else:
        detected = False

    return detected , square_points , image

