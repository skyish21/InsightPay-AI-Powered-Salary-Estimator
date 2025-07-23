import streamlit as st
import pandas as pd
import re
from resume_parser import extract_resume_text, parse_resume_features 
from utils.encoding_utils import encode_inputs, model, le_gender, le_title, education_map, location_map, seniority_map

# === Page Config ===
st.set_page_config(page_title="Upload Resume", layout="wide")

# === UI ===
st.title("📄 Upload Resume for Salary Prediction")

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file:
    with st.spinner("🔍 Parsing resume..."):
        resume_text = extract_resume_text(uploaded_file)
        extracted = parse_resume_features(resume_text)  # ✅

    st.subheader("📋 Parsed Resume Info (Editable)")

    gender = st.selectbox("Gender", ['Female', 'Male'], index=['Female', 'Male'].index(extracted.get("Gender", "Female")))
    education = st.selectbox("Education Level", list(education_map.keys()), index=list(education_map.keys()).index(extracted.get("Education Level", "Bachelor")))
    title = st.selectbox("General Title", list(le_title.classes_), index=list(le_title.classes_).index(extracted.get("General Title", "Other")))
    seniority = st.selectbox("Seniority Level", list(seniority_map.keys()), index=list(seniority_map.keys()).index(extracted.get("Seniority Level", "Mid")))
    experience = st.number_input("Years of Experience", 0, 50, value=extracted.get("Years of Experience", 0), step=1)
    location = st.selectbox("Location", list(location_map.keys()))
    age = st.number_input("Age", 18, 65, value=extracted.get("Age", 25), step=1)

    if st.button("🔮 Predict Salary"):
        input_df = pd.DataFrame([{
            "Gender": gender,
            "Education Level": education,
            "General Title": title,
            "Seniority Level": seniority,
            "Years of Experience": experience,
            "Location": location,
            "Age": age
        }])

        input_df['Gender'] = le_gender.transform(input_df['Gender'])
        input_df['General Title'] = le_title.transform(input_df['General Title'])
        input_df['Education Level'] = input_df['Education Level'].map(education_map)
        input_df['Location'] = input_df['Location'].map(location_map)
        input_df['Seniority Level'] = input_df['Seniority Level'].map(seniority_map)

        prediction = model.predict(input_df)[0]
        st.success(f"💰 Estimated Salary: ₹ {int(prediction):,}")

        # Store to session
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append({**input_df.to_dict(orient='records')[0], "Prediction": int(prediction)})

        # Download option
        history_df = pd.DataFrame(st.session_state.history)
        csv = history_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Predictions", csv, "predictions.csv", "text/csv")
