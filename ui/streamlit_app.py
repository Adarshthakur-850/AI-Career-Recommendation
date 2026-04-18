import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="AI Career Recommender", layout="wide")

st.title("🚀 AI Career Recommendation System")
st.markdown("Enter your profile details below to get personalized career advice.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Profile")
    skills = st.text_area("Skills (comma separated)", "python, statistics, modeling")
    interests = st.text_area("Interests", "solving problems, ai")
    projects = st.text_area("Projects", "churn prediction model")
    education = st.selectbox("Education Level", ["Bachelor", "Master", "PhD", "Self-Taught"])
    experience = st.slider("Years of Experience", 0, 20, 2)
    
    if st.button("Predict Career Path"):
        payload = {
            "skills": skills,
            "interests": interests,
            "education_level": education,
            "years_experience": experience,
            "projects": projects
        }
        
        try:
            with st.spinner("Analyzing profile..."):
                response = requests.post(API_URL, json=payload)
                
            if response.status_code == 200:
                data = response.json()
                st.session_state['results'] = data['predictions']
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")

with col2:
    st.subheader("Recommendations")
    if 'results' in st.session_state:
        for res in st.session_state['results']:
            st.success(f"**{res['career']}** ({res['probability']*100:.1f}%)")
            st.markdown("**Learning Roadmap:**")
            for step in res['roadmap']:
                st.write(f"- {step}")
            st.divider()
    else:
        st.info("Results will appear here.")
