
import streamlit as st
def footer_home():



    logo_url="https://res.cloudinary.com/dvaqjnnd1/image/upload/f_auto,q_auto/bhavneet_bhoria_black_bold_1x_epd99r"


    st.markdown(f"""
            <div style="margin-top:2rem; display: flex; gap:6px; justify-content:center; items-align:center;">
            <p style="font-weight:bold; color:white;" >Created by</p>
            <img src ="{logo_url}" style="max-height:50px"/>
             </div>  



                """,unsafe_allow_html=True)
    
def footer_dashboard():



    logo_url="https://res.cloudinary.com/dvaqjnnd1/image/upload/f_auto,q_auto/bhavneet_bhoria_black_bold_1x_epd99r"



    st.markdown(f"""
            <div style="margin-top:2rem; display: flex; gap:6px; justify-content:center; items-align:center;">
            <p style="font-weight:bold; color:black;" >Created by</p>
            <img src ="{logo_url}" style="max-height:50px"/>
             </div>  



                """,unsafe_allow_html=True)