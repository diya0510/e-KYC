import cv2
import os
import streamlit as st
from sqlalchemy import text
from preprocess import read_image,extract_idcard,save_image
from ocr_engine import extract_text
from postprocess import extract_information
from mysql_operations import insert_records,fetch_data,duplicacy
from face_recognition import detect_and_extract_face, face_comparison
from datetime import datetime





def format_dob(dob):
    if isinstance(dob, datetime):
        return dob.strftime('%Y-%m-%d')
    elif isinstance(dob, str):
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(dob.strip(), fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
    return "NA"  # fallback if invalid

def wider_page():
    max_width_str = "max-width: 1200px;"
    st.markdown(
        f"""
        <style>
            .reportview-container .main .block-container{{ {max_width_str} }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def set_custom_theme():
    st.markdown(
        """
        <style>
            body {
                background-color: #f0f2f6; /* Set background color */
                color: #333333; /* Set text color */
            }
            .sidebar .sidebar-content {
                background-color: #ffffff; /* Set sidebar background color */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
def sidebar_section():
    st.sidebar.title("Select ID Card Type")
    
def main_content(image_file,fac_image_file,conn):
    if image_file is not None:
        face_image=read_image(fac_image_file,is_uploaded=True)
        if face_image is not None:
            image=read_image(image_file,is_uploaded=True)
            image_roi,_=extract_idcard(image)
            face_image_path2 = detect_and_extract_face(img=image_roi)
            face_image_path1 = save_image(face_image, "face_image.jpg", path="data\\02_intermediate_data")
            print("Face image path 1:", face_image_path1)
            print("Face image path 2:", face_image_path2)

            if face_image_path1 and face_image_path2:
                is_face_verified = face_comparison(image1_path=face_image_path1, image2_path=face_image_path2)
                
                if is_face_verified:
                    extracted_text = extract_text(image_roi)
                    text_info = extract_information(extracted_text)
                    print("Extrected text",extracted_text)
                    print("Parsed info",text_info)
                    if text_info is None or 'ID' not in text_info:
                        st.error("Could not extract ID")
                        return 
                    records = fetch_data(text_info)
                    if records.shape[0] > 0:
                        st.write(records.shape)
                        st.write(records)
                    is_duplicate = duplicacy(text_info)
                    if is_duplicate:
                        st.write(f"User already present with ID {text_info['ID']}")
                    else: 
                        st.write(text_info)
                        if isinstance(text_info['DOB'], datetime):
                             text_info['DOB'] = text_info['DOB'].strftime('%Y-%m-%d')
                        elif isinstance(text_info['DOB'], str):
                             try:
                                  dt = datetime.strptime(text_info['DOB'], '%d/%m/%Y')
                                  text_info['DOB'] = dt.strftime('%Y-%m-%d')
                             except ValueError:
                                 pass  # Leave it as-is if it fails to parse
                        if not text_info['DOB'] or text_info['DOB'].strip() == "":
                            text_info['DOB'] = None

                        insert_records(text_info)
                else:
                    print("Face verification failed ")
                    
            else:
                st.error("No image1 path.")

        else:
            st.error("Face image not uploaded. Please upload a face image.")
            

    else:
        st.warning("Please upload an ID card image.")
        
def main():
    # Initialize connection.
    conn = st.connection('mysql', type='sql')
    wider_page()
    set_custom_theme()
    image_file = st.file_uploader("Upload ID Card")
    if image_file is not None:
        face_image_file = st.file_uploader("Upload Face Image")
        main_content(image_file, face_image_file, conn)

if __name__ == "__main__":
    main()