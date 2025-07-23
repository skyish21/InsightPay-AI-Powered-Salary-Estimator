import streamlit as st

st.set_page_config(page_title="Salary Prediction App", layout="centered")

st.markdown("# 💼 Salary Predictor")
st.markdown("#### Choose how you want to continue:")

col1, col2 = st.columns(2)

with col1:
    if st.button("📝 Manual Input", use_container_width=True):
        st.switch_page("pages/1_Manual_Input.py")

with col2:
    if st.button("📄 Upload Resume", use_container_width=True):
        st.switch_page("pages/2_Resume_Upload.py")
