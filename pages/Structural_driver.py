import streamlit as st  # pip install streamlit
# import glob
from streamlit_js_eval import get_geolocation
import time
import socket
from tools.database import insert_driver


page_title = "CAM TOOL"
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
page_icon = ":information_source:"
layout = "centered"
# --------------------------------------


st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.markdown("""<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
 integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">""", unsafe_allow_html=True)

# -----styling---------
hide_st_style = """
            <style>

            img{height:75px;width:1500px;}
            img{height:75px;width:1500px;}
        div.row-widget.css-k008qs.epcbefy2{margin-left: 8%;}
        button.css-1q8dd3e.edgvbvh5{
        padding:2% 30%;}
        div.css-ocqkz7.e1tzin5v4 {
        border: 0.1rem solid #586E75;
        border-radius:10px;
        padding: 20px 30px;}
        div.css-zt5igj.e16nr0p32{margin-top:-10%;}
        div.css-zt5igj.e16nr0p32{margin-bottom:-17%;}
        div.css-14xtw13.e8zbici0{display:None}
        footer.css-1lsmgbg.egzxvld0{display:None}
            </style>

            """
st.markdown(hide_st_style, unsafe_allow_html=True)


def progress():
    my_bar = st.progress(0)
    for p in range(100):
        time.sleep(0.02)
        my_bar.progress(p+1)
    st.success("Response Submitted Successfully")


# -------------- SETTINGS --------------
listed = ["-", "No", "Yes"]
collections = {
    'cam_teams': ["-", "Akamkpa 1", "Bakassi", "Ikom", "Akamkpa 2",    "Akpabuyo", "Calabar South", "Calabar Municipal 1", "Calabar Municipal 2",
                  "Obubra", "Yakurr", "Abi", "biase", "Boki", "Etung",  "Odukpani"],
    'type_of_structural_driver': ["-", "TBA", "Healing home", "Traditional Bone-Setter", "Plantation", "Settlement",
                                  "Prayer House", "PMV", "Health-Center", "Private Hospital", "Pharmacy", "Laboratory", "Others"],
    'name_of_structural_driver': '',
    'residence_area': ['-', 'Urban', 'Semi-Urban', 'Rural'],
    'client_load': '',
    'key_person': '',
    'skill_level': ['-', 'Trained Healthcare Worker', 'Non-Healthcare Worker'],

    'client_referals': listed,
    'phone_number': '',
    'entry': ['-', 'Retrospective', 'Current'],
    'address': '',
    'longitude': '',
    'latitude': ''
}


location = get_geolocation('Get location')


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def is_not_a_word(word):
    """ This function checks if given string is empty
     or contain only shite spaces"""
    list = '!@#$%^&*()-+?_=,<>/'
    if (word.strip() == '' or word in list):
        return True


st.header(f"Structural Drivers Notebook")


st.markdown("_This form is to be correctly filled for each **Structural driver** identified in the Community by your CAM Team_", unsafe_allow_html=True)
main_container = st.container()

with st.form(key="entry_form", clear_on_submit=True):
    with main_container:

        col1, col2 = st.columns(2)
        col1.selectbox("Select your CAM Team:",
                       collections['cam_teams'], key="cam_teams")
        col2.selectbox("Type of Structural Driver:",
                       collections['type_of_structural_driver'], key="type_of_structural_driver")

        col1.text_input("Name of Structural Driver",
                        key="name_of_structural_driver")
        col2.selectbox("Residence Area:",
                       collections['residence_area'], key="residence_area")
        col1.number_input("Monthly average Client load", step=1,
                          min_value=0, key="client_load")

        col2.text_input(
            "Full name of Owner/Key person", key="key_person", placeholder="John Doe")
        col1.selectbox("Skill Level of Owner/Key person:",
                       collections['skill_level'], key="skill_level")
        col2.selectbox("Are Clients referred to health Institutions?",
                       collections['client_referals'], key="client_referals")
        col1.text_input(
            "Phone No. of focal person", key="phone_number", placeholder="080xxxxxxxx")

        col2.selectbox("Type of entry", collections['entry'], key="entry")
        st.text_area(
            "", placeholder="Descriptive address of the structural Driver ...", key="address")

        placeholder = st.empty()
        if str(st.session_state["entry"]) == "Retrospective":
            with placeholder.container():
                pos1, pos2 = st.columns(2)
                pos1.number_input("GPS coordinate, Longitude:",
                                  key="longitude", value=0.000)
                pos2.number_input("GPS coordinate, Lattitude:", key="latitude",
                                  value=0.000)

    submitted = st.form_submit_button("Submit Response")

    if submitted:
        # ----------------- Validatation-----------------------------
        if str(st.session_state["entry"]) != "Retrospective":
            hotspots = {key: str(st.session_state[key]) if i < 11 else "" for i, key in enumerate(
                list(collections.keys()))}

            for key in list(collections.keys())[:11]:

                if (is_not_a_word(str(st.session_state[key]))):
                    st.error("The input for " + key.upper() +
                             " is Incorrect or Empty")
                    st.stop()
                if key == "phone_number":
                    if (len(str(st.session_state[key])) != 11 or not(st.session_state[key].isdigit())):
                        st.error("The input for " + key.upper() +
                                 " is Incorrect or Empty")
                        st.stop()
                if key == "client_load":
                    if (len(str(st.session_state[key])) < 2 and int(st.session_state[key] == 0)):
                        st.error("The input for " + key.upper() +
                                 " is Incorrect or Empty")
                        st.stop()
        if str(st.session_state["entry"]) == "Retrospective":
            if (int(st.session_state["longitude"]) == 0 or int(st.session_state["latitude"]) == 0):
                st.error("The input for Latitude/Longitude is Incorrect or Empty")
                st.stop()
            else:
                hotspots = {key: str(st.session_state[key])
                            for key in list(collections.keys())}
    # -------------------Submission-----------------------
        ip = get_ip()
        timestamp = location["timestamp"]
        location2 = location['coords']
        insert_driver(str(timestamp), str(ip), location2, hotspots)
        progress()

# imgcol1, imgcol2 = st.columns(2)
# files = [file for file in glob.glob("tools\images\*")]


# img1 = files[0]
# img2 = files[1]
# with imgcol1:
#     st.image(img1)

# with imgcol2:
#     st.image(img2)
