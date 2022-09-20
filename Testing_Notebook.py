from datetime import datetime
import streamlit as st  # pip install streamlit
import time
import socket
from tools.database import insert_deta
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
        div.css-zt5igj.e16nr0p32{margin-bottom:-15%;}
        div.css-14xtw13.e8zbici0{display:None}
        footer.css-1lsmgbg.egzxvld0{display:None}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# ----------------------------------------------------------------Get Geolocation--------------------------
location = get_geolocation('Get location')

# ----------------------------------------------------------------Get IP--------------------------


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
    'cam_teams': ["-", "Akamkpa 1", "Bakassi", "Ikom", "Akamkpa2",    "Akpabuyo", "Calabar South",
                  "Obubra", "Yakurr", "Abi-biase", "Boki", "Etung", "Calabar Municipal", "Odukpani"],
    'type_of_structural_driver': ["-", "TBA", "Healing home", "Traditional Bone-Setter", "Plantation", "Settlement",
                                  "Prayer House", "PMV", "Health-Center", "Private Hospital", "Pharmacy", "Laboratory", "Others"],
    'date_of_birth': '',
    'testing_modality': ["-", "Social Network Testing", "Sexual Network Testing", "Geneology Testing", "Self-Testing (HIVST)",
                         "Targetted Testing", "Voluntary Counselling Testing (VCT)", "PMTCT Testing"],
    'sex': ["-", "Male", "Female"],
    'risk_level': ["-", "High", "Low"],

    'elicited': "",
    'test_result': ["-", "Negative", "Positive"],

    # ---
    'client_code': '',
    'phone': '',


    'residence_LGA': '',
    'last_test': ["-", "<1 month", "1-3 months", "4-6 months", "> 6 months"],
    'occupation': '',
    'education_level': ["-", "Not Educated", "Primary",
                        "Secondary", "Tertiary", "Post-Graduate"],
    'marital_status': ["-", "Married", "Single", "Divorced",
                       "Widowed", "Seperated", "Cohabiting", "Others"],
    'vaccinated': listed,
    'linked': listed,
    'income_level': ['less than #30,000', 'btw #30,000- #100,000', 'btw #100,000- #500,000', '#500,000 and above'],
    'No_of_child_enumerated': '',
    'recency_status': ["-", "Not Done", "Recent Infection", "Long-Term Infection"],
    'address': '',
    'med_history_comements': '',
}

st.header(f"Case Identification")
st.markdown("_This form is to be correctly filled for each **Person Tested Positive or Negative** by your Cam Team_", unsafe_allow_html=True)

main_container = st.container()

# with st.form("entry_form"):
with st.form(key="entry_form", clear_on_submit=True):
    with main_container:
        col1, col2 = st.columns(2)
        # Tested Clients
        col1.selectbox("Select the CAM Team:",
                       data['cam_teams'], key="cam_teams")
        col2.selectbox("Select Type of Structural Driver:",
                       data['type_of_structural_driver'], key="type_of_structural_driver")
        col1.date_input(
            "Select date of birth",
            datetime.now(), key="date_of_birth", min_value=datetime.date(1930, 1, 1), max_value=datetime.now())

        col2.selectbox("Select Testing Modality:",
                       data['testing_modality'], key="testing_modality")
        col1.selectbox("Select the Sex:", data['sex'], key="sex")
        col2.selectbox("Select Risk Level of Client:",
                       data['risk_level'], key="risk_level")

        col1.number_input("No.of Social Networks/ Partners Elicited", value=0, step=1, min_value=0,
                          key='elicited')
# social networks offered yes/no
# social networks offered numbers

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
                pos1.text_input("LGA of Residence",
                                key="residence_LGA", placeholder="e.g. Abi")
                pos2.selectbox("Last HIV Negative Result:",
                               data['last_test'], key="last_test")
                pos1.text_input("Client's Occupation",
                                key='occupation', placeholder="e.g Fisherman")
                pos2.selectbox("Client's Education Level:",
                               data['education_level'], key="education_level")
                pos1.selectbox("Client's Marital Status:",
                               data["marital_status"], key="marital_status")
                pos2.selectbox(
                    "Income Level", data['income_level'], key="income_level")

                pos1.selectbox("Was Client Linked to Care ?",
                               data['linked'], key="linked")
                pos2.selectbox("Is the Client Vacinnated for Covid-19 ?",
                               data['vaccinated'], key="vaccinated")

                pos1.number_input("No. of Children Enumerated", value=0, step=1, min_value=0,
                                  key='No_of_child_enumerated')

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

            result = {key: str(st.session_state[key]) if i < 8 else "" for i, key in enumerate(
                list(data.keys()))}
            for key in list(result.keys())[:8]:
                if (is_not_a_word(str(st.session_state[key])) or str(st.session_state[key]) == todays_date):
                    st.error("The input for " + key.upper() +
                             " is Incorrect or Empty")
                    st.stop()
        # ----------------- Validate if Positive-----------------------------
        else:
            result = {key: str(st.session_state[key])
                      for key in list(data.keys())}
            for key in list(result.keys()):
                if (is_not_a_word(str(st.session_state[key])) or str(st.session_state[key]) == todays_date):
                    st.error("The input for " + key.upper() +
                             " is Incorrect or Empty")
                    st.stop()

        # -------------------Submission-----------------------
        ip = get_ip()
        timestamp = location["timestamp"]
        location2 = location['coords']
        insert_deta(str(timestamp), str(ip), location2, result)
        progress()

# imgcol1, imgcol2 = st.columns(2)
# files = [file for file in glob.glob("tools\images\*")]


# img1 = files[0]
# img2 = files[1]
# with imgcol1:
#     st.image(img1)

# with imgcol2:
#     st.image(img2)
