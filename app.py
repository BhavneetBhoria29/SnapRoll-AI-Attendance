
import streamlit as st


from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.components.dialog_auto_enroll import auto_enroll_dialog

def main():
    st.setup_page_config(
         page_title="SnapRoll - Smart Attendance System",
         page_icon=":school:",
         layout="wide",
         initial_sidebar_state="collapsed"
    )

    # Restore Login_Type from query params on refresh
    if "Login_Type" not in st.session_state:
        st.session_state["Login_Type"] = st.query_params.get("screen")

    if "is_logged_in" not in st.session_state:
        st.session_state["is_logged_in"] = False
    if "user_role" not in st.session_state:
        st.session_state["user_role"] = None

    # Restore teacher session from query params
    if "teacher_login_type" not in st.session_state:
        st.session_state["teacher_login_type"] = st.query_params.get("teacher_screen", "login")

    join_code = st.query_params.get("join-code")
    if join_code:
        if st.session_state.get("Login_Type") != 'student':
            st.session_state["Login_Type"] = 'student'
            st.query_params["screen"] = "student"
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)

    match st.session_state["Login_Type"]:
        case "teacher":
            teacher_screen()
        case "student":
            student_screen()
        case None:
            home_screen()

main()
