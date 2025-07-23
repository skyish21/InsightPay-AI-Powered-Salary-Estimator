import fitz  # PyMuPDF
import re

def extract_resume_text(pdf_path):
    try:
        doc = fitz.open(stream=pdf_path.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except:
        return "❌ Could not parse or extract the resume"
    
# Map General Title
def map_general_title(text):
    text = text.lower()
    job_titles = {
        "engineer": "Engineer",
        "developer": "Engineer",
        "analyst": "Analyst",
        "scientist": "Scientist",
        "manager": "Manager",
        "director": "Director",
        "consultant": "Advisor",
        "designer": "Designer"
    }
    for keyword, label in job_titles.items():
        if keyword in text:
            return label
    return "Other"

# Extract seniority
def extract_seniority(text):
    text = text.lower()
    if 'intern' in text or 'entry level' in text or 'junior' in text:
        return 'Junior'
    elif 'senior' in text:
        return 'Senior'
    elif any(x in text for x in ['lead', 'principal', 'head']):
        return 'Lead'
    elif any(x in text for x in ['director', 'vp', 'chief', 'ceo', 'cto']):
        return 'Executive'
    else:
        return 'Mid'

    
def parse_resume_features(text):

    text = text.lower()
    
    # Education Level Guess
    if "master" in text or "m.sc" in text or "m.tech" in text:
        education = "Master"
    elif "high school" in text:
        education = "High School"
    elif "bachelor" in text or "b.sc" in text or "b.tech" in text:
        education = "Bachelor"
    elif "phd" in text or "ph.d" in text:
        education = "PhD"
    else:
        education = None

    # Years of Experience Guess
    exp_match = re.findall(r'(\d+)\+?\s*(?:years|yrs|year)', text.lower())
    experience = int(exp_match[0]) if exp_match else 0

    # Gender 
    if "she/her" in text or "ms." in text or "female" in text:
        gender = "Female"
    elif "he/him" in text or "mr." in text or "male" in text:
        gender = "Male"
    else:
        gender = None

    return {
        "Age": None,  # Always ask for Age
        "Gender": gender,
        "Education Level": education,
        "General Title": map_general_title(text),
        "Seniority Level": extract_seniority(text),
        "Years of Experience": experience,
        "Location": None  # Always ask for Location
    }