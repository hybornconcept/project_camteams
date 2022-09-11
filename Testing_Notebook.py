
import geocoder
from datetime import datetime
import streamlit as st  # pip install streamlit
import time
from PIL import Image
import glob
import json
from tools.database import insert_deta


# --------------- PAGE SETTINGS------------
page_title = "CAM TOOL"
page_icon = ":blue_book:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"


def get_location():
    loc = []
    location = geocoder.ip('me')
    loc.append(location.latlng[0])
    loc.append(location.latlng[1])
    return loc


def progress():
    my_bar = st.progress(0)
    for p in range(100):
        time.sleep(0.1)
        my_bar.progress(p+1)
    st.success("Response Submitted Successfully")


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
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# -------------- SETTINGS --------------
listed = ["---", "No", "Yes"]
data = {
    'cam_teams': ["---", "Akamkpa 1", "Akpabuyo 1", "Bakassi", "Ikom-Etung", "Akamkpa 2", "Akpabuyo 2", "Calabar South",
                  "Obubra", "Yakurr", "Abi-biase", "Boki", "Calabar Municipal 1", "Calabar Municipal 2", "Odukpani 1", "Odukpani 2"],
    'structural_driver': ["---", "TBA", "Healing home", "Traditional Bone-Setter", "Plantation", "Settlement",
                          "Prayer House", "PMV", "Health-Center", "Private Hospital", "Pharmacy", "Laboratory", "Others"],
    'DOB': '',
    'testing_modality': ["---", "Social Network Testing", "Sexual Network Testing", "Geneology Testing", "Self-Testing (HIVST)",
                         "Targetted Testing", "Voluntary Counselling Testing (VCT)", "PMTCT Testing"],
    'sex': ["---", "Male", "Female"],
    'risk_level': ["---", "High", "Low"],
    'PrEP': listed,
    'accepted_ict': listed,
    'elicited': "",
    'test_result': ["---", "Negative", "Positive"],

    # ---------
    'client_code': '',
    'phone': '',
    'last_test': ["---", "<1 month", "1-3 months", "4-6 months", "> 6 months"],
    'residence_State': '',
    'education_level': ["---", "Not Educated", "Primary",
                        "Secondary", "Tertiary", "Post-Graduate"],
    'marital_status': ["---", "Married", "Single", "Divorced",
                       "Widowed", "Seperated", "Cohabiting", "Others"],
    'linked': listed,

    'recency_test': listed,
    'vaccinated': listed,
    'recency_status': ["---", "Recent Infection", "Long-Term Infection"],
    'income_level': ['less than #30,000', 'btw #30,000- #100,000', 'btw #100,000- #500,000', '#500,000 and above'],
    'residence_LGA': '',
    'occupation': '',
    'No_of_child_enumerated': '',
    'address': '',
    'med_history_comements': '',
}

st.header(f"Case Identification")

main_container = st.container()

# with st.form("entry_form"):
with st.form(key="entry_form", clear_on_submit=True):
    with main_container:
        col1, col2 = st.columns(2)
        # Tested Clients
        col1.selectbox("Select the CAM Team:",
                       data['cam_teams'], key="cam_teams")
        col2.selectbox("Select Type of Structural Driver:",
                       data['structural_driver'], key="structural_driver")
        col1.date_input(
            "Select date of birth",
            datetime.now(), key="DOB")

        col2.selectbox("Select Testing Modality:",
                       data['testing_modality'], key="testing_modality")
        col1.selectbox("Select the Sex:", data['sex'], key="sex")
        col2.selectbox("Select Risk Level of Client:",
                       data['risk_level'], key="risk_level")
        col1.selectbox("Is Client on PrEP ?:",
                       data['PrEP'], key="PrEP")
        col2.selectbox("Accepted Index Testing ?",
                       data['accepted_ict'], key="accepted_ict")
        col1.number_input("No.of Partners Elicited", value=-1, step=1, min_value=-1, max_value=30,
                          key='elicited')

        col2.selectbox("Select Test result:",
                       data['test_result'], key="test_result")

        "---"
        placeholder = st.empty()
        if str(st.session_state["test_result"]) == "Positive":

            with placeholder.container():
                pos1, pos2 = st.columns(2)
                pos1.text_input("Client code", key="client_code")
                pos2.text_input("Client's Phone Number",
                                key="phone", placeholder="e.g. 080xxxxxxxx")
                pos1.text_input(
                    "State of Residence", key="residence_State", placeholder="e.g. Cross river")
                pos2.text_input("LGA of Residence",
                                key="residence_LGA", placeholder="e.g. Abi")
                pos1.selectbox("Last HIV Negative Result:",
                               data['last_test'], key="last_test")
                pos2.text_input("Client's Occupation",
                                key='occupation', placeholder="e.g Fisherman")
                pos1.selectbox("Client's Education Level:",
                               data['education_level'], key="education_level")
                pos2.selectbox("Client's Marital Status:",
                               data["marital_status"], key="marital_status")
                pos1.selectbox("Is the Client Vacinnated for Covid-19 ?",
                               data['vaccinated'], key="vaccinated")
                pos2.selectbox("Was Client Linked to Care ?",
                               data['linked'], key="linked")
                pos1.selectbox(
                    "Income Level", data['income_level'], key="income_level")

                pos2.number_input("No. of Children Enumerated", value=-1, step=1, min_value=-1, max_value=30,
                                  key='No_of_child_enumerated')

                pos1.selectbox("Recency Testing done?",
                               data['recency_test'], key="recency_test")
                pos2.selectbox("Recency Testing result",
                               data['recency_status'], key="recency_status")
                pos1.text_area(
                    "", placeholder="Provide a Client descriptive address ...", key='address')
                history = pos2.text_area(
                    "", placeholder="Comments  or Patients medical history", key='med_history_comements')

    submitted = st.form_submit_button("Submit Response")
    if submitted:
        todays_date = datetime.today().strftime('%Y-%m-%d')

        # ----------------- Validate if Negative-----------------------------
        if str(st.session_state["test_result"]) != "Positive":

            result = {key: str(st.session_state[key]) if i < 10 else "" for i, key in enumerate(
                list(data.keys()))}
            for key in list(result.keys())[:10]:
                if (st.session_state[key] == '---' or str(st.session_state[key]) == todays_date or str(st.session_state[key]) in ['-1', '-0', '-']):
                    st.error("The input for " + key.upper() +
                             " is Incorrect or Empty")
                    st.stop()
        # ----------------- Validate if Positive-----------------------------
        else:
            result = {key: str(st.session_state[key])
                      for key in list(data.keys())}
            for key in list(result.keys())[:24]:
                if (bool(st.session_state[key]) == False or st.session_state[key] == '---' or str(st.session_state[key]) == todays_date or str(st.session_state[key]) in ['-1', '-0', '-']):
                    st.error("The input for " + key.upper() +
                             " is Incorrect or Empty")
                    st.stop()
        # -----------------Submit everything--------------------------
        location = json.dumps(get_location())
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        insert_deta(timestampStr, location, result)
        progress()


# # -----------Logo------------------
# img1, img2 = st.columns(2)

# # image1 = Image.open('ecews.jpg')

# files = [file for file in glob.glob("tools\images\*")]

# image1 = files[0]
# image2 = files[1]
# img1.image(image1)
# img2.image(image2)
