
import streamlit as st



def main():
    st.header("This is title")
    name=st.text_input("Enter your name")
    button=st.button('Display my name',type='primary')
    button2=st.button('Display my name',type='primary')

main()