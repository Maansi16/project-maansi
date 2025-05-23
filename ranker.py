import spacy
import os
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''.join(page.extract_text() for page in reader.pages if page.extract_text())
    return text

def preprocess(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return ' '.join(tokens)

def rank_resumes(job_desc_text, resume_folder='resumes'):
    job_desc_processed = preprocess(job_desc_text)
    resumes = []
    texts = [job_desc_processed]
    filenames = []

    for filename in os.listdir(resume_folder):
        if filename.endswith('.pdf'):
            path = os.path.join(resume_folder, filename)
            raw_text = extract_text_from_pdf(path)
            processed_text = preprocess(raw_text)
            texts.append(processed_text)
            filenames.append(filename)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts)
    scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    ranked = sorted(zip(filenames, scores), key=lambda x: x[1], reverse=True)
    return ranked
