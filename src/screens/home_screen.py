import streamlit as st
from src.screens.components.header import header_home
from src.screens.ui.base_layout import style_base_layout, style_background_home
from src.screens.components.footer import footer_home


def home_screen():

    # Background + layout first
    style_background_home()
    style_base_layout()

    # Header
    header_home()

    st.write("")  # spacing

    col1, col2 = st.columns(2, gap="large")

    # -----------------------------
    # TEACHER SECTION
    # -----------------------------
    with col1:
        st.header("I'm Teacher")
        st.image(
            "https://res.cloudinary.com/dvaqjnnd1/image/upload/f_auto,q_auto/Copilot_20260425_174806_r8pktj",
            width=145
        )

        if st.button(
            "Teacher Portal",
            type="primary",
            icon=":material/arrow_outward:",
            icon_position="right",
            use_container_width=True
        ):
            st.session_state["Login_Type"] = "teacher"
            st.query_params["screen"] = "teacher"
            st.rerun()

    # -----------------------------
    # STUDENT SECTION
    # -----------------------------
    with col2:
        st.header("I'm Student")
        st.image(
            "https://res.cloudinary.com/dvaqjnnd1/image/upload/f_auto,q_auto/Copilot_20260425_174017_uq0ecl",
            width=145
        )

        if st.button(
            "Student Portal",
            type="primary",
            icon=":material/arrow_outward:",
            icon_position="right",
            use_container_width=True
        ):
                st.session_state["Login_Type"] = "student"
                st.query_params["screen"] = "student"
                st.rerun()

    # Footer
    footer_home()
