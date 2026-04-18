from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import sys
import os

import sys
import os

# Add project root to path to import nlp.skill_extractor
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)

from nlp import skill_extractor

app = FastAPI(title="AI Career Recommender")

# Load Model
model_path = os.path.join(project_root, 'models', 'career_model.pkl')

try:
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        print(f"Model loaded successfully from {model_path}")
    else:
        print(f"Model file not found at {model_path}")
        model = None
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

class UserProfile(BaseModel):
    skills: str
    interests: str
    education_level: str
    years_experience: int
    projects: str

# Static Roadmaps (Simplified for demo)
roadmaps = {
    "Data Scientist": ["Learn Python & SQL", "Master Machine Learning Algorithms", "Deep Learning & NLP", "Build Portfolio Projects"],
    "Web Developer": ["HTML/CSS/JS Basics", "React or Vue framework", "Backend with Node.js/Python", "Database Management"],
    "Software Engineer": ["Data Structures & Algorithms", "System Design", "Advanced Python/Java/C++", "Cloud Computing"],
    "Product Manager": ["Agile Methodologies", "User Research", "Data Analytics", "Product Strategy"],
    "UX Designer": ["Design Principles", "Figma/Sketch Mastery", "User Testing", "Prototyping"]
}

@app.post("/predict")
def predict_career(profile: UserProfile):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
        
    # extract skills if needed, but model uses raw text features
    # we can use extracted skills to Augment the input or for recommendation logic
    extracted = skill_extractor.extract_skills(profile.skills + " " + profile.projects)
    
    # Prepare input dataframe
    text_features = profile.skills + " " + profile.interests + " " + profile.projects
    
    input_data = pd.DataFrame({
        'text_features': [text_features],
        'education_level': [profile.education_level],
        'years_experience': [profile.years_experience]
    })
    
    # Predict Probabilities
    probas = model.predict_proba(input_data)[0]
    classes = model.classes_
    
    # Get Top 3
    top3_indices = probas.argsort()[-3:][::-1]
    top3_careers = []
    
    for idx in top3_indices:
        career = classes[idx]
        prob = probas[idx]
        roadmap = roadmaps.get(career, ["General Learning Path"])
        
        top3_careers.append({
            "career": career,
            "probability": float(prob),
            "roadmap": roadmap,
            "extracted_skills": extracted
        })
        
    return {"predictions": top3_careers}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
