# Similar_image_clustering

### Prerequisites
Python 3.6+ version
cv2 version 3.4.2.17

### How to run
Execute the following commands.

```
  pip install opencv-python==3.4.2.16
  
  pip install opencv-contrib-python==3.4.2.16

  python group_images.py
  ```
  ### Test a new dataset
  Copy the images in 'pics' directory and run the script again
  
  After execution of the script, a new directory will be created named 'grouped' which will contain the output.
  
  ### Approach
  
  I used the simplest approach I could find to solve this problem. I used python's pre-built library, CV2 because I believe that there's no need of re-inventing the wheel. My script works in the following manner:
  1. The images in the dataset are checked if they are equal.
  2. Then the images are compared to find percentage of similarity between them.
  3. If similarity percentage is above a threshold value or if they are equal then the images are kept in the same group.
  
 ### Accuracy
 For the given data, there is 1 False Positive in a corpus of 20 images.
 
