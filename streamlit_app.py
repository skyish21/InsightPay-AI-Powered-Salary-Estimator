import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from resume_parser import extract_resume_text, parse_resume_features
import pickle

# === Page Config ===
st.set_page_config(page_title="Salary Predictor", layout="wide")

# === Load trained model (replace with your actual path) ===
model = pickle.load(open("salary_prediction_model.pkl", "rb"))

# Must match training

# Gender LabelEncoder (trained alphabetically)
le_gender = LabelEncoder()
le_gender.fit(['Female', 'Male'])

# General Title LabelEncoder (alphabetical order)
le_title = LabelEncoder()
le_title.fit([
    'Advisor', 'Analyst', 'Designer', 'Director',
    'Engineer', 'Manager', 'Other', 'Scientist'
])

# === Map dictionaries ===
education_map = {'High School': 0, 'Bachelor': 1, 'Master': 2, 'PhD': 3}
location_map = {'Rural': 0, 'Suburban': 1, 'Urban': 2}
seniority_map = {'Junior': 0, 'Mid': 1, 'Senior': 2, 'Lead': 3, 'Executive': 4}


# === Helper: Encode Inputs ===
def encode_inputs(df):
    df['Gender'] = le_gender.transform(df['Gender'])
    df['General Title'] = le_title.transform(df['General Title'])
    df['Education Level'] = df['Education Level'].map(education_map)
    df['Location'] = df['Location'].map(location_map)
    df['Seniority Level'] = df['Seniority Level'].map(seniority_map)
    return df


##
# STREAMLIT APP
##

# === Front Page ===
st.title("💼 Salary Prediction App")

# About link (top-right corner)
st.markdown("""
    <div style='text-align: right; margin-top: -50px;'>
        <a href="#about" style='font-size: 14px; text-decoration: none;'>🔗 About Me</a>
    </div>
""", unsafe_allow_html=True)

st.markdown("Choose how you want to provide your job/candidate details:")

st.markdown("---")

# Store selection
if "mode" not in st.session_state:
    st.session_state.mode = None

col1, col2 = st.columns(2)

with col1:
    if st.button("📝 Manual Input", use_container_width=True):
        st.session_state.mode = "manual"

with col2:
    if st.button("📄 Upload Resume", use_container_width=True):
        st.session_state.mode = "resume"

# Spacer
st.markdown("---")

# MANUAL MODE
if st.session_state.get("mode") == "manual":
    st.header("📝 Manual Input")

    gender = st.selectbox("Gender", ['Female', 'Male'], index=0, placeholder="Select gender")
    education = st.selectbox("Education Level", list(education_map.keys()), index=1, placeholder="Select education")
    title = st.selectbox("General Title", list(le_title.classes_), index=5, placeholder="Select title")
    seniority = st.selectbox("Seniority Level", list(seniority_map.keys()), index=1, placeholder="Select seniority")
    experience = st.number_input("Years of Experience", 0, 50, value=None, step=1, placeholder="Enter years of experience")
    location = st.selectbox("Location", list(location_map.keys()), index=2, placeholder="Select location")
    age = st.number_input("Age", 18, 65, value=None, step=1, placeholder="Enter age")

# RESUME MODE
elif st.session_state.mode == "resume":
    st.markdown("## 📄 Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    if uploaded_file:
        with st.spinner("Extracting details..."):
            resume_text = extract_resume_text(uploaded_file)
            parsed = parse_resume_features(resume_text)

        st.markdown("### 🧾 Parsed & Editable Details")

        gender = st.selectbox("Gender", ['Female', 'Male'], index=['Female', 'Male'].index(parsed.get("Gender", "Female")))
        education = st.selectbox("Education Level", list(education_map.keys()), index=list(education_map.keys()).index(parsed.get("Education Level", "Bachelor")))
        title = st.selectbox("General Title", list(le_title.classes_), index=list(le_title.classes_).index(parsed.get("General Title", "Other")))
        seniority = st.selectbox("Seniority Level", list(seniority_map.keys()), index=list(seniority_map.keys()).index(parsed.get("Seniority Level", "Mid")))
        experience = st.number_input("Years of Experience", 0, 50, value=parsed.get("Years of Experience", 0), step=1)
        location = st.selectbox("Location", list(location_map.keys()))
        age = st.number_input("Age", 18, 65, step=1)

# === Prediction Section ===
if st.session_state.mode and st.button("🔮 Predict Salary"):
    input_df = pd.DataFrame([{
        "Gender": gender,
        "Education Level": education,
        "General Title": title,
        "Seniority Level": seniority,
        "Years of Experience": experience,
        "Location": location,
        "Age": age
    }])

    # Encode and predict
    encoded_df = encode_inputs(input_df)
    prediction = model.predict(encoded_df)[0]
    st.success(f"💰 Estimated Salary: $ {int(prediction):,}")

    # Store & Download
    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append({**input_df.iloc[0].to_dict(), "Predicted Salary": int(prediction)})

    history_df = pd.DataFrame(st.session_state.history)
    csv = history_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Prediction(s)", csv, "predictions.csv", "text/csv")

# === Footer / About ===
st.markdown("---")
st.markdown("<h4 id='about'>👩‍💻 About Me</h4>", unsafe_allow_html=True)
st.markdown("""
Hi! I'm working on this salary prediction tool using machine learning and NLP techniques.

🔗 Connect with me:  
- [GitHub](https://github.com/skyish21)  
- [LinkedIn](https://https://www.linkedin.com/in/ishika-sharma-79a67a326/)
""")