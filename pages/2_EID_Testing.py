
import streamlit as st  # pip install streamlit
import time
# from datetime import date
# from datetime import datetime
import socket
from datetime import datetime
# import itertools
from streamlit_option_menu import option_menu
from tools.database import insert_eid
from tools.database import insert_post_natal
from tools.database import get_period
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
        div.row-widget.css-k008qs.epcbefy2{margin-left: 12%;}
        button.css-1q8dd3e.edgvbvh5{
        padding:2% 30%;}
        div.css-ocqkz7.e1tzin5v4 {
        border-radius:10px;
        padding: 20px 30px;}
        footer.css-1lsmgbg.egzxvld0{display:None}
        
            div.css-ocqkz7.e1tzin5v4 {
            border: 0.1rem solid #586E75;
            border-radius:10px;
            padding: 20px 30px;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# div.css-zt5igj.e16nr0p32{margin-top:-10%;}
# div.css-zt5igj.e16nr0p32{margin-bottom:-35%;}
# border: 0.1rem solid #586E75;
# ------------------------------------------List of facilities----------------------------------------------
facilities = ['-', 'cr Akamkpa General Hospital', 'cr Akani Esuk Health Centre', 'cr Akpabuyo St Joseph Hospital', 'cr Akpet Central Cottage Hospital', 'cr Anantigha Primary Health Centre', 'cr Anderson Primary Health Centre', 'cr Aningeje Primary Health Centre', 'cr Aya Medical Centre', 'cr Bakor Medical centre', 'cr Calabar General Hospital', 'cr Calabar South Family Health Centre', 'cr Calabar Women and Children Hospital', 'cr Country Specialist Hospital', 'cr Cross River University of Science and Technology (CRUTECH) Medical Centre', 'cr Dr Lawrence Henshaw Memorial Hospital', 'cr Ekana Medical Centre', 'cr Ekorinim Health Centre', 'cr Ekpo Abasi Primary Health Centre', 'cr Ekpri Obutong Health Centre', 'cr Emmanuel Infirmiry', 'cr Essierebom Primary Health Centre', 'cr Faith Foundation Clinic', 'cr Goldie Clinic', 'cr Henshaw Town Health Post', 'cr Hiltop Healthcare Foundation', 'cr Holy Family Catholic Hospital',
              'cr Ikang Primary Health Centre', 'cr Ikot Edem Odo Health Centre', 'cr Ikot Effiong Otop Comprehensive Health Centre (UCTH Annex)', 'cr Ikot Ekpo Health Post (Ward 10)', 'cr Ikot Enebong Health Post', 'cr Ishie Health Post', 'cr Kasuk Health Centre', 'cr Mambo Clinic', 'cr Melrose Hospital', 'cr Mfamosing Primary Health Center', 'cr Mma Efa Health Centre', 'cr Mount Zion Medical Centre', 'cr Nyahasang Health Centre', 'cr Oban Health Centre', 'cr Obubra General Hospital', 'cr Obubra Maternal and Child Health Clinic', 'cr Peace medical centre', 'cr Police Hospital', 'cr Ugep General Hospital', 'cr Ukpem General Hospital', 'cr University of Calabar Medical Centre', 'cr University of Calabar Teaching Hospital', 'cr Diamond Hill Health Centre', 'cr Okundi Comprehensive Health Centre', 'cr Katchuan Irruan Model Primary Health Centre', 'cr Eja Memorial Hospital', 'cr Igbo-Imabana Model Primary Health Centre']
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
    if (word is None or word in list):
        return True


def progress():
    my_bar = st.progress(0)
    for p in range(100):
        time.sleep(0.002)
        my_bar.progress(p+1)
    st.success("Response Submitted Successfully")


# -------------- SETTINGS --------------
gravida = [str(i) for i in list(range(0, 9, 1))]
gravida.insert(0, "-")
listed = ["-", "No", "Yes"]
data = {
    'hospital_No': "",
    'facility': facilities,
    'enrollmenent_setting': ["-", "Community", "Facility"],
    'client_category': ["-", "Facility Based Client", "TBA", "Healing home", "Prayer House", "PMV", "Unsupported Health-Center", "Private Hospital", "Pharmacy", "Laboratory", "Others"],
    'residence_LGA': '',
    'cervical_screening': listed,
    'recency_status': ["-", "Not Done", "Recent Infection", "Long-Term Infection"],
    'Last_menstrul_Period': '',
    'marital_status': ["-", "Married", "Single", "Divorced",
                       "Widowed", "Seperated", "Cohabiting", "Others"],
    'mamapack': '',
    'partner_HIV_status': ["-", "I dont Know", "HIV Positive", "HIV Negative"],
    'viral_load_collection': ["-", "Not Yet Eligible", "Eligible But Sample Not Collected", "Before 32 Weeks", "32 Weeks", "33 Weeks",  "34 Weeks", "35 Weeks", "36 Weeks", "After 36 Weeks"],
    'viral_load_Status': ["-", "Undetectable", "Suppressed", "Unsuppressed", "No VL result Yet"],
    'no_of_pregnancies': gravida,
    'address': '',
    'client_concerns': '',
    # Child
    'delivery_location': ["-", "TBA", "Supported Site", "Unsupported Health-Center", "Private Hospital", "Delivered at home", "Prayer House", "Unknown"],
    'name_of_delivery_site': "",
    'delivery_method': ["-", "Normal Birth", "Ceasearian Section"],

    'delivery_date': '',
    'child_risk_level': ["-", "High", "Low"],
    'prophylaxis': ['-', 'Not Given', 'Nevirapine only', 'Nevirapine + Zidovudine'],
    'birth_weight': ['-', 'below 2.6 Kg', '2.6 Kg and above'],
    'dbs_sample_collected': listed,
    'sample_collection_date': '',
    'result_recieved_date': '',

    'comments': ''
}

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Pre-Natal Data", "Post-Natal Data"],
    icons=["cursor", "pen"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)
if selected == "Pre-Natal Data":
    st.header(f"PMTCT EID (Pre-Natal Data Collection)")

    st.markdown("_This form is specifically for **HIV Positive Pregnant Client** identified both in the community and Facility_", unsafe_allow_html=True)

    with st.form(key="entry_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        # Tested Clients
        col1.text_input("Client's Hospital_No",
                        key="hospital_No")
        col2.selectbox("Select the Facility",
                       data['facility'], key='facility')
        col1.selectbox("Enrollment Setting",
                       data['enrollmenent_setting'], key='enrollmenent_setting')
        col2.selectbox("Client Categorization",
                       data['client_category'], key='client_category')
        col2.text_input("LGA of Residence:", key="residence_LGA")
        col1.selectbox("Screened for Cervical Cancer:", data['cervical_screening'],
                       key="cervical_screening")
        col2.selectbox("HIV Recency Status:",
                       data['recency_status'], key="recency_status")

        col1.date_input("The first Day of your Last Menstrual Period (LMP):",
                        datetime.now(), key="Last_menstrul_Period")

        col1.selectbox("Marital Status:",
                       data['marital_status'], key="marital_status")
        col2.selectbox("Was MaMaPack provided ?",
                       listed, key="mamapack")
        col1.selectbox("HIV Status of your Partner?:",
                       data['partner_HIV_status'], key="partner_HIV_status")

        col2.selectbox("Viral Load Sample was collect at?:",
                       data['viral_load_collection'], key="viral_load_collection")
        col1.selectbox("Viral Load Status:",
                       data['viral_load_Status'], key="viral_load_Status")
        col2.selectbox("No of Pregnacies so far:",
                       data['no_of_pregnancies'], key="no_of_pregnancies")
        col1.text_area(
            "", placeholder="Provide a Client descriptive address ...", key='address')

        col2.text_area(
            "", placeholder="Client concerns or comments  ...", key='client_concerns')

        submitted = st.form_submit_button("Submit Response")

        if submitted:
            # todays_date = datetime.today().strftime('%Y-%m-%d')
            eid_response = {
                key: str(st.session_state[key]) for key in list(data.keys())[:16]}
            for key in list(eid_response.keys()):
                if (is_not_a_word(str(st.session_state[key]))):
                    st.error("The input for " + key.upper() +
                             " is Incorrect or Empty")
                    st.stop()
                if (key in ('Last_menstrul_Period')) and (int((datetime.now().date()-datetime.strptime(str(st.session_state[key]), '%Y-%m-%d').date()).days) < 30):
                    st.error(
                        "LMP cannot be less than 30 days for a pregnant woman ")
                    st.stop()
                if (key in ('client_concerns', 'address')) and (len(st.session_state[key]) < 10):
                    st.error("Please provide more details for  " + key.upper())
                    st.stop()
            ip = get_ip()
            timestamp = location["timestamp"]
            location2 = location['coords']
            # identity = dict(list(eid_response.items())[:2])
            patient_id = eid_response['facility'] + \
                str(eid_response['hospital_No']).lower()
            a_dict = {key: eid_response[key] for key in eid_response if key not in (
                'facility', 'hospital_No')}
            insert_eid(patient_id, str(timestamp),
                       str(ip), location2, a_dict)
            progress()


# --- Post-Natal Sections ---
headerSection = st.container()
generateSection = st.container()
childsection = st.container()
# --- Post-Natal Sections ---

keydata = ''


def show_generate():
    with generateSection:
        with st.form(key="data_generate"):
            gen1, gen2 = st.columns(2)
            # Tested Clients
            mother_Hospital_No = gen1.text_input("Mother's Hospital_No",
                                                 key="mother_Hospital_No")
            facility_name = gen2.selectbox("Select the Facility",
                                           data['facility'], key='facility2')
            generate = st.form_submit_button("Get Child Section")

            if generate:
                keydata = facility_name + str(mother_Hospital_No).lower()
                database_output = get_period(keydata)
                if database_output is None:
                    st.session_state['child_show'] = False
                    st.error(
                        f"There is no client with that Hospital_No  in {facility_name} in the database ensure the correct Hospital No and Facility Name for the Client")

                else:
                    st.session_state['child_show'] = True


def show_childpage():

    with childsection:
        main_container = st.container()
        with st.form(key="post_natal", clear_on_submit=False):
            with main_container:
                child1, child2 = st.columns(2)

                child1.selectbox("Select the Delivery Location:",
                                 data['delivery_location'], key="delivery_location")
                child2.text_input("State the full name of the delivery Facility/TBA :",
                                  key="name_of_delivery_site")
                child1.date_input("Date of the Deivery:",
                                  datetime.now(), key="delivery_date")
                child2.selectbox("Delivery Method:",
                                 data['delivery_method'], key="delivery_method")

                child1.selectbox("Risk level of the Child:",
                                 data['child_risk_level'], key="child_risk_level")

                child2.selectbox("Prophylaxis Given:",
                                 data['prophylaxis'], key="prophylaxis")

                child1.selectbox("Birth Weight",
                                 data['birth_weight'], key="birth_weight")
                child2.selectbox("DBS Sample collected:",
                                 data['dbs_sample_collected'], key="dbs_sample_collected")

                placeholder = st.empty()
                if str(st.session_state["dbs_sample_collected"]) == "Yes":
                    with placeholder.container():
                        pos1, pos2 = st.columns(2)
                        pos1.date_input("Date DBS sample was collected",
                                        datetime.now(), key="sample_collection_date")

                        pos2.date_input("Date DBS result recieved",
                                        datetime.now(), key="result_recieved_date")
                st.text_area(
                    "", placeholder="Any comments or birth complications ...", key='comments')
            # Every form must have a submit button.
            submitted2 = st.form_submit_button(label="Submit Data")
            if submitted2:

                for key in list(list(data.keys())[16:]):

                    if (is_not_a_word(str(st.session_state[key]))):
                        st.error("The input for " + key.upper() +
                                 " is Incorrect or Empty")
                        st.stop()

                    if str(st.session_state["dbs_sample_collected"]) == "No":
                        st.session_state["sample_collection_date"] = "None"
                        st.session_state["result_recieved_date"] = "None"
                    else:

                        if ((key in ('delivery_date', 'sample_collection_date', 'result_recieved_date')) and (datetime.strptime(str(st.session_state[key]), "%Y-%m-%d").date() > datetime.now().date())):
                            st.error("The input for " + key.upper() +
                                     " Cannot be greater than today")
                            st.stop()
                        if (key == "sample_collection_date") and (datetime.strptime(str(st.session_state[key]), "%Y-%m-%d").date() > datetime.strptime(str(st.session_state['result_recieved_date']), "%Y-%m-%d").date()):
                            st.error("The input for " + key.upper() +
                                     " is Incorrect or Empty")
                            st.stop()
                        if (key in ('sample_collection_date', 'result_recieved_date')) and (datetime.strptime(str(st.session_state[key]), "%Y-%m-%d").date() < datetime.strptime(str(st.session_state['delivery_date']), "%Y-%m-%d").date()):
                            st.error("The input for " + key.upper() +
                                     " is Incorrect or Empty")
                            st.stop()

                    # Evaluate and pass to database
                post_natal = {
                    key: str(st.session_state[key]) for key in list(data.keys())[16:]}
                keydata = st.session_state['facility2'] + \
                    st.session_state['mother_Hospital_No']
                ip = get_ip()
                timestamp = location["timestamp"]
                location2 = location['coords']
                insert_post_natal(str(timestamp), keydata,
                                  str(ip), location2, post_natal)

                progress()


if selected == "Post-Natal Data":

    with headerSection:
        st.header(f"PMTCT EID - Delivery Outcome")
        st.markdown(
            "_Please fill the  form **Only Live Births** of Positive Women identified both in the community and Facility_", unsafe_allow_html=True)
        show_generate()
        if 'child_show' not in st.session_state:
            st.session_state['child_show'] = False

        else:
            if st.session_state['child_show']:
                show_childpage()

            # -------------------- ------- DQelivery  outcome-------------------------------------------
