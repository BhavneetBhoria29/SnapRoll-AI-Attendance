
import streamlit as st
def footer_home():



    logo_url="https://copilot.microsoft.com/th/id/BCO.c6766c32-a0a6-4db6-8705-774f4388cf26.png"



    st.markdown(f"""
            <div style="margin-top:2rem; display: flex; gap:6px; justify-content:center; items-align:center;">
            <p style="font-weight:bold; color:white;" >Created by </p>
            <img src ="{logo_url}" style="max-height:80px"/>
             </div>  



                """,unsafe_allow_html=True)