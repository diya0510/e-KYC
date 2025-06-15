import os
import easyocr
import cv2


def extract_text(image,threshold=0.3,languages=['en']):
    reader=easyocr.Reader(languages)
    try:
        result=reader.readtext(image)
        filtered_text='|'
        for r in result:
            bounding_box,text,confidence=r
            if confidence>threshold:
                filtered_text+=text+'|'
        return filtered_text
    except Exception as e:
        print("Error extracting text from image",e)
        return ""


