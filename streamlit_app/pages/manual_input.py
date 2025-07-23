import streamlit as st
import pandas as pd
from utils.encoding_utils import encode_inputs, model, le_gender, le_title

st.markdown("# 📝 Manual Input Form")

with st.form("manual_form"):
    gender = st.selectbox("Gender", ['Female', 'Male'], index=None, placeholder="Select Gender")
    education = st.selectbox("Education Level", ['High School', 'Bachelor', 'Master', 'PhD'], index=None, placeholder="Select Education")
    title = st.selectbox("Job Title", list(le_title.classes_), index=None, placeholder="Select Title")
    seniority = st.selectbox("Seniority Level", ['Junior', 'Mid', 'Senior', 'Lead', 'Executive'], index=None, placeholder="Select Level")
    location = st.selectbox("Location", ['Rural', 'Suburban', 'Urban'], index=None, placeholder="Select Location")
    experience = st.number_input("Years of Experience", min_value=0, step=1, placeholder="Enter experience")
    age = st.number_input("Age", min_value=18, max_value=70, step=1, placeholder="Enter age")

    submitted = st.form_submit_button("Predict Salary")

    if submitted:
        df = pd.DataFrame([{
            "Gender": gender,
            "Education Level": education,
            "General Title": title,
            "Seniority Level": seniority,
            "Years of Experience": experience,
            "Location": location,
            "Age": age
        }])

        encoded_df = encode_inputs(df)
        prediction = model.predict(encoded_df)[0]

        st.success(f"💰 Estimated Salary: ₹ {int(prediction):,}")

        # Store history
        if "history" not in st.session_state:
            st.session_state.history = []

        st.session_state.history.append({**df.to_dict(orient='records')[0], "Prediction": int(prediction)})

        # CSV Download
        hist_df = pd.DataFrame(st.session_state.history)
        csv = hist_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Predictions", csv, "predictions.csv", "text/csv")
