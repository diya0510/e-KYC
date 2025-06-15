from deepface import DeepFace
import os 
from utils import file_exists,read_yaml

import cv2
import os
import numpy as np

config_path = "config.yaml"
config = read_yaml(config_path)
artifacts = config['artifacts']

cascade_path=artifacts["HAARCASCADE_PATH"]
output_path = artifacts['INTERMIDEIATE_DIR']


def detect_and_extract_face(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    face_cascade = cv2.CascadeClassifier(cascade_path)

    if face_cascade.empty():
        print("Error loading Haar cascade XML file.")
        return None

    faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)

    max_area = 0
    largest_face = None
    for (x, y, w, h) in faces:
        area = w * h
        if area > max_area:
            largest_face = (x, y, w, h)

    if largest_face is not None:
        (x, y, w, h) = largest_face
        new_w = int(w * 1.5)
        new_h = int(h * 1.5)
        new_x = max(0, x - int((new_w - w) / 2))
        new_y = max(0, y - int((new_h - h) / 2))

        # Clip to image boundaries
        img_height, img_width = img.shape[:2]
        end_y = min(new_y + new_h, img_height)
        end_x = min(new_x + new_w, img_width)

        extracted_face = img[new_y:end_y, new_x:end_x]

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Always points to your script's location
        filename = os.path.join(BASE_DIR, output_path, "extracted_face.jpg")
        if file_exists(filename):
            os.remove(filename)
        cv2.imwrite(filename, extracted_face)
        print(f"Extracted face saved at: {filename}")
        return filename
    else:
        print("Unable to detect face")
        return None


# def face_recog_face_compare(image1_path="data\\02_intermediate_data\\extracted_face.jpg", image2_path = "data\\02_intermediate_data\\face_image.jpg"):
#     img1_exists=file_exists(image1_path)
#     img2_exists=file_exists(image2_path)

#     if not(img1_exists and img2_exists):
#         print("check one or both images path")
#         return False
#     img1=face_recognition.load_image_file(image1_path)
#     img2=face_recognition.load_image_file(image2_path)

#     if img1 is not None or img2 is not None:
#         face_encodings1=face_recognition.face_encodings(img1)
#         face_encodings2=face_recognition.face_encodings(img2)
#     else:
#         print("Image not loaded properly")
#         return False
    
#     if len(face_encodings1)==0 or len(face_encodings2)==0:
#         print("No face detected in one or both images")
#         return False
#     else:
#         matches=face_recognition.compare_faces(np.array(face_encodings1),np.array(face_encodings2))

#         if matches[0]:
#             print("The faces are similar")
#             return True
#         else:
#             print("The faces do not match")
#             return False


def face_comparison(image1_path, image2_path):
    is_verified=False
    img1_exists = file_exists(image1_path)
    img2_exists = file_exists(image2_path)

    if not(img1_exists and img2_exists):
        print("Check the path for the images provided")
        return False
    
    verfication = DeepFace.verify(img1_path=image1_path, img2_path=image2_path)

    if len(verfication) > 0 and verfication['verified']:
        print("Faces are verified")
        return True
    else:
        return False
    



