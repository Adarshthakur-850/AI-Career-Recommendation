import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

def train():
    # Load Data
    import os
    import sys
    
    # Calculate project root from this file's location
    # training/train_model.py -> .. -> project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..')
    data_path = os.path.join(project_root, 'data', 'careers_dataset.csv')
    
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print("Dataset not found. Running generation script...")
        
        # Add project root to path to find data module
        if project_root not in sys.path:
            sys.path.append(project_root)
            
        from data import generate_data
        df = generate_data.generate_data()
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        df.to_csv(data_path, index=False)

    # Feature Engineering
    # Combine text features into one column for TF-IDF
    df['text_features'] = df['skills'] + " " + df['interests'] + " " + df['projects']
    
    X = df[['text_features', 'education_level', 'years_experience']]
    y = df['target_career']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Preprocessing Pipeline
    # Text -> Tfidf
    # Education -> OneHot (or Ordinal)
    # Experience -> Passthrough (or Scaler)
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('text', TfidfVectorizer(max_features=500, stop_words='english'), 'text_features'),
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['education_level']),
            ('num', 'passthrough', ['years_experience'])
        ]
    )
    
    # Model Pipeline
    clf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    # Train
    print("Training model...")
    clf.fit(X_train, y_train)
    
    # Evaluate
    print("Evaluating model...")
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # Save
    models_dir = os.path.join(project_root, 'models')
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        
    joblib.dump(clf, os.path.join(models_dir, "career_model.pkl"))
    print(f"Model saved to {models_dir}/career_model.pkl")

if __name__ == "__main__":
    train()
