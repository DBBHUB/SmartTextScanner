import streamlit as st
import pytesseract
import cv2
import os
import zipfile
import tempfile
from fuzzywuzzy import fuzz
import numpy as np

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()
# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.title("📂 Auto-Scan Local Folder")

# Upload a Zip file
# uploaded_zip = st.file_uploader("Upload a Zip file of images", type="zip")

# Enter folder path manually
folder_path = st.text_input("Enter the folder path where your images are stored")

# Enter the word to search
search_word = st.text_input("Enter the word to search")

# Fuzzy match threshold
threshold = st.slider("Fuzzy Match Threshold (%)", 70, 100, 85)

# Supported image formats
supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

# Search Button
if st.button("Search"):
    if not search_word:
        st.error("Please enter a word to search!")
    else:

        # This will track if any match found
        found_any = False

        def search_images(base_folder):
            found = False
            for root, dirs, files in os.walk(base_folder):
                for file in files:
                    if file.lower().endswith(supported_formats):
                        img_path = os.path.join(root, file)
                        img = cv2.imread(img_path)

                        if img is None:
                            continue

                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        text = pytesseract.image_to_string(gray)

                        if fuzz.partial_ratio(search_word.lower(), text.lower()) >= threshold:
                            st.success(f"✅ Found in: {img_path}")
                            st.image(img, caption=file, use_column_width=True)
                            found = True
            return found

        # if uploaded_zip is not None:
        #     with tempfile.TemporaryDirectory() as tmpdir:
        #         with zipfile.ZipFile(uploaded_zip, "r") as zip_ref:
        #             zip_ref.extractall(tmpdir)

        #         st.success(f"Extracted images from zip file!")
        #         found_any = search_images(tmpdir)

        if folder_path and os.path.exists(folder_path):
            st.success(f"Scanning images from folder: {folder_path}")
            found_any = search_images(folder_path)

        else:
            st.error("Please provide a valid folder path or upload a zip file.")

        if not found_any:
            st.error(f"No image found containing '{search_word}'.")
