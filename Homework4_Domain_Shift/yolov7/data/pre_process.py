import os
import glob
import random
import argparse

CLASS_NAME = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
    'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
    'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
    'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
    'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
    'hair drier', 'toothbrush'
]


# Q2 and Q3 TODO : select "better" images from Q2 folder
def select_imaegs(image_paths, images_num=200):
    ####### Random #######
    # random.shuffle(image_paths)
    # selected_image_paths = image_paths[:images_num]
    ######################

    ####### Averagely Random #######
    img170 = list(filter(lambda s: '170/170' in s, image_paths))
    img173 = list(filter(lambda s: '173/173' in s, image_paths))
    img398 = list(filter(lambda s: '398/398' in s, image_paths))
    img410 = list(filter(lambda s: '410/410' in s, image_paths))
    img495 = list(filter(lambda s: '495/495' in s, image_paths))
    img511 = list(filter(lambda s: '511/511' in s, image_paths))

    random.shuffle(img170)
    random.shuffle(img495)
    random.shuffle(img410)
    random.shuffle(img511)
    random.shuffle(img398)
    random.shuffle(img173)

    selected_image_paths = img170[:33] + img173[:34] + img398[:34] + img410[:33] + img495[:33] + img511[:33]
    ######################

    ###### Select Most # of objects ######
    # amount_dict = {}
    # for path in image_paths:
    #     txt_name = path.replace('jpg', 'txt')
    #     with open(txt_name, 'r') as fh:
    #         obj = fh.readlines()
    #         amount_dict[txt_name] = len(obj)
    # image_paths.sort(key=lambda amount: amount_dict[amount], reverse=True)
    # selected_image_paths = image_paths[:images_num]
    # ###########################################

    ###### Averagely Select Most # of Objects ######
    # img170 = list(filter(lambda s: '170/170' in s, image_paths))
    # img173 = list(filter(lambda s: '173/173' in s, image_paths))
    # img398 = list(filter(lambda s: '398/398' in s, image_paths))
    # img410 = list(filter(lambda s: '410/410' in s, image_paths))
    # img495 = list(filter(lambda s: '495/495' in s, image_paths))
    # img511 = list(filter(lambda s: '511/511' in s, image_paths))
    #
    # img_folder_paths = [img170, img173, img398, img410, img495, img511]
    # img_folder_path_ = []
    # for folder in img_folder_paths:
    #     amount_dict = {}
    #     for path in folder:
    #         txt_name = path.replace('jpg', 'txt')
    #         with open(txt_name, 'r') as fh:
    #             obj = fh.readlines()
    #             amount_dict[txt_name] = len(obj)
    #     img_folder_path_.append(amount_dict)
    # for idx, i in enumerate(img_folder_path_):
    #     img_folder_paths[i].sort(key=lambda amount: img_folder_path_[i][amount], reverse=True)
    #
    # selected_image_paths = img_folder_paths[0][:33] + img_folder_paths[1][:33] + img_folder_paths[2][:33] + img_folder_paths[3][:33] + img_folder_paths[4][:34] + img_folder_paths[5][:34]
    ##########################################



    ###### Select Most Class ######
    # amount_dict = {}
    # for path in image_paths:
    #     cls = ""
    #     txt_name = path.replace('jpg', 'txt')
    #     with open(txt_name, 'r') as fh:
    #         obj = fh.readlines()
    #         for i in obj:
    #             if i[0] not in cls:
    #                 cls+=i[0]
    #         _ = str(len(cls)) + str(len(obj))
    #         amount_dict[txt_name] = int(str(len(cls)) + "0"*(3-len(_)) + str(len(obj)))
    # image_paths.sort(key=lambda amount: amount_dict[amount], reverse=True)
    # selected_image_paths = image_paths[:images_num]
    # ###########################################

    ###### Averagely Select Most Class ######
    # img170 = list(filter(lambda s: '170/170' in s, image_paths))
    # img173 = list(filter(lambda s: '173/173' in s, image_paths))
    # img398 = list(filter(lambda s: '398/398' in s, image_paths))
    # img410 = list(filter(lambda s: '410/410' in s, image_paths))
    # img495 = list(filter(lambda s: '495/495' in s, image_paths))
    # img511 = list(filter(lambda s: '511/511' in s, image_paths))
    #
    # img_folder_paths = [img170, img173, img398, img410, img495, img511]
    # img_folder_path_ = []
    # for folder in img_folder_paths:
    #     amount_dict = {}
    #     for path in folder:
    #         cls = ""
    #         txt_name = path.replace('jpg', 'txt')
    #         with open(txt_name, 'r') as fh:
    #             obj = fh.readlines()
    #             for i in obj:
    #                 if i[0] not in cls:
    #                     cls+=i[0]
    #             _ = str(len(cls)) + str(len(obj))
    #             amount_dict[txt_name] = int(str(len(cls)) + "0"*(3-len(_)) + str(len(obj)))
    #     img_folder_path_.append(amount_dict)
    # for idx, i in enumerate(img_folder_path_):
    #     img_folder_paths[i].sort(key=lambda amount: img_folder_path_[i][amount], reverse=True)
    #
    # selected_image_paths = img_folder_paths[0][:33] + img_folder_paths[1][:33] + img_folder_paths[2][:33] + img_folder_paths[3][:33] + img_folder_paths[4][:34] + img_folder_paths[5][:34]
    ##########################################

    return selected_image_paths


# TODO : split train and val images
def split_train_val_path(all_image_paths, train_val_ratio=0.9):
    random.shuffle(all_image_paths)
    train_image_paths = all_image_paths[: int(len(all_image_paths) * train_val_ratio)]
    val_image_paths = all_image_paths[int(len(all_image_paths) * train_val_ratio):]

    return train_image_paths, val_image_paths


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_folder', type=str, default='./data/CityCam', help='path of CityCam datasets folder')
    parser.add_argument('--ques', type=str, default='Q1', choices=['Q1', 'Q2', 'Q3'], help='question in data_folder')
    args = parser.parse_args()
    print(args)

    # Get whole and Test image paths
    all_image_paths = glob.glob(os.path.join(args.data_folder, args.ques, '*', '*.jpg'))
    test_image_paths = glob.glob(os.path.join(args.data_folder, 'test', '*' + os.sep + '*.jpg'))

    # for Q2 and Q3 : select images
    if args.ques == 'Q2' or args.ques == 'Q3':
        selected_image_paths = select_imaegs(all_image_paths, images_num=200)
    else:
        selected_image_paths = all_image_paths
    # split Train and Val
    train_image_paths, val_image_paths = split_train_val_path(selected_image_paths)

    # write train/val/test info
    train_path = os.path.join(args.data_folder, 'train.txt')
    val_path = os.path.join(args.data_folder, 'val.txt')
    test_path = os.path.join(args.data_folder, 'test.txt')
    with open(train_path, 'w') as f:
        for image_path in train_image_paths:
            f.write(os.path.abspath(image_path) + '\n')
    with open(val_path, 'w') as f:
        for image_path in val_image_paths:
            f.write(os.path.abspath(image_path) + '\n')
    with open(test_path, 'w') as f:
        for image_path in test_image_paths:
            f.write(os.path.abspath(image_path) + '\n')

    # write training YAML file
    with open('./data/citycam.yaml', 'w') as f:
        f.write("train: " + os.path.abspath(train_path) + "\n")
        f.write("val: " + os.path.abspath(val_path) + "\n")
        f.write("test: " + os.path.abspath(test_path) + "\n")
        # number of classes
        f.write('nc: 80\n')
        # class names
        f.write('names: ' + str(CLASS_NAME))

    # delete cache
    if os.path.exists(os.path.join(args.data_folder, 'train.cache')):
        os.remove(os.path.join(args.data_folder, 'train.cache'))
    if os.path.exists(os.path.join(args.data_folder, 'val.cache')):
        os.remove(os.path.join(args.data_folder, 'val.cache'))
    """
    if os.path.exists(os.path.join(args.data_folder, 'test.cache')):
        os.remove(os.path.join(args.data_folder, 'test.cache'))
        """
