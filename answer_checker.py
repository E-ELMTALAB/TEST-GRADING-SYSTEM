### answer checker file

from itertools import zip_longest
import numpy as np
import cv2

ground_truth = [3,1,4,2,3,1,2,4,3,2,1,2,1,4,3,1,2,1,2,1,3,1,2,3,1,3,4,1,2,2,1,3,1,3,1,1,4,2,1,3,1,3,1,2,3,2,1,3,2,4,1]

def find_main_Xpoints(pointsY):

    i = k = 0
    exist = False
    x_points = []
    chart = []
    y = pointsY[0]["y"]

    while i != len(pointsY):

        if not (y - 7 < pointsY[i]["y"] < y + 7)  :

            # each line of the points are now sorted
            sorted_chart = sorted(chart , key= lambda d: d['x'])

            for dict in sorted_chart : 
                x1 = dict["x"]

                for element in x_points :
                    if (x1 - 15 < element < x1 + 15):
                       exist = True

                if not exist :
                    x_points.append(x1)

                exist = False

            chart = []
            y = pointsY[i]["y"]

            i = i - 1
            k = k + 1
            
            if k == 6:
                break
            
        else :
            chart.append(pointsY[i])

        i += 1

    return x_points

def organize_answers(pointsY):

    # find the x points that all of the tick boxes rely in
    x_points = find_main_Xpoints(pointsY)

    i = 0
    exist = False
    chart = []
    points = []
    right_points = []
    middle_points = []
    y = pointsY[0]["y"]

    while i != len(pointsY):

        if not (y - 7 < pointsY[i]["y"] < y + 7)  :

            # each line of the points are now sorted
            sorted_chart = sorted(chart , key= lambda d: d['x'])
            if not (len(sorted_chart) % 2 == 0) or not (len(sorted_chart) == len(x_points)):

                for element in x_points :
                    for dict in sorted_chart:
                        x = dict["x"]

                        if (x - 15 < element < x + 15):
                            exist = True
                            break  

                    if not exist:                      
                        replacement_dict = {"class": "un_known" , "x": element , "y": y}
                        sorted_chart.append(replacement_dict)
                        sorted_chart = sorted(sorted_chart , key = lambda d: d["x"])

                    exist = False

            # now each line is divided by 4 
            sorted_chart_sliced = [list(filter(None, sublist)) for sublist in zip_longest(*([iter(sorted_chart)] * 4), fillvalue=None)]

            match len(sorted_chart_sliced):

                case 1:
                    points.append(sorted_chart_sliced[0])
                case 2:
                    points.append(sorted_chart_sliced[0])
                    middle_points.append(sorted_chart_sliced[1])
                case 3:
                    points.append(sorted_chart_sliced[0])
                    middle_points.append(sorted_chart_sliced[1])
                    right_points.append(sorted_chart_sliced[2])

            chart = []
            y = pointsY[i]["y"]

            i = i - 1

        else :
            chart.append(pointsY[i])

        if (i == len(pointsY) - 1):
                    
            sorted_chart = sorted(chart , key= lambda d: d['x'])

            if not (len(sorted_chart) % 2 == 0) or not (len(sorted_chart) == len(x_points)):

                for element in x_points :
                    for dict in sorted_chart:

                        x = dict["x"]

                        if (x - 15 < element < x + 15):
                            exist = True
                            break  

                    if not exist:                      

                        replacement_dict = {"class": "un_known" , "x": element , "y": y}
                        sorted_chart.append(replacement_dict)
                        sorted_chart = sorted(sorted_chart , key = lambda d: d["x"])

                    exist = False

            # now each line is divided by 4 
            sorted_chart_sliced = [list(filter(None, sublist)) for sublist in zip_longest(*([iter(sorted_chart)] * 4), fillvalue=None)]

            match len(sorted_chart_sliced):

                case 1:
                    points.append(sorted_chart_sliced[0])
                case 2:
                    points.append(sorted_chart_sliced[0])
                    middle_points.append(sorted_chart_sliced[1])
                case 3:
                    points.append(sorted_chart_sliced[0])
                    middle_points.append(sorted_chart_sliced[1])
                    right_points.append(sorted_chart_sliced[2])

        i += 1

    for i in range(len(right_points)):
        middle_points.append(right_points[i])

    for i in range(len(middle_points)):
        points.append(middle_points[i])

    return points

def check_answers(points):

    num = 0
    correct_answers_index = np.zeros_like(points)
    answers = np.zeros(200 , np.uint8)

    for i , four_options in enumerate(points):
        for j , option in enumerate(four_options):
            
            if option["class"] == "marked":
                answers[i] = j+1
                correct_answers_index[i][j] = 1

            else :
                correct_answers_index[i][j] = 0

    answers = answers[answers != 0]
    correct_answers_index = np.array(list(filter(lambda x : True if x[0]+x[1]+x[2]+x[3] else False , correct_answers_index)))

    for answer , ground in zip(answers , ground_truth):
        if answer == ground:
            num = num + 1

    return num , correct_answers_index

# transform the number based answers to list based
def transform_number(ground_truth):

    trans_list = np.zeros((len(ground_truth) , 4) , np.uint8)

    for answer , list in zip(ground_truth , trans_list):
        list[answer - 1] = 1

    return trans_list

# transform the list based answers to number based
def transform_list(answers):

    number_list = np.zeros(len(answers) , np.uint8)

    for j , answer in enumerate(answers):
        for i , point in enumerate(answer):
            if point:

                number_list[j] = i + 1

    return number_list

# showing the right and wrong answer on the image
def show_right_answers(image , right_answers_list , ground_truths_number, points):

    new_points = []
    right_answers_number = transform_list(right_answers_list)

    for point in points :
        num = 0

        for dict in point:
            if (dict["class"] == "un_known") :
                num += 1

        if (num != 4):  
            new_points.append(point)

    for answer , truth , point in zip(right_answers_number , ground_truths_number , new_points):

        if (answer == truth):
            cv2.circle(image , (point[answer - 1]["x"] , point[answer - 1]["y"]) , 5 , (0 , 255 , 0) , - 1)

        else:
            cv2.circle(image , (point[answer - 1]["x"] , point[answer - 1]["y"]) ,  5 , (0 , 255 , 0) , - 1)
            cv2.circle(image , (point[truth - 1]["x"] , point[truth - 1]["y"]) ,  5 , (0 , 0 , 255) , - 1)
        
    return image

