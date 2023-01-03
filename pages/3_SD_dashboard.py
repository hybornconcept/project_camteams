import streamlit as st
import pandas as pd
from datetime import datetime
import datetime
from tools.components import *
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from tools.database import fetch_all_users
# ------------PAGE SETTINGS
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/


st.set_page_config(page_title="Dashboard",
                   page_icon=":bar_chart:",
                   layout='wide')

st.markdown("""<meta charset="utf-8">""", unsafe_allow_html=True)
st.markdown("""<meta name="viewport" content="width=device-width, initial-scale=1">""",
            unsafe_allow_html=True)
st.markdown("""<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
 integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">""", unsafe_allow_html=True)
# -----------Font CDN----------------------

st.markdown(""" <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">""", unsafe_allow_html=True)
# --- STREAMLIT STYLE ---
st.markdown("""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.1/font/bootstrap-icons.css">""", unsafe_allow_html=True)

hide_st_style = """
            <style>
            div.css-1fv8s86.e16nr0p33 >hr{margin-top:4vh;}
            div.css-zt5igj.e16nr0p32{margin-top:-3vh;}
            div.stMarkdown{margin-top:-4vh}
            span.css-10trblm.e16nr0p30{margin-top:0px}
            div.object-key-val{display:none}
            h3{font-size:20px}
            div.css-zt5igj.e16nr0p32{margin-top:-5vh}
            ul.css-1helkxk.e1fqkh3o9{margin-top:-4vh}
            ul.css-1helkxk.e1fqkh3o9{padding-bottom:5vh}
           
           
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# -----------------------containers ---------------------------------

mainSection = st.container()


# ------------Spacer function-------------------


# ------Title------------


# --- USER AUTHENTICATION ---
# users = fetch_all_users()

# usernames = [user["key"] for user in users]
# names = [user["name"] for user in users]
# hashed_passwords = [user["password"] for user in users]
# authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
#                                     "sales_dashboard", "abcdef", cookie_expiry_days=3)

# name, authentication_status, username = authenticator.login("Login", "main")

# if authentication_status == False:
#     st.error("Username/password is incorrect")

# if authentication_status == None:
#     st.warning("Please enter your username and password")


df = sanitize()

st.markdown(
    f'''<h1><i class="bi bi-bar-chart-line" style="font-size:40px"></i> Structural Drivers Mapping Dashboard</h1>''', unsafe_allow_html=True)
# '---'
# ---SIDEBAR---
# --- CAM TEAM FILTER  ------------
cam_team = st.sidebar.multiselect(
    "Select CAM Team:",
    df.cam_teams.unique().tolist())

# --- structural driver TEAM FILTER  ------------

structural_driver = st.sidebar.multiselect(
    "Select the structural Driver",
    df.type_of_structural_driver.unique().tolist())

# --- structural driver Client Load ------------
average_monthly_client = st.sidebar.select_slider(
    'Monthly Average Visit:', options=sorted(df['client_load'].unique()), value=max(sorted(df['client_load'].unique())))
col1, col2 = st.columns([4, 1])

# ----------------------------------------------------------------  filtering the dataframe  --------------------------
cam_team_filter = cam_team if cam_team else df.cam_teams.unique().tolist()
structural_driver_filter = structural_driver if structural_driver else df.type_of_structural_driver.unique().tolist()
filtered_df = df.query(
    "cam_teams in (@cam_team_filter) and type_of_structural_driver in (@structural_driver_filter) and client_load <= @average_monthly_client")

# st.write(filtered_df.shape)
# --- Map ------------
with col1:

    geolocation, Other_maps = st.tabs(["GIS_Maps", "Other_maps"])

    with geolocation:
        # spacer(2)
        # st.write('hshs')
        # df2 = pd.read_csv('./tools/bree.csv')
        st.map(data=filtered_df)
        # st.dataframe(filtered_df)

        # --- KPI ------------
with col2:
    total_entries = filtered_df.shape[0]  # get the total entries
    tba_entries = filtered_df['type_of_structural_driver'].value_counts()[
        'TBA']  # get the TBA entries
    current_entries = filtered_df['entry'].value_counts(
    )['Current']  # get the current entries
    retrospective_entries = filtered_df['entry'].value_counts(
    )['Retrospective']  # get the retrospective entries
    # the arrays
    kpi = [total_entries, tba_entries,
           current_entries, retrospective_entries]
    title = ['Total No. of entries', 'Total No. of TBAs',
             'Current Entries', 'Retrospective Entries']
    font = ['view-stacked', 'house', 'calendar2-check', 'recycle']
    # calling the method
    st.markdown(card_kpis(kpi, title, font),
                unsafe_allow_html=True)

spacer(4)
tab1, tab2 = st.tabs(
    ["Level of Effort  |  CAM Teams", "Level of Effort  |  Trend"])

with tab1:
    spacer(2)
    barchart(filtered_df, 'cam_teams', 'date_of_entry')
with tab2:
    spacer(2)
    trendchart(filtered_df, 'date_of_entry',
               'type_of_structural_driver')

# pie charts
spacer(3)
circle1, circle2 = st.tabs(
    ["Skill_Level", "Raw Data"])

with circle1:
    spacer(2)
    skill, residence = st.columns(2)
    with skill:
        spacer(3)
        st.subheader('Distribution by Skill Level')
        pie_chart(filtered_df, 'skill_level', 'date_of_entry')
    with residence:
        spacer(3)
        st.subheader('Distribution by Residence Area')
        pie_chart(filtered_df, 'residence_area', 'date_of_entry')

with circle2:
    spacer(3)
    st.markdown(filedownload(filtered_df), unsafe_allow_html=True)
    st.dataframe(filtered_df)
