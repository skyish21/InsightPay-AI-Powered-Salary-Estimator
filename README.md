# InsightPay 💰 — AI-Powered Salary Estimator

This project is an interactive **Streamlit** web app that predicts an individual's salary based on their job-related information or uploaded resume. It uses **machine learning** models and **natural language processing (NLP)** to extract and encode key features from resumes.

**Streamlit App**

https://salary-prediction-liknwwrgipqk898ad7ky9x.streamlit.app/

---

## 🚀 Features

- 🔢 Predict salary using:
  1. Manual input fields
  2. Uploaded resume (PDF)
  3. Built-in sample resumes to test the app
- 🧠 NLP-based parsing of resumes (via PyMuPDF or PDFMiner)
- 🧮 Machine Learning model trained on structured salary data
- 🧾 Download prediction history as CSV
- 🎯 Clean UI with sidebar help and session state tracking
- 📎 About Me section with links to GitHub & LinkedIn

---

## 📈 Model Info
The model was trained on synthetic salary data using categorical and numeric features like:

- Gender
- Education
- Job Title
- Seniority
- Experience
- Location
- Age

## 📂 Project Structure

```bash
salary-prediction-app/
│
├── streamlit_app.py # Main app logic
├── resume_parser.py # Resume parsing and feature extraction
├── salary_prediction_model.pkl # Pre-trained ML model
├── requirements.txt # Python dependencies
├── sample_resumes/
│ ├── resume_data.pdf
│ ├── resume_engineer.pdf
│ ├── resume_manager.pdf
│ ├── resume_scientist.pdf
│ └── resume_intern.pdf
└── README.md # Project overview
```

---

## 🧪 Tech Stack

- **Frontend/UI**: Streamlit
- **ML Model**: Trained using scikit-learn
- **PDF Parsing**: PyMuPDF (fitz) / PDFMiner
- **Encoders**: LabelEncoder, custom mapping
- **Language**: Python 3.8+

---

## 📦 Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/salary-prediction-app.git
   cd salary-prediction-app
   ~~~

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the app**
```bash
streamlit run streamlit_app.py
```

## 📚 Sample Resume Testing

The app provides a dropdown to test 5 sample resumes:

- Junior Engineer
- Data Analyst
- Project Manager
- Senior Data Scientist
- Intern

These help showcase resume parsing and prediction without needing your own file.
