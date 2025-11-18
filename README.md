# Named Entity Recognition

A full-stack web application that automatically extracts and identifies named entities from text using advanced Natural Language Processing (NLP) and Machine Learning (ML) models. The system detects entities such as persons, organizations, locations, products, dates, monetary values, and provides analytics, sentiment analysis, contextual categorization, and multi-document processing.

---

**Advanced Named Entity Recognition and Text Analytics Tool**

### Objective
To build an easy-to-use, real-time, web-based NER system that:
- Automatically extracts entities from unstructured text
- Works on both text input and uploaded documents
- Provides contextual insights, sentiment analysis, and an analytical dashboard
- Enables non-technical users to perform NLP tasks without coding
- Achieves high accuracy and fast response using spaCy and Transformer-based models

---

This tool provides an intuitive interface to perform Named Entity Recognition (NER) on any text. Users can:

✔ Paste text or upload documents  
✔ Analyze sentiment  
✔ View entity categories and counts  
✔ Compare multiple documents  
✔ Explore insights using the dashboard

It supports real-time highlighting, side-panel entity aggregation, and multi-document analysis. The backend uses spaCy and HuggingFace Transformers, giving state-of-the-art performance across news, business, academic, and social media text.

---

### Entity Extraction
- People, organizations, countries, cities, dates, money, events, products, etc.
- Color-coded highlighting in extracted text
- Interactive sidebar with click-to-highlight feature

### Advanced Features
- **Sentiment Analysis**
- **Contextual Categorization** (e.g., grouping similar entities)
- **Analytical Dashboard** with charts & entity frequency
- **Multi-Document Support** for batch analysis
- **Document Upload** (PDF/text)
- **Model Switching** (spaCy small / Transformer model)

---

### Backend
- Python 3.10+
- FastAPI
- spaCy NER / HuggingFace Transformers
- Uvicorn

### Frontend
- React 18
- Vite
- Tailwind CSS
- Axios

### Prerequisites
Install: Python, Node.js, npm, Git

---

## Setup

### 1. Clone Repo
```bash
git clone https://github.com/YOUR_USER_NAME/ner-ml-project.git
cd ner-ml-project
```

### 2. Backend
```bash
mkdir backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Download a NER Model

**Small Model:**
```bash
python -m spacy download en_core_web_sm
```

**Transformer Model:**
```bash
python -m spacy download en_core_web_trf
```

### 4. Start Backend
```bash
uvicorn app.main:app --reload --port 8000
```

- **Backend URL:** http://localhost:8000
- **Health check:** http://localhost:8000/health

### 5. Frontend
```bash
cd ../frontend
mkdir frontend (if not there)
cd frontend
npm install
npm run dev
```

- **App URL:** http://localhost:5173

---

## Datasets

### CoNLL-2003
- Entity types: PERSON, ORG, LOC, MISC

### WNUT-17
- 3,394 social media texts
- Noisy, real-world anomalies
- Useful for informal language

### OntoNotes 5.0
- Large, multi-genre corpus
- 18 entity categories

---

## Model

### NER Pipeline
1. Tokenization
2. Feature representation
3. Named Entity Recognition
4. Post-processing
5. JSON output

### Models

#### spaCy en_core_web_sm
- Fast, lightweight
- Suitable for real-time UI

#### spaCy transformer en_core_web_trf
- BERT/RoBERTa-based
- Higher accuracy (~91% F1)
- Higher latency

### Custom Model Use
```python
nlp = spacy.load("./custom_ner_model")
```

---

## Result

### Performance Metrics

| Model | Precision | Recall | F1 Score | Latency |
|-------|-----------|--------|----------|---------|
| spaCy small | 89% | 90% | 89.5% | 120 ms |
| Transformer | 92% | 91% | 91.5% | 430 ms |

### Achievements
- ~90% F1 Score
- <500 ms average latency
- Supports documents up to 10k words
---


