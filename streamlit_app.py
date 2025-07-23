import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from resume_parser import extract_resume_text, parse_resume_features
import pickle


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
        with st.spinner("🔍 Parsing resume..."):
            resume_text = extract_resume_text(uploaded_file)
            parsed = parse_resume_features(resume_text)

        st.subheader("📋 Parsed Resume Info (Editable)")

        # --- Handle possible missing values ---
        try:
            gender_idx = ['Female', 'Male'].index(parsed.get("Gender", "Female"))
        except ValueError:
            gender_idx = 0

        try:
            edu_idx = list(education_map.keys()).index(parsed.get("Education Level", "Bachelor"))
        except ValueError:
            edu_idx = 1

        try:
            title_idx = list(le_title.classes_).index(parsed.get("General Title", "Other"))
        except ValueError:
            title_idx = list(le_title.classes_).index("Other")

        try:
            seniority_idx = list(seniority_map.keys()).index(parsed.get("Seniority Level", "Mid"))
        except ValueError:
            seniority_idx = 1

    # === Editable Fields ===
    gender = st.selectbox("Gender", ['Female', 'Male'], index=gender_idx)
    education = st.selectbox("Education Level", list(education_map.keys()), index=edu_idx)
    title = st.selectbox("General Title", list(le_title.classes_), index=title_idx)
    seniority = st.selectbox("Seniority Level", list(seniority_map.keys()), index=seniority_idx)
    experience = st.number_input("Years of Experience", 0, 50, value=parsed.get("Years of Experience", 0), step=1)
    location = st.selectbox("Location", list(location_map.keys()), index=0)
    age = st.number_input("Age", 18, 65, value=parsed.get("Age", 25), step=1)

    # === Predict Button ===
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

        # Encoding
        input_df['Gender'] = le_gender.transform(input_df['Gender'])
        input_df['General Title'] = le_title.transform(input_df['General Title'])
        input_df['Education Level'] = input_df['Education Level'].map(education_map)
        input_df['Location'] = input_df['Location'].map(location_map)
        input_df['Seniority Level'] = input_df['Seniority Level'].map(seniority_map)

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