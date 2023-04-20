# Computer Vision-Based Automated Test Grading System

The traditional method of manually grading tests in educational institutions, although widely practiced, may not necessarily be the most effective approach. It is time-consuming and susceptible to human error and fallibility. In light of this challenge, this project endeavors to employ advanced techniques in computer vision and image processing, along with the utilization of the Python programming language, to offer a solution to this issue.

This particular project aims to utilize the YOLOv5s model, which has been trained on Colab, to detect individual tests and determine whether or not they have been marked. The tests are then sorted into groups of four, and their answers are checked accordingly. To facilitate this process, various image processing techniques such as dilation and erosion are employed to enhance the visibility of the tests for the model. Initially, each of the paper's corners is detected, and these points are then utilized to generate a warped image of the paper, making it easier for the model to make accurate predictions. Subsequently, after organizing the individual tests and verifying the ground truth answers provided by the user, the system showcases both the correct and incorrect answers, as well as the true answers themselves, using augmented reality techniques directly on the paper.


## Screenshots
Included below are several images showcasing the functionality  of the project



![Screenshot (198)](https://user-images.githubusercontent.com/117757969/233491843-36748a53-a742-4384-a511-2e98fe57e381.png)

![Screenshot (199)](https://user-images.githubusercontent.com/117757969/233491848-db786a62-55c4-48b1-90e2-bc816c2686f6.png)

![Screenshot (200)](https://user-images.githubusercontent.com/117757969/233491852-c5490a7d-3dfe-4bd4-815f-56dee32ac20d.png)



## Optimizations

1 - The present model has been trained on a relatively modest dataset of 1700 images, which implies that the accuracy and f1 score of the model could be enhanced significantly by training it on a larger dataset containing diverse images. This would help the model to learn more effectively and be better prepared for a variety of scenarios.

2 - The algorithm implemented in the program is intricate and may not be easy to comprehend, necessitating the use of more advanced algorithms to manage answers, correct misidentified tests, and enhance the images for easier detection by the model. For instance, more combinations of techniques such as image dilation\erosion , adaptive threshold , edges detection and more could be employed to improve the visibility of the tests and allow for more accurate predictions.

3 - Tracking algorithms could be incorporated into the program to enable the model to predict the test results every i'th frame, making the whole process of real-time feel more like real-time. This would ensure that the program remains up-to-date with the latest developments and trends, and that users can have the most accurate and up-to-date results.

4 - A graphical user interface could also be added to the program to facilitate its usage, particularly when inputting ground truth answers to the program. This would make it easier for users to navigate and interact with the program, allowing them to provide accurate information and receive accurate results.

5 - A database could also be implemented to store test grades and the corresponding student names. This would allow users to easily access and analyze the data, making it easier to track student progress and identify areas of improvement. Additionally, it would ensure that the program remains organized and efficient, and that data is stored securely and reliably.

NOTE :  Overall, this project is a demonstration of the technology, and all of the aforementioned features could be integrated into the program if it were to become commercial. This would enable the program to be more versatile and effective, and to serve a wider range of users and purposes.
