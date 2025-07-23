import pickle
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Load model
model = pickle.load(open("model/salary_prediction_model.pkl", "rb"))

# LabelEncoders
le_gender = LabelEncoder()
le_gender.fit(['Female', 'Male'])

le_title = LabelEncoder()
le_title.fit(['Advisor', 'Analyst', 'Designer', 'Director', 'Engineer', 'Manager', 'Other', 'Scientist'])

# Encoding maps
education_map = {'High School': 0, 'Bachelor': 1, 'Master': 2, 'PhD': 3}
location_map = {'Rural': 0, 'Suburban': 1, 'Urban': 2}
seniority_map = {'Junior': 0, 'Mid': 1, 'Senior': 2, 'Lead': 3, 'Executive': 4}

def encode_inputs(df):
    df['Gender'] = le_gender.transform(df['Gender'])
    df['General Title'] = le_title.transform(df['General Title'])
    df['Education Level'] = df['Education Level'].map(education_map)
    df['Location'] = df['Location'].map(location_map)
    df['Seniority Level'] = df['Seniority Level'].map(seniority_map)
    return df
