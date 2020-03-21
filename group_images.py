import cv2
import numpy as np
import os
import shutil


def check_match(img_1, img_2):
    # Check if 2 images are equals
    if img_1.shape == img_2.shape:
        #print("The images have same size and channels")
        difference = cv2.subtract(img_1, img_2)
        b, g, r = cv2.split(difference)

        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            print('same image')
            return True
        #else:
            #return False

    # 2) Check for similarities between the 2 images
    sift = cv2.xfeatures2d.SIFT_create()
    kp_1, desc_1 = sift.detectAndCompute(img_1, None)
    kp_2, desc_2 = sift.detectAndCompute(img_2, None)

    index_params = dict(algorithm=0, trees=5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    match = flann.knnMatch(desc_1, desc_2, k=2)
    match_rev = flann.knnMatch(desc_2, desc_1, k=2)

    # Define how similar they are
    number_keypoints = 0
    if len(kp_1) <= len(kp_2):
        number_keypoints = len(kp_1)
    else:
        number_keypoints = len(kp_2)

    good_points = []
    for m, n in match:
        if m.distance < 0.6*n.distance:
            good_points.append(m)

    # good points after reversing the order of images
    good_points_rev = []
    for m, n in match_rev:
        if m.distance < 0.6*n.distance:
            good_points_rev.append(m)


    match_percentage = len(good_points) / number_keypoints * 100
    print('match per: ', match_percentage)
    # match percentage after reversing the order of images
    rev_match_percentage = len(good_points_rev) / number_keypoints * 100
    print('rev match per: ', rev_match_percentage)

    #result = cv2.drawMatches(img_1, kp_1, img_2, kp_2, good_points, None)
    #cv2.imshow("result", cv2.resize(result, None, fx=0.4, fy=0.4))
    #cv2.waitKey(0)

    if match_percentage >= 1 and rev_match_percentage >= 1:
        return True
    else:
        return False


def group_images(file_list, new_list):
    for i, file_1 in enumerate(file_list):
        temp_list = [file_1]    # Storing the file which have been checked
        for j, file_2 in enumerate(file_list):
            if j <= i:
                continue
            else:
                img_1 = cv2.imread(os.path.join('pics', file_1))
                img_2 = cv2.imread(os.path.join('pics', file_2))
                if check_match(img_1, img_2) == True:    # Checking if the two images are similar
                    temp_list.append(file_list[j])   # Temporarily storing the matched files
        #print("temp list: ", temp_list)
        file_list = [x for x in file_list if x not in temp_list]  # Removing the matched files from the original list
        #print("file list: ", file_list)
        new_list.append(temp_list)    # New list of grouped files
        #print("new list: ", new_list)
        return file_list, new_list
    return file_list, new_list



def main():
    src_path = 'pics'     # Source path
    dest_path = 'grouped'   #Destination path
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    file_list = os.listdir(src_path)
    new_list = []    # Empty list for storing grouped files
    while file_list:
        file_list, new_list = group_images(file_list, new_list)
        #print(file_list_copy)


    # Copying the grouped files in different folders
    for i, files in enumerate(new_list):
        new_dest_path = os.path.join(dest_path, str(i))
        if not os.path.exists(os.path.join(new_dest_path)):
            os.mkdir(new_dest_path)

        for file in files:
            shutil.copy(os.path.join(src_path, file), os.path.join(new_dest_path, file))


if __name__ == '__main__':
    main()
