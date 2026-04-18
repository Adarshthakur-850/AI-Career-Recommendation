import spacy

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    """
    Extracts potential skills from text using simple NLP rules (Noun Chunks / Entities).
    In a real system, this would use a dedicated Entity Ruler with a skill list.
    For this prototype, we rely on tokenization and basic filtering.
    """
    doc = nlp(text.lower())
    
    # Simple strategy: Extract nouns and proper nouns, plus known keywords
    # Ideally, we matches against a known skill database
    
    skills = []
    
    # Common tech skills keywords to look for specifically
    tech_keywords = {
        "python", "java", "c++", "javascript", "html", "css", "sql", "react", "node.js",
        "machine learning", "deep learning", "nlp", "statistics", "data analysis",
        "communication", "management", "leadership", "agile", "scrum", "design", "figma",
        "aws", "azure", "docker", "kubernetes", "git"
    }
    
    # 1. Direct Keyword Matching
    for token in doc:
        if token.text in tech_keywords:
            skills.append(token.text)
            
    # 2. Noun Chunks for multi-word skills (e.g., "machine learning")
    for chunk in doc.noun_chunks:
        if chunk.text in tech_keywords:
            skills.append(chunk.text)

    return list(set(skills))
