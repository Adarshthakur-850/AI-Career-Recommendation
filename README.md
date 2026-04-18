# AI Career Recommendation System

A Machine Learning powered application that suggests career paths based on user skills and interests.

## Features
- **NLP Skill Extraction**: Uses spaCy to analyze profile text.
- **ML Classification**: Predicts career paths (Data Scientist, Web Dev, etc.) using RandomForest.
- **Career Roadmap**: Provides learning resources for predicted careers.
- **Interactive UI**: Built with Streamlit.
- **REST API**: Built with FastAPI.

## Installation

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    ```

2.  Run the application (see Walkthrough for detailed steps).

## Project Structure
- `data/`: Dataset generation and CSV.
- `nlp/`: Skill extraction logic.
- `training/`: Model training script.
- `models/`: Saved ML models.
- `api/`: FastAPI backend.
- `ui/`: Streamlit frontend.
