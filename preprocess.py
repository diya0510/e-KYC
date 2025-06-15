import cv2 
import matplotlib.pyplot as plt
import numpy as np
import os 
from utils import file_exists,read_yaml

config_path = "config.yaml"
config = read_yaml(config_path)

artifacts = config['artifacts']
intermediate_dir_path = artifacts['INTERMIDEIATE_DIR']
contour_file_name = artifacts['CONTOUR_FILE']

def read_image(image_path,is_uploaded=False):
    if is_uploaded:
        try:
            img_bytes=image_path.read()
            image=cv2.imdecode(np.frombuffer(img_bytes,np.uint8),cv2.IMREAD_COLOR)
            if image is None:
                raise Exception("Failed to read image {}".format(image_path))
            return image
        except Exception as e:
            print("Error reading image",e)
            return None
    else:
        try:
            image=cv2.imread(image_path)
            if image is None:
                raise Exception("Failed to read image {}".format(image_path))
            return image
        except Exception as e:
            print("Error reading image")
            return None
        
def extract_idcard(image):
    gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),0)
    thresh=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 11, 2)
     
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

   
    largest_contour = None
    largest_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > largest_area:
            largest_contour = cnt
            largest_area = area

   
    if not largest_contour.any():
        return None

    # Get bounding rectangle of the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)

   
    

    
    filtered_img = cv2.bilateralFilter(image[y:y+h, x:x+w], 9, 75, 75)
   
    current_wd = os.getcwd()
    filename = os.path.join(current_wd,intermediate_dir_path, contour_file_name)
    contour_id = image[y:y+h, x:x+w]
    is_exists = file_exists(filename)
    if is_exists:
        # Remove the existing file
        os.remove(filename)

    cv2.imwrite(filename, contour_id)

    return contour_id, filename



def save_image(img, filename, path="data\\02_intermediate_data"):
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(full_path, exist_ok=True)
    file_path = os.path.join(full_path, filename)
    cv2.imwrite(file_path, img)
    return file_path


        