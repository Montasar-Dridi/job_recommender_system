# job_recommender/text_preprocessing.py

import re
import spacy

# Load the spaCy English model (run: python -m spacy download en_core_web_sm if not already downloaded)
nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    """
    Clean extracted text by removing noise (headers, footers, extra formatting).
    """
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        # Remove lines that look like page numbers or headers
        if re.match(r'^\s*(page\s*\d+|\d+)\s*$', line.lower()):
            continue
        line = re.sub(r'[-_]{2,}', '', line)
        cleaned_lines.append(line.strip())
    cleaned_text = "\n".join(cleaned_lines)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text

def preprocess_text(text: str) -> (str, list):
    """
    Preprocess text: cleaning, lemmatization, and named entity recognition.
    
    Returns:
      - normalized (lemmatized) text
      - list of extracted entities (as tuples of (text, label))
    """
    cleaned = clean_text(text)
    doc = nlp(cleaned)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    normalized_text = " ".join(tokens)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return normalized_text, entities
