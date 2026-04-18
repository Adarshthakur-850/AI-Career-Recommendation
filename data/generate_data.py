import pandas as pd
import random

def generate_data(num_samples=1000):
    careers = {
        "Data Scientist": {
            "skills": ["python", "machine learning", "statistics", "sql", "pandas", "numpy", "deep learning", "nlp"],
            "interests": ["analyzing data", "building models", "solving complex problems", "ai research"],
            "projects": ["customer churn prediction", "image classification", "sentiment analysis"]
        },
        "Web Developer": {
            "skills": ["html", "css", "javascript", "react", "node.js", "databases", "api"],
            "interests": ["building websites", "ui design", "frontend development", "backend systems"],
            "projects": ["e-commerce site", "portfolio website", "chat application"]
        },
        "Software Engineer": {
            "skills": ["java", "c++", "python", "algorithms", "data structures", "system design", "git"],
            "interests": ["software architecture", "coding", "optimizing performance", "backend logic"],
            "projects": ["scalable system", "desktop application", "algorithm visualizer"]
        },
        "Product Manager": {
            "skills": ["communication", "agile", "scrum", "market research", "roadmapping", "analytics"],
            "interests": ["product strategy", "user experience", "leading teams", "business growth"],
            "projects": ["product launch", "market analysis", "user research"]
        },
        "UX Designer": {
            "skills": ["figma", "sketch", "prototyping", "user research", "wireframing", "adobe xd"],
            "interests": ["user interface", "design capability", "user testing", "visual design"],
            "projects": ["mobile app design", "website redesign", "user flow diagram"]
        }
    }

    data = []
    
    for _ in range(num_samples):
        career = random.choice(list(careers.keys()))
        profile = careers[career]
        
        # Sample random subset of skills and interests to make it realistic
        skills = ", ".join(random.sample(profile["skills"], k=random.randint(3, len(profile["skills"]))))
        interests = ", ".join(random.sample(profile["interests"], k=random.randint(2, len(profile["interests"]))))
        projects = ", ".join(random.sample(profile["projects"], k=1))
        
        education = random.choice(["Bachelor", "Master", "PhD", "Self-Taught"])
        experience = random.randint(0, 10)
        certifications = random.choice(["Certified", "None", "In Progress"])
        
        data.append([skills, interests, education, experience, certifications, projects, career])
        
    df = pd.DataFrame(data, columns=["skills", "interests", "education_level", "years_experience", "certifications", "projects", "target_career"])
    return df

if __name__ == "__main__":
    df = generate_data()
    df.to_csv("data/careers_dataset.csv", index=False)
    print("Dataset generated at data/careers_dataset.csv")
