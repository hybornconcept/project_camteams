from datetime import datetime
import streamlit as st  # pip install streamlit
import time
import socket
from tools.database import insert_eid
from streamlit_js_eval import get_geolocation

# --------------- PAGE SETTINGS------------
page_title = "CAM TOOL"
page_icon = ":blue_book:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

# ------------STYLING--------------------------
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
        img{height:75px;width:1500px;}
        div.row-widget.css-k008qs.epcbefy2{margin-left: 8%;}
        button.css-1q8dd3e.edgvbvh5{
        padding:2% 30%;}
        div.css-ocqkz7.e1tzin5v4 {
        border: 0.1rem solid #586E75;
        border-radius:10px;
        padding: 20px 30px;}
        div.css-zt5igj.e16nr0p32{margin-top:-10%;}
        div.css-zt5igj.e16nr0p32{margin-bottom:-35%;}
        footer.css-1lsmgbg.egzxvld0{display:None}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# ----------------------------------------------------------------Get Geolocation--------------------------
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

# ----------------------------------------------------------------REMOVE BLANK AND NONE WORD--------------------------


def is_not_a_word(word):
    """ This function checks if given string is empty
     or contain only shite spaces"""
    list = '!@#$%^&*()-+?_=,<>/'
    if (word.strip() == '' or word in list):
        return True


def progress():
    my_bar = st.progress(0)
    for p in range(100):
        time.sleep(0.1)
        my_bar.progress(p+1)
    st.success("Response Submitted Successfully")


# -------------- SETTINGS --------------
listed = ["-", "No", "Yes"]
data = {
    'Hospital_No': "",
    'facility':   "",
    'cam_teams': ["-", "Akamkpa 1", "Bakassi", "Ikom", "Akamkpa2",    "Akpabuyo", "Calabar South",
                  "Obubra", "Yakurr", "Abi-biase", "Boki", "Etung", "Calabar Municipal", "Odukpani"],
    'residence_LGA': '',
    'vaccinated': listed,
    'recency_status': ["-", "Not Done", "Recent Infection", "Long-Term Infection"],

    'delivery_location': ["-", "TBA", "Healing home", 'Unsupported site', "Supported facility",
                          "Prayer House",  "Health-Center", "Private Hospital", "Others"],
    "delivery_facility": '',
    'Last_menstrul_Period': ["-", "<1 month", "1-3 months", "4-6 months", "> 6 months"],
    'trimester': ['1st Trimester', '2nd Trimester', '3rd Trimester'],
    'marital_status': ["-", "Married", "Single", "Divorced",
                       "Widowed", "Seperated", "Cohabiting", "Others"],
    'EDD': '',
    'viral_load': ["-", "No Viral load done" "Suppressed", "Unsurppressed"],

    # 'Regimen': '',
    'delivery_outcome': ["-", "child is alive", "child died"],
    # ---
    'child_risk_level': ["-", "High", "Low"],
    'prophylaxis': listed,
    'EID_sampling': listed,
    'date_of_sampling': '',
    'address': '',
    'med_history_comements': ''
}

st.header(f"PMTCT EID Identification")

st.markdown("_This form is specifically for **HIV Positive Pregnant Client** identified both in the community and Facility_", unsafe_allow_html=True)


main_container = st.container()

# with st.form("entry_form"):
with st.form(key="entry_form", clear_on_submit=True):
    with main_container:

        col1, col2 = st.columns(2)
        # Tested Clients
        col1.text_input("Hospital_No",
                        key="Hospital_No")
        col2.text_input("Select the Supporting Site:",
                        key="facility")
        col1.selectbox("Select the CAM TEAM:",
                       data['cam_teams'], key="cam_teams")

        col2.text_input("LGA of Residence:", key="residence_LGA")
        col1.selectbox("Client Vacination:", data['vaccinated'],
                       key="vaccinated")
        col2.selectbox("HIV Recency Status:",
                       data['recency_status'], key="recency_status")
        col1.selectbox("Site booked for delivery:",
                       data['delivery_location'], key="delivery_location")
        col2.text_input("Name of the Site:",
                        key="delivery_facility")

        col1.selectbox("Last menstrul Period LMP:",
                       data['Last_menstrul_Period'], key="Last_menstrul_Period")
        col2.selectbox("Select the Trimester:",
                       data['trimester'], key="trimester")
        col1.selectbox("Client Marital Status:",
                       data['marital_status'], key="marital_status")
        col2.selectbox("Last viral load result:",
                       data['viral_load'], key="viral_load")
        col1.date_input(
            "Expected Delivery date",
            datetime.now(), key="EDD")

        # col2.text_input("Regimen of the client:",
        #                 key="Regimen"),
        col2.selectbox("Delivery outcome:",
                       data['delivery_outcome'], key="delivery_outcome")

        "---"
        placeholder = st.empty()
        if str(st.session_state["delivery_outcome"]) == "child is alive":

            with placeholder.container():
                pos1, pos2 = st.columns(2)
                pos1.selectbox("Risk level of the Child:",
                               data['child_risk_level'], key="child_risk_level")

                pos2.selectbox("Prophylaxis Given:",
                               data['prophylaxis'], key="prophylaxis")

                pos1.selectbox("DBS collected:",
                               data['EID_sampling'], key="EID_sampling")

                pos2.date_input("Date DBS was collected",
                                datetime.now(), key="date_of_sampling")

                pos1.text_area(
                    "", placeholder="Provide a Client descriptive address ...", key='address')
                history = pos2.text_area(
                    "", placeholder="Comments  or Patients medical history", key='med_history_comements')

    submitted = st.form_submit_button("Submit Response")
    if submitted:
        todays_date = datetime.today().strftime('%Y-%m-%d')

        # ----------------- Validate if Negative-----------------------------
        if str(st.session_state["delivery_outcome"]) != "child is alive":

            eid_response = {key: str(st.session_state[key]) if i < 14 else "" for i, key in enumerate(
                list(data.keys()))}
            for key in list(eid_response.keys())[:13]:
                if (is_not_a_word(str(st.session_state[key]))):
                    st.error("The input for " + key.upper() +
                             " is Incorrect or Empty")
                    st.stop()
        # ----------------- Validate if Positive-----------------------------
        else:
            eid_response = {key: str(st.session_state[key])
                            for key in list(data.keys())}
            for key in list(eid_response.keys()):
                if (is_not_a_word(str(st.session_state[key]))):
                    st.error("The input for " + key.upper() +
                             " is Incorrect or Empty")
                    st.stop()

    # -------------------Submission-----------------------
        ip = get_ip()
        timestamp = location["timestamp"]
        location2 = location['coords']
        insert_eid(str(timestamp), str(ip), location2, eid_response)
        progress()


# imgcol1, imgcol2 = st.columns(2)
# files = [file for file in glob.glob("tools\images\*")]


# img1 = files[0]
# img2 = files[1]
# with imgcol1:
#     st.image(img1)

# with imgcol2:
#     st.image(img2)
