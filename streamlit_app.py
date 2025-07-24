import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from resume_parser import extract_resume_text, parse_resume_features
import pickle
import os

# === Load trained model ===
model = pickle.load(open("salary_prediction_model.pkl", "rb"))

# === LabelEncoders (must match training) ===
le_gender = LabelEncoder()
le_gender.fit(['Female', 'Male'])

le_title = LabelEncoder()
le_title.fit(['Advisor', 'Analyst', 'Designer', 'Director', 'Engineer', 'Manager', 'Other', 'Scientist'])

# === Mappings ===
education_map = {'High School': 0, 'Bachelor': 1, 'Master': 2, 'PhD': 3}
location_map = {'Rural': 0, 'Suburban': 1, 'Urban': 2}
seniority_map = {'Junior': 0, 'Mid': 1, 'Senior': 2, 'Lead': 3, 'Executive': 4}


# === Helper: Encode ===
def encode_inputs(df):
    df['Gender'] = le_gender.transform(df['Gender'])
    df['General Title'] = le_title.transform(df['General Title'])
    df['Education Level'] = df['Education Level'].map(education_map)
    df['Location'] = df['Location'].map(location_map)
    df['Seniority Level'] = df['Seniority Level'].map(seniority_map)
    return df

# === Sidebar Info ===
with st.sidebar:
    st.markdown("## 📚 Info Panel")
    st.markdown("---")

    st.markdown("""
    Welcome to **InsightPay**, a smart ML app that predicts salaries based on:
    - 📄 Uploaded resumes
    - 📝 Manual form inputs

    ### 🔍 Features:
    - Resume parsing using NLP
    - Title, seniority & experience extraction
    - Clean UI with dual input modes
    - CSV export of predictions
    """)

    st.markdown("### 🛠 Built With")
    st.markdown("""
    - Python 🐍  
    - Streamlit ⚡  
    - scikit-learn 🔧  
    - PDFMiner / PyMuPDF 📄  
    - Pandas 🐼
    """)

    st.markdown("### 🧪 Model Info")
    st.markdown("""
    - LightGBM (trained on labeled dataset)
    - LabelEncoded + Mapped inputs
    """)

    st.markdown("---")
    st.markdown("💡 Try uploading a sample resume from below or use manual mode!")

    st.markdown("---")
    st.markdown("## 👩‍💻 About Me")
    st.markdown("Trying out new things in ML + NLP!")
    st.markdown(
        """
        <div style='text-align: center;'>
            <a href='https://github.com/skyish21' target='_blank'>GitHub 🔗</a>&nbsp;|&nbsp;
            <a href='https://www.linkedin.com/in/ishika-sharma-79a67a326/' target='_blank'>💼 LinkedIn</a>
        </div>
        """,
        unsafe_allow_html=True
    )


# === PAGE ===
st.title("InsightPay 💰 — AI-Powered Salary Estimator")

st.markdown("---")

st.markdown("""
<div style="font-size:17px; line-height:1.6; padding-bottom:10px;">
Welcome to <b>InsightPay</b> – an AI-powered salary prediction tool! 📊<br>
Upload a resume <i>or</i> enter candidate/job details manually to estimate salary using machine learning.<br><br>
Built using Python, NLP, and predictive modeling, this tool helps individuals and recruiters quickly assess compensation benchmarks.<br><br>
Want to know how this app works? Check the sidebar! 📌 
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("Select how you want to enter job/candidate details:")

col1, col2 = st.columns(2)

if "mode" not in st.session_state:
    st.session_state.mode = None

with col1:
    if st.button("📝 Manual Input", use_container_width=True):
        st.session_state.mode = "manual"
with col2:
    if st.button("📄 Upload Resume", use_container_width=True):
        st.session_state.mode = "resume"

st.markdown("---")

gender = education = title = seniority = experience = location = age = None
parsed = {}

# === MANUAL MODE ===
if st.session_state.mode == "manual":
    st.header("📝 Manual Entry")
    gender = st.selectbox("Gender", ['Female', 'Male'])
    education = st.selectbox("Education Level", list(education_map.keys()))
    title = st.selectbox("General Title", list(le_title.classes_))
    seniority = st.selectbox("Seniority Level", list(seniority_map.keys()))
    experience = st.number_input("Years of Experience", 0, 50, step=1)
    location = st.selectbox("Location", list(location_map.keys()))
    age = st.number_input("Age", 18, 65, step=1)

# === RESUME UPLOAD MODE ===
elif st.session_state.mode == "resume":
    st.header("📄 Upload Resume")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    sample_resumes = {
        "Junior Engineer": "resumes/resume_engineer.pdf",
        "Data Analyst": "resumes/resume_data.pdf",
        "Project Manager": "resumes/resume_manager.pdf",
        "Senior Data Scientist": "resumes/resume_scientist.pdf",
        "Intern": "resumes/resume_intern.pdf"
    }

    # === Change 1: Check if sample resumes exist ===
    if not os.path.exists("resumes"):
        st.warning("⚠️ 'resumes/' folder not found. Sample resumes will not work.")

    st.markdown("#### Or try a sample resume")
    sample_choice = st.selectbox("Choose Sample Resume", ["None"] + list(sample_resumes.keys()))

    if sample_choice != "None":
        sample_path = sample_resumes.get(sample_choice)
        if os.path.exists(sample_path):
            with open(sample_path, "rb") as f:
                sample_text = extract_resume_text(f)
                parsed = parse_resume_features(sample_text)
            st.success(f"✅ Parsed Sample: {sample_choice}")
        else:
            st.error(f"Sample file not found: {sample_path}")

    if uploaded_file and sample_choice == "None":
        with st.spinner("🔍 Parsing resume..."):
            resume_text = extract_resume_text(uploaded_file)
            parsed = parse_resume_features(resume_text)

    if parsed:
        st.subheader("📋 Parsed Resume Info (Editable)")

        try:
            gender_idx = ['Female', 'Male'].index(parsed.get("Gender", "Female"))
        except ValueError:
            gender_idx = None
        try:
            edu_idx = list(education_map.keys()).index(parsed.get("Education Level", "Bachelor"))
        except ValueError:
            edu_idx = None
        try:
            title_idx = list(le_title.classes_).index(parsed.get("General Title", "Other"))
        except ValueError:
            title_idx = list(le_title.classes_).index("Other")
        try:
            seniority_idx = list(seniority_map.keys()).index(parsed.get("Seniority Level", "Mid"))
        except ValueError:
            seniority_idx = None

        gender = st.selectbox("Gender", ['Female', 'Male'], index=gender_idx)
        education = st.selectbox("Education Level", list(education_map.keys()), index=edu_idx)
        title = st.selectbox("General Title", list(le_title.classes_), index=title_idx)
        seniority = st.selectbox("Seniority Level", list(seniority_map.keys()), index=seniority_idx)
        experience = st.number_input("Years of Experience", 0, 50, value=parsed.get("Years of Experience", 0), step=1)
        options = ["-- Select Location --"] + list(location_map.keys())
        location = st.selectbox("Location", options)
        
        # Treat the placeholder as None
        if location == "-- Select Location --":
            location = None
        age = st.number_input("Age", 18, 65, value=parsed.get("Age", 25), step=1)

# === PREDICT BUTTON ===
if st.session_state.mode and gender and education and title and seniority and experience is not None and location and age:
    if st.button("🔮 Predict Salary", key="predict_salary"):
        input_df = pd.DataFrame([{
            "Gender": gender,
            "Education Level": education,
            "General Title": title,
            "Seniority Level": seniority,
            "Years of Experience": experience,
            "Location": location,
            "Age": age
        }])

        encoded_df = encode_inputs(input_df.copy())
        prediction = model.predict(encoded_df)[0]
        st.success(f"💰 Estimated Salary: $ {int(prediction):,}")

        # Store for download
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append({**input_df.iloc[0].to_dict(), "Predicted Salary": int(prediction)})

        df_history = pd.DataFrame(st.session_state.history)
        st.download_button("⬇️ Download Prediction(s)", df_history.to_csv(index=False).encode("utf-8"), "predictions.csv")



