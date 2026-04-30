import datetime
import pandas as pd
import streamlit as st
from src.screens.ui.base_layout import style_background_dashboard, style_base_layout
from src.screens.components.header import header_dashboard
from src.screens.components.footer import footer_dashboard
from src.screens.database.db import check_teacher_exist, create_teacher, teacher_login, get_teacher_subject
from src.screens.components.dialog_create_subject import create_subject_dialog
from src.screens.components.subject_card import subject_card
from src.screens.components.dialog_share_subject import share_subject_dialog
from src.screens.components.dialog_add_photo import add_photos_dialog
from src.screens.pipelines.face_pipeline import predict_attendance
from src.screens.components.dialog_voice_attendance import voice_attendance_dialog
import numpy as np
from src.screens.database.db import supabase
from src.screens.components.dialog_attendance_result import attendance_result_dialog
from src.screens.database.db import get_attendance_for_teacher

def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_login_type" not in st.session_state:
        st.session_state.teacher_login_type = "login"

    screen = st.session_state.teacher_login_type

    if screen == "login":
        teacher_screen_login()
    elif screen == "register":
        teacher_screen_register()
    elif screen == "dashboard":
        teacher_dashboard()


def teacher_dashboard():

    if "teacher_data" not in st.session_state:
        st.error("Session expired. Please login again.")
        st.session_state.teacher_login_type = "login"
        st.rerun()

    teacher_data = st.session_state.teacher_data

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {teacher_data['name']}")
        if st.button("Log out", type="secondary", key="logoutbtn"):
            st.session_state.teacher_login_type = "login"
            st.session_state.pop("teacher_data", None)
            st.rerun()

    st.write("")

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        active = st.session_state.current_teacher_tab == "take_attendance"
        if st.button("Take Attendance", type="primary" if active else "tertiary", icon="📝", use_container_width=True):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        active = st.session_state.current_teacher_tab == "manage_subjects"
        if st.button("Manage Subjects", type="primary" if active else "tertiary", icon="📔", use_container_width=True):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        active = st.session_state.current_teacher_tab == "attendance_records"
        if st.button("Attendance Records", type="primary" if active else "tertiary", icon="📒", use_container_width=True):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    tab = st.session_state.current_teacher_tab

    if tab == "take_attendance":
        teacher_tab_take_attendance()
    elif tab == "manage_subjects":
        teacher_tab_manage_subject()
    elif tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']

    st.header("Take AI Attendance")

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subject(teacher_id)

    if not subjects:
        st.warning('You have not created any subjects yet')
        return

    subject_options = {f"{s['name']}-{s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    selected_subject_id = subject_options[selected_subject_label]
    st.divider()

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_camera:', use_container_width=True):
            st.session_state.show_add_photos_dialog = True

    if st.session_state.get('show_add_photos_dialog'):
        st.session_state.show_add_photos_dialog = False
        add_photos_dialog()

    if st.session_state.attendance_images:
        st.subheader('Captured Photos')
        img_cols = st.columns(4)
        for i, img in enumerate(st.session_state.attendance_images):
            with img_cols[i % 4]:
                st.image(img, use_container_width=True, caption=f"Photo {i+1}")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.session_state.attendance_images:
            if st.button('Clear all photos', use_container_width=True, type='tertiary', icon=':material/delete:'):
                st.session_state.attendance_images = []
                st.rerun()

    with c2:
        if st.session_state.attendance_images:
            if st.button('Run face Analysis', use_container_width=True, type='secondary', icon=':material/analytics:'):
                with st.spinner('Analyzing photos, please wait..'):
                    all_detected_ids = {}

                    for i, img in enumerate(st.session_state.attendance_images):
                        img_np = np.array(img.convert('RGB'))
                        detected, _, _ = predict_attendance(img_np)

                        if detected:
                            for sid in detected.keys():
                                student_id = int(sid)
                                all_detected_ids.setdefault(student_id, []).append(f"Photo {i+1}")

                    enrolled_res = supabase.table('subject_students').select("*,students(*)").eq('subject_id', selected_subject_id).execute()
                    enrolled_students = enrolled_res.data

                    if not enrolled_students:
                        st.warning('No students enrolled in this subject yet')
                    else:
                        results = []
                        attendance_to_log = []

                        current_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                        for node in enrolled_students:
                            student = node['students']
                            sources = all_detected_ids.get(int(student['student_id']), [])
                            is_present = len(sources) > 0

                            results.append({
                                "Name": student['name'],
                                "ID": student['student_id'],
                                "Sources": ", ".join(sources) if is_present else "Not detected",
                                "Status": "✅ Present" if is_present else "❌ Absent"
                            })

                            attendance_to_log.append({
                                'student_id': student['student_id'],
                                'subject_id': selected_subject_id,
                                'timestamp': current_timestamp,
                                'is_present': bool(is_present)
                            })

                        attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button('Use Voice Attendance', type='primary', icon=':material/mic:', use_container_width=True):
            voice_attendance_dialog(selected_subject_id)


def teacher_tab_manage_subject():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header("Manage Subjects")
    with col2:
        if st.button('Create new subject', use_container_width=True):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subject(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]

            def share_btn(sub=sub):
                if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                    share_subject_dialog(sub['name'], sub['subject_code'])
                st.write("")

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("NO SUBJECT FOUND, CREATE ABOVE")


def teacher_tab_attendance_records():
    st.header("Attendance Records")

    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No attendance records found yet.")
        return

    data = []
    for r in records:
        ts = r.get('timestamp')

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M:%S") if ts else None,
            "Subject": r['subject']['name'],
            "Subject Code": r['subject']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        )
        .reset_index()
    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str)
        + " / "
        + summary['Total_Count'].astype(str)
        + " Students"
    )

    display_df = summary.sort_values(by='ts_group', ascending=False)[
        ["Time", "Subject", "Subject Code", "Attendance Stats"]
    ]

    st.dataframe(display_df, use_container_width=True)


def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go Back to Home", type="secondary"):
            st.session_state["Login_Type"] = None
            st.query_params.clear()
            st.session_state.teacher_login_type = "login"
            st.rerun()

    st.header("Login using password", anchor=False)
    st.write("")

    teacher_username = st.text_input("Enter username", placeholder="AlicaSchmidt")
    teacher_password = st.text_input("Enter Password", type="password", placeholder="enter password")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login", icon=":material/passkey:", use_container_width=True):
            user = teacher_login(teacher_username, teacher_password)
            if user:
                st.session_state.teacher_data = user
                st.session_state.teacher_login_type = "dashboard"
                st.toast("Welcome back!", icon="👋")
                st.rerun()
            else:
                st.error("Invalid username or password")

    with col2:
        if st.button("Register", type="primary", icon=":material/passkey:", use_container_width=True):
            st.session_state.teacher_login_type = "register"
            st.rerun()

    footer_dashboard()


def register_teacher(username, name, password, confirm):
    if not username or not name or not password or not confirm:
        return False, "All fields are required!"

    if password != confirm:
        return False, "Passwords do not match"

    if check_teacher_exist(username):
        return False, "Username already exists"

    try:
        create_teacher(username, password, name)
        return True, "Successfully created account. You can login now."
    except Exception:
        return False, "Unexpected error while registering"


def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go Back to Home", type="secondary"):
            st.session_state["Login_Type"] = None
            st.query_params.clear()
            st.session_state.teacher_login_type = "login"
            st.rerun()

    st.header("Register Your Profile")
    st.write("")

    username = st.text_input("Enter username", placeholder="AlicaSchmidt")
    name = st.text_input("Enter name", placeholder="Alica Schmidt")
    password = st.text_input("Enter Password", type="password", placeholder="enter password")
    confirm = st.text_input("Confirm your Password", type="password", placeholder="confirm your password")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Register Now", icon=":material/passkey:", use_container_width=True):
            success, message = register_teacher(username, name, password, confirm)
            if success:
                st.success(message)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)

    with col2:
        if st.button("Login Instead", type="primary", icon=":material/passkey:", use_container_width=True):
            st.session_state.teacher_login_type = "login"
            st.rerun()

    footer_dashboard()