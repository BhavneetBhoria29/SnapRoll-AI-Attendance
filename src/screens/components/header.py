import streamlit as st

def header_home():

    logo_url = "https://res.cloudinary.com/dvaqjnnd1/image/upload/f_auto,q_auto/snaproll_PNG_gl9tq1"

    st.markdown(
        f"""
        <div style="
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;
            margin-top:30px;
            margin-bottom:20px;
        ">
            <img src="{logo_url}" style="height:100px;" />
            <h1 style="
                text-align:center;
                color:#E0E3FF;
                font-weight:700;
                margin-top:10px;
                line-height:1.1;
            ">
                SNAP<br/>ROLL
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )


def header_dashboard():

    logo_url = "https://res.cloudinary.com/dvaqjnnd1/image/upload/f_auto,q_auto/snaproll_PNG_gl9tq1"

    st.markdown(
        f"""
        <div style="
            display:flex;
            align-items:center;
            justify-content:center;
            gap:12px;
            margin-top:10px;
            margin-bottom:10px;
        ">
            <img src="{logo_url}" style="height:75px;" />
            <h2 style="
                color:#5865F2;
                font-weight:700;
                margin:0;
                line-height:1.1;
            ">
                SNAP<br/>ROLL
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )
