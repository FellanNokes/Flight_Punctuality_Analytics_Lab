import base64
import streamlit as st
from pathlib import Path

def get_image_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def clickable_image(image_path, link_target):
    img_base64 = get_image_as_base64(image_path)
    html = f'''
        <a href="{link_target}" target="_self">
            <img src="data:image/png;base64,{img_base64}" style="width:100%; border-radius:10px;">
        </a>
    '''
    st.markdown(html, unsafe_allow_html=True)