import cv2
import os
import streamlit as st
from preprocess import read_image, extract_idcard, save_image
from ocr_engine import extract_text
from postprocess import extract_information
from face_recognition import detect_and_extract_face, face_comparison
from datetime import datetime

USE_DB = os.getenv("USE_DB", "no") == "yes"

if USE_DB:
    from mysql_operations import insert_records, fetch_data, duplicacy

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
                background-color: #f0f2f6;
                color: #333333;
            }
            .sidebar .sidebar-content {
                background-color: #ffffff;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def sidebar_section():
    st.sidebar.title("Select ID Card Type")

def main_content(image_file, fac_image_file):
    if image_file is not None:
        face_image = read_image(fac_image_file, is_uploaded=True)
        if face_image is not None:
            image = read_image(image_file, is_uploaded=True)
            image_roi, _ = extract_idcard(image)
            face_image_path2 = detect_and_extract_face(img=image_roi)
            face_image_path1 = save_image(face_image, "face_image.jpg", path="data\\02_intermediate_data")

            if face_image_path1 and face_image_path2:
                is_face_verified = face_comparison(image1_path=face_image_path1, image2_path=face_image_path2)

                if is_face_verified:
                    extracted_text = extract_text(image_roi)
                    text_info = extract_information(extracted_text)

                    if text_info is None or 'ID' not in text_info:
                        st.error("Could not extract ID")
                        return

                    # If DB usage is enabled
                    if USE_DB:
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
                                    pass
                            if not text_info['DOB'] or text_info['DOB'].strip() == "":
                                text_info['DOB'] = None
                            insert_records(text_info)
                    else:
                        st.write("DB Disabled. Parsed info:")
                        st.json(text_info)

                else:
                    st.error("Face verification failed.")
            else:
                st.error("Face image extraction failed.")
        else:
            st.error("Face image not uploaded.")
    else:
        st.warning("Please upload an ID card image.")

def main():
    wider_page()
    set_custom_theme()
    st.title("e-KYC ID Verification")
    image_file = st.file_uploader("Upload ID Card")
    if image_file is not None:
        face_image_file = st.file_uploader("Upload Face Image")
        main_content(image_file, face_image_file)

if __name__ == "__main__":
    main()
