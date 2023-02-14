import datetime
import streamlit as st  # pip install streamlit
import time
import socket
from tools.database import insert_partner
from streamlit_js_eval import get_geolocation



# --------------- PAGE SETTINGS------------
page_title = "CAM TOOL"
page_icon = ":blue_book:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

if 'button1' not in st.session_state:
    st.session_state.button1 = False
if 'button2' not in st.session_state:
    st.session_state.button2 = False
# ------------STYLING--------------------------
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
        img{height:75px;width:1500px;}
        div.row-widget.css-k008qs.epcbefy2{margin-left: 8%;}
        div.css-zt5igj.e16nr0p32{
            margin-top: 4%;
        }
          
        button.css-1w1p63c.edgvbvh5{
        padding:10px 15%;
        background-color:#58868D;
        margin-left:20%;

        }
       
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

year = int(datetime.date.today().strftime("%Y"))-13
listyear = [str(i) for i in list(range(1940, year))]
listyear.append("-")

list_elicit = [str(i) for i in list(range(1, 6))]
list_elicit.append("-")



# -------------- SETTINGS --------------
listed = ["-", "No", "Yes"]
data = {
    'cam_teams': ["-", "Akamkpa 1", "Bakassi", "Ikom", "Akamkpa 2",    "Akpabuyo", "Calabar South", "Calabar Municipal 1", "Calabar Municipal 2",
                  "Obubra", "Yakurr", "Abi", "biase", "Boki", "Etung",  "Odukpani"],
    'type_of_structural_driver': ["-", "TBA", "Healing home", "Traditional Bone-Setter", "Plantation", "Settlement",
                                  "Prayer House", "PMV", "Health-Center", "Private Hospital", "Pharmacy", "Laboratory", "Others"],
    'index_year_of_birth': listyear,
    # ---
    'fullname_of_index': "",
    'phone_no_index': "",
    'address_of_index': "",
    'index_partners_elicited':list_elicit,

    'index_testing_modality': ["-", "Social Network Testing", "Sexual Network Testing", "Geneology Testing", "Self-Testing (HIVST)",
                         "Targetted Testing", "Voluntary Counselling Testing (VCT)", "PMTCT Testing"],
    'sex_of_index': ["-", "Male", "Female","Others"],
    'residence_LGA_of_index': '',
    'test_result': ["-", "Negative", "Positive"],
    'index_comments': '',
  

    # ---Parner 1 info--
    'fullname_of_partner1':'',
    'phone_no_partner1':'',
    'year_of_birth_of_partner1': listyear,
    'partner1_relationship':['-','Boyfriend','Girlfriend','Husband','Wife','friend','Others'],
    'sex_of_partner1':['-','Male','Female','Others'],
    'location_partner1':['-','Within Cross-river','Outside Cross-river'],
    'residence_LGA_of_partner1': '',
    'test_result_partner1': ["-", "Negative", "Positive","Not yet Tested"],
     'partner1_comments': '',
    'partner1_address': '',

       # ---Parner 2 info--
    'fullname_of_partner2':'',
    'phone_no_partner2':'',
    'year_of_birth_of_partner2': listyear,
    'partner2_relationship':['-','Boyfriend','Girlfriend','Husband','Wife','friend','Others'],
    'sex_of_partner2':['-','Male','Female','Others'],
    'location_partner2':['-','Within Cross-river','Outside Cross-river'],
    'residence_LGA_of_partner2': '',
    'test_result_partner2': ["-", "Negative", "Positive","Not yet Tested"],
     'partner2_comments': '',
    'partner2_address': '',
    # ---Parner 3 info--
    'fullname_of_partner3':'',
    'phone_no_partner3':'',
    'year_of_birth_of_partner3': listyear,
    'partner3_relationship':['-','Boyfriend','Girlfriend','Husband','Wife','friend','Others'],
    'sex_of_partner3':['-','Male','Female','Others'],
    'location_partner3':['-','Within Cross-river','Outside Cross-river'],
    'residence_LGA_of_partner3': '',
    'test_result_partner3': ["-", "Negative", "Positive","Not yet Tested"],
     'partner3_comments': '',
    'partner3_address': '',

    # ---Parner 4 info--
    'fullname_of_partner4':'',
    'phone_no_partner4':'',
    'year_of_birth_of_partner4': listyear,
    'partner4_relationship':['-','Boyfriend','Girlfriend','Husband','Wife','friend','Others'],
    'sex_of_partner4':['-','Male','Female','Others'],
    'location_partner4':['-','Within Cross-river','Outside Cross-river'],
    'residence_LGA_of_partner4': '',
    'test_result_partner4': ["-", "Negative", "Positive","Not yet Tested"],
     'partner4_comments': '',
    'partner4_address': '',

     # ---Parner 4 info--
    'fullname_of_partner5':'',
    'phone_no_partner5':'',
    'year_of_birth_of_partner5': listyear,
    'partner5_relationship':['-','Boyfriend','Girlfriend','Husband','Wife','friend','Others'],
    'sex_of_partner5':['-','Male','Female','Others'],
    'location_partner5':['-','Within Cross-river','Outside Cross-river'],
    'residence_LGA_of_partner5': '',
    'test_result_partner5': ["-", "Negative", "Positive","Not yet Tested"],
     'partner5_comments': '',
    'partner5_address': ''
}

st.header(f"PreTest Elicitation Tool")
st.markdown("_This form is to be correctly filled for each **Person offered Pre-Test ICT** by the CAM Team_",
            unsafe_allow_html=True)

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
        #------------Index Information-------------------
        st.markdown("<h3>Index Information:<h3>", unsafe_allow_html=True)
        index1, index2= st.columns(2)
        index1.text_input("fullname of Index:",
                       data['fullname_of_index'], key="fullname_of_index")
        index2.text_input("Phone No:",
                       data['phone_no_index'], key="phone_no_index")
        index1.selectbox(
            "Select year of birth", reversed(listyear),
            key="index_year_of_birth")
        index2.selectbox("Select Testing Modality:",
                       data['index_testing_modality'], key="index_testing_modality")
        index1.selectbox("Select the Sex:", data['sex_of_index'], key="sex_of_index")

        index2.selectbox("Number of Partners Elicited from Index",reversed(list_elicit),
                          key='index_partners_elicited')
       
       
        index1.text_input("LGA of Residence:",
                       data['residence_LGA_of_index'], key="residence_LGA_of_index")
        index2.selectbox("Result of the Test:",
                       data['test_result'], key="test_result")
        index1.text_area(
                    "", placeholder="Provide a Client descriptive address ...", key='address_of_index')
        index2.text_area(
                    "", placeholder="Comments about Index", key='index_comments')
  
         #------------Partner 1 iNFO-------------------
        partner1 = st.expander("Partner 1 Information", expanded=False)
        with partner1.container():
               
            st.markdown("<h3>Partner 1 Information:<h3>", unsafe_allow_html=True)
            pc1, pc2= st.columns(2)
            pc1.text_input("fullname of Partner:",
                        key="fullname_of_partner1", placeholder='John Doe')
            pc2.text_input("Phone No:",
                        key='phone_no_partner1', placeholder="080XXXXXXXX")
            pc1.selectbox(
                "Select year of birth", reversed(listyear),
                key="year_of_birth_of_partner1")
            pc2.selectbox("Relationship with Index:",
                        data['partner1_relationship'], key="partner1_relationship")
            pc1.selectbox("Select the Sex:", data['sex_of_partner1'], key="sex_of_partner1")

            pc2.selectbox("Location:",
                        data["location_partner1"], key="location_partner1")
            pc1.text_input("LGA of Residence:",
                        key="residence_LGA_of_partner1", placeholder="Calabar Municipal")

            pc2.selectbox("Result of the Test:",
                        data['test_result_partner1'], key="test_result_partner1")
            pc1.text_area(
                        "", placeholder="Provide descriptive address of the Partner ...", key='partner1_address')
            pc2.text_area(
                        "", placeholder="Comments about this Partner", key='partner1_comments')

        #------------Partner 2 iNFO-------------------
        partner2 = st.expander("Partner 2 Information", expanded=False)
        with partner2.container():
                
            st.markdown("<h3>Partner 2 Information:<h3>", unsafe_allow_html=True)
            p2c1, p2c2= st.columns(2)
            p2c1.text_input("fullname of Partner:",
                        key="fullname_of_partner2", placeholder='John Doe')
            p2c2.text_input("Phone No:",
                        key='phone_no_partner2', placeholder="080XXXXXXXX")
            p2c1.selectbox(
                "Select year of birth", reversed(listyear),
                key="year_of_birth_of_partner2")
            p2c2.selectbox("Relationship with Index:",
                        data['partner2_relationship'], key="partner2_relationship")
            p2c1.selectbox("Select the Sex:", data['sex_of_partner2'], key="sex_of_partner2")

            p2c2.selectbox("Location:",
                        data["location_partner2"], key="location_partner2")
            p2c1.text_input("LGA of Residence:",
                        key="residence_LGA_of_partner2", placeholder="Calabar Municipal")

            p2c2.selectbox("Result of the Test:",
                        data['test_result_partner2'], key="test_result_partner2")
            p2c1.text_area("",
                        placeholder="Provide a partner 2 descriptive address ...", key='partner2_address')
            p2c2.text_area("",
                        placeholder="Comments about partner 2", key='partner2_comments')   

        #------------Partner 3 iNFO-------------------
        partner3 = st.expander("Partner 3 Information", expanded=False)
        with partner3.container():
               
            st.markdown("<h3>Partner 3 Information:<h3>", unsafe_allow_html=True)
            pc1, pc2= st.columns(2)
            pc1.text_input("fullname of Partner:",
                        key="fullname_of_partner3", placeholder='John Doe')
            pc2.text_input("Phone No:",
                        key='phone_no_partner3', placeholder="080XXXXXXXX")
            pc1.selectbox(
                "Select year of birth", reversed(listyear),
                key="year_of_birth_of_partner3")
            pc2.selectbox("Relationship with Index:",
                        data['partner3_relationship'], key="partner3_relationship")
            pc1.selectbox("Select the Sex:", data['sex_of_partner3'], key="sex_of_partner3")

            pc2.selectbox("Location:",
                        data["location_partner3"], key="location_partner3")
            pc1.text_input("LGA of Residence:",
                        key="residence_LGA_of_partner3", placeholder="Calabar Municipal")

            pc2.selectbox("Result of the Test:",
                        data['test_result_partner3'], key="test_result_partner3")
            pc1.text_area(
                        "", placeholder="Provide descriptive address of the Partner ...", key='partner3_address')
            pc2.text_area(
                        "", placeholder="Comments about this Partner", key='partner3_comments')


        #------------Partner 4 iNFO-------------------
        partner4 = st.expander("Partner 4 Information", expanded=False)
        with partner4.container():
               
            st.markdown("<h3>Partner 4 Information:<h3>", unsafe_allow_html=True)
            pc1, pc2= st.columns(2)
            pc1.text_input("fullname of Partner:",
                        key="fullname_of_partner4", placeholder='John Doe')
            pc2.text_input("Phone No:",
                        key='phone_no_partner4', placeholder="080XXXXXXXX")
            pc1.selectbox(
                "Select year of birth", reversed(listyear),
                key="year_of_birth_of_partner4")
            pc2.selectbox("Relationship with Index:",
                        data['partner4_relationship'], key="partner4_relationship")
            pc1.selectbox("Select the Sex:", data['sex_of_partner4'], key="sex_of_partner4")

            pc2.selectbox("Location:",
                        data["location_partner4"], key="location_partner4")
            pc1.text_input("LGA of Residence:",
                        key="residence_LGA_of_partner4", placeholder="Calabar Municipal")

            pc2.selectbox("Result of the Test:",
                        data['test_result_partner4'], key="test_result_partner4")
            pc1.text_area(
                        "", placeholder="Provide descriptive address of the Partner ...", key='partner4_address')
            pc2.text_area(
                        "", placeholder="Comments about this Partner", key='partner4_comments')


        #------------Partner 3 iNFO-------------------
        partner5 = st.expander("Partner 5 Information", expanded=False)
        with partner5.container():
               
            st.markdown("<h3>Partner 5 Information:<h3>", unsafe_allow_html=True)
            pc1, pc2= st.columns(2)
            pc1.text_input("fullname of Partner:",
                        key="fullname_of_partner5", placeholder='John Doe')
            pc2.text_input("Phone No:",
                        key='phone_no_partner5', placeholder="080XXXXXXXX")
            pc1.selectbox(
                "Select year of birth", reversed(listyear),
                key="year_of_birth_of_partner5")
            pc2.selectbox("Relationship with Index:",
                        data['partner5_relationship'], key="partner5_relationship")
            pc1.selectbox("Select the Sex:", data['sex_of_partner5'], key="sex_of_partner5")

            pc2.selectbox("Location:",
                        data["location_partner5"], key="location_partner5")
            pc1.text_input("LGA of Residence:",
                        key="residence_LGA_of_partner5", placeholder="Calabar Municipal")

            pc2.selectbox("Result of the Test:",
                        data['test_result_partner5'], key="test_result_partner5")
            pc1.text_area(
                        "", placeholder="Provide descriptive address of the Partner ...", key='partner5_address')
            pc2.text_area(
                        "", placeholder="Comments about this Partner", key='partner5_comments')    
    submitted = st.form_submit_button("Submit Response")
    
     # ----------------- Validate form-----------------------------
    if submitted:
        elicited=int(st.session_state["index_partners_elicited"])
        if int(st.session_state["index_partners_elicited"]) < 1:
            st.error("The number of Partners Elicied from Index must be Greater than 0")
            st.stop()
        elicited=int(st.session_state["index_partners_elicited"])
          
        result = {key: str(st.session_state[key]) if i < ((elicited+1)*10)+1 else "" for i, key in enumerate(
                list(data.keys()))}
        for key in list(result.keys())[:((elicited+1)*10)+1]:
            if ("phone_no"  in key):
                continue
            elif(is_not_a_word(str(st.session_state[key]))):
                st.error("The input for " + key.upper() +
                             " is Incorrect or Empty")
                st.stop()
         
        # -------------------Submission-----------------------
        ip = get_ip()
        timestamp = location["timestamp"]
        location2 = location['coords']
        insert_partner(str(timestamp), str(ip), location2, result)
        progress()

# imgcol1, imgcol2 = st.columns(2)
# files = [file for file in glob.glob("tools\images\*")]


# img1 = files[0]
# img2 = files[1]
# with imgcol1:
#     st.image(img1)

# with imgcol2:
#     st.image(img2)
