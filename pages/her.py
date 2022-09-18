import streamlit as st


from streamlit_js_eval import get_geolocation
# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            div.element-container.css-1t5s6n0.e1tzin5v3{
                background-color: transparent}
    
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

location = get_geolocation('Get my location')

st.write(location)
st.write(location["coords"])
st.write(location['timestamp'])
