# Named Entity Recognition

Objective : To build a web application that automatically extracts and identifies named entities from text using advanced Natural Language Processing (NLP) and Machine Learning (ML) models. The system detects entities such as persons, organizations, locations, products, dates, monetary values, and provides analytics, sentiment analysis, contextual categorization, and multi-document processing.
Features: Text highlighting, entity aggregation, and multi-doc analysis. Backend uses spaCy and HuggingFace Transformers, for better performance across news, business, academic, and social media text.

---

### Entity Extraction
- People, organizations, countries, cities, dates, money, events, products, etc.
- Color-coded highlighting in extracted text
- Interactive sidebar with click-to-highlight feature

### Advanced Features
- **Sentiment Analysis**
- **Contextual Categorization** (e.g., grouping similar entities)
- **Analytical Dashboard** with charts & entity frequency
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


