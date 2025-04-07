Homework 4 - Handling Domain Shift with YOLOv7
Course
Computer Vision (CS5658), Instructor: Prof. Min Sun

Objective
This assignment aims to tackle the domain shift problem in object detection tasks using the YOLOv7 model. The dataset used is CityCam, which includes surveillance images taken from multiple cameras during both day and night. The homework is divided into three parts: Q1, Q2, and Q3.

Q1: Training and Evaluation per Camera
We implemented the split_train_val_path() function to split the training and validation sets by camera. We then fine-tuned a YOLOv7 model on the Q1 dataset using only the default training set and analyzed its detection performance (mAP scores) across different cameras. The goal is to understand whether training on images from specific cameras leads to camera-specific biases or generalizable features.

Q2: Comparison of Data Selection Strategies
We investigated the effect of data selection strategies on the performance of YOLOv7 models. Several strategies were explored, including:

Random selection

Average random selection (average number of images per camera)

Object count-based selection

Class diversity-based selection

Each strategy was evaluated using mAP@0.5 and mAP@0.5:0.95 scores. Our goal was to understand whether selecting images based on their information richness (e.g., number of objects or number of classes) leads to better detection performance, compared to random sampling.

Q3: Domain-Specific Training
In this part, we investigated whether using only daytime or nighttime training data leads to better performance, especially considering that the test set contains only daytime images.

We defined three training sets:

All: Contains both day and night images (491 images total).

Day only: Contains only daytime images (298 images).

Night only: Contains only nighttime images (193 images).

We trained a YOLOv7-tiny model on each of the three datasets using identical training parameters. We then evaluated each model on the validation set and compared their performance.

Since the test set consists solely of daytime images, we hypothesized that training with only daytime data would yield the best performance, as night images may introduce noise or irrelevant features that hurt generalization to day scenarios.

Conclusion
Through these experiments, we explored how domain-specific characteristics and data selection methods affect the performance of object detection models under domain shift. We found that carefully selecting training data based on time of day or object statistics can significantly impact the final performance on unseen target domains.

Environment
Python 3.8+

PyTorch 1.13+

YOLOv7 repository (https://github.com/WongKinYiu/yolov7)

NVIDIA GPU (tested on RTX 3090)