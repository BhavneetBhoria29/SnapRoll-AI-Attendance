import streamlit as st

from src.screens.database.db import create_subject
from src.screens.database.config import supabase
from src.screens.database.db import enroll_student_to_subject
import time
@st.dialog("Enroll in Subject")
def enrol_dialog():
    st.write('Enter the subject code provided by your teacher to enrol')
    join_code =st.text_input('Subject Code',placeholder='Eg, CS101')
    if st.button('Enroll now', type='primary', width='stretch'):
        if join_code:
            res = supabase.table('subject').select('subject_id,name,subject_code').ilike('subject_code', join_code).execute()
        
        if res.data:
            subject = res.data[0]
            student_id = st.session_state.student_data['student_id']

            check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()
            if check.data:
                st.warning('You are already enrolled')
            else:
                enroll_student_to_subject(student_id, subject['subject_id'])
                st.success('Successfully Enrolled')
                time.sleep(1)
                st.rerun()
        else:
            st.warning('Subject code not found. Please check with your teacher.')
    else:
        st.warning('Please enter a subject code')