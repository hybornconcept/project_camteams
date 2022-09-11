from datetime import datetime
import streamlit as st  # pip install streamlit
import geocoder
import datetime
import re
import time
from tools.database import insert_driver
import glob
from PIL import Image

page_title = "CAM TOOL"
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
page_icon = ":information_source:"
layout = "centered"
# --------------------------------------


st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)


# -----styling---------
hide_st_style = """
            <style>
            img{height:75px;width:1500px;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --------------- Location------------


def get_location():
    loc = []
    location = geocoder.ip('me')
    loc.append(location.latlng[0])
    loc.append(location.latlng[1])
    return loc
# -----progress bar-------------------


def progress():
    my_bar = st.progress(0)
    for p in range(100):
        time.sleep(0.02)
        my_bar.progress(p+1)
    st.success("Response Submitted Successfully")


# -------------- SETTINGS --------------
collections = {
    'cam_teams': ["-", "Akamkpa 1", "Akpabuyo 1", "Bakassi", "Ikom-Etung", "Akamkpa 2", "Akpabuyo 2", "Calabar South",
                  "Obubra", "Yakurr", "Abi-biase", "Boki", "Calabar Municipal 1", "Calabar Municipal 2", "Odukpani 1", "Odukpani 2"],
    'structural_driver': ["-", "TBA", "Healing home", "Traditional Bone-Setter", "Plantation", "Settlement",
                          "Prayer House", "PMV", "Health-Center", "Private Hospital", "Pharmacy", "Laboratory", "Others"],
    'longitude': '',
    'latitude': '',
    'focal_person': '',
    'address': '',


}


def is_empty_or_blank(msg):
    """ This function checks if given string is empty
     or contain only shite spaces"""
    return re.search("^\s*$", msg)


st.header(f"Structural Drivers Notebook")
with st.form("entry_form"):
    col1, col2 = st.columns(2)
    col1.selectbox("Select the CAM Team:",
                   collections['cam_teams'], key="cam_teams")
    col2.selectbox("Select Type of Structural Driver:",
                   collections['structural_driver'], key="structural_driver")

    col1.number_input("Enter the Longitude:", key="longitude",
                      value=0.001, step=0.001)
    col2.number_input("Enter the Latitude:", key="latitude",
                      value=0.001, step=0.001)
    focal_person = st.text_input(
        "Full name of focal person", key="focal_person", placeholder="John Doe")
    address = st.text_area(
        "", placeholder="Please provide a descriptive address ...", key="address")

    submitted = st.form_submit_button("Submit Response")

    if submitted:
        hotspots = {key: st.session_state[key]
                    for key in list(collections.keys())}

        for key, value in hotspots.items():
            if (bool(value) == False or len(str(value)) <= 1 or str(value)[0] == '0'):
                st.error("The input for " + key.upper() +
                         " is Incorrect or Empty")
                st.stop()

        timestamp = str(datetime.datetime.now())
        location = get_location()
        insert_driver(timestamp, location, hotspots)
        progress()

# -----------Logo------------------
img1, img2 = st.columns(2)


# image1 = glob.glob("tools\ecews.jpg")
# image2 = glob.glob("tools\usaid_2.jpg")
image1 = Image.open(
    'https://drive.google.com/file/d/111jLG4GVoPOTZbs8iWektwthOHqUTrgm/view?usp=sharing')
image2 = Image.open(
    'https://drive.google.com/file/d/1ywGGxKAlqgIEfMyIoENQtBrE7WIWavTe/view?usp=sharing')

# files = [file for file in glob.glob("tools\images\*")]

# image1 = files[0]
# image2 = files[1]
img1.image(image1)
img2.image(image2)
