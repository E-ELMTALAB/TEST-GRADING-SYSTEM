### main file

import detector , cv2 , time
import sheet_finder_warper as sheet_finder
import answer_checker as checker

# necessary variables
flag = 1
red = (0 ,0 ,255 )
blue = (255 ,0 ,0)
green = (0 ,255 ,0 )
magenta = (255 ,0 ,255)
cTime = pTime = iteration = i  = 0
ground_truth_number = [3,1,4,2,3,1,2,1,3,2,1,2,1,4,3,1,2,1,2,1,3,1,2,1,1,3,4,1,2,2,1,3,1,3,1,1,4,4,1,3,1,3,1,3,3,2,1,3,2,4,1]

# loading the video 
cap = cv2.VideoCapture(r"C:\Users\Morvarid\Documents\VID_20230326_152300 (online-video-cutter.com).mp4")

# run until the user presses the "q" button
while cv2.waitKey(1) != ord("q"):

    # reading the frame from the video
    _ , orig = cap.read()

    # computer the fps 
    cTime = time.time()
    if pTime != 0:
        fps = 1 / (cTime - pTime)
        cv2.putText(orig, str(int(fps)), (50, 200), cv2.FONT_HERSHEY_PLAIN , 10, (0, 255, 0), 13)
    pTime = cTime

    # predict every i'th frames
    if flag : 

        # apply errosion and adaptive threshold 
        processed = detector.pre_process(orig , 16)

        # detect corners of paper for warping 
        image , corner_length , corner_points = detector.detect_corners(orig , True)

        # if all four corners were detected begin the main job 
        if corner_length == 4:

            # warp the image using the corner points returned by the corner detector
            orig_warped , po , so = sheet_finder.warp(cv2.resize(orig , (640 , 640)) , corner_points)
            warped , s , h = sheet_finder.warp(cv2.resize(processed , (640 , 640)) , corner_points)

            # detect the test 
            points_x , pointsXY , detected = detector.detect_test( warped , True)

            # organize the test tick boxes
            org_points = checker.organize_answers(pointsXY)

            # compare and show the answers of the paper to the ground truth answer given by the user
            right_answers_num , right_answers_list = checker.check_answers(org_points)
            corrected = checker.show_right_answers(orig_warped , right_answers_list , ground_truth_number , org_points)

            # rewarp the warped image on the original image 
            rewarped = sheet_finder.rewarp(cv2.resize(orig , (640 , 640)) , po , so , corrected)

        flag = 0

    # used for making prediction every i'th frame 
    if not flag:
        iteration += 1
        if (iteration == 4):
            flag = 1
            iteration = 0


    cv2.imshow("detected" , detected )
    cv2.imshow("wapred" , rewarped)
    cv2.imshow("image" , image)

