# Named Entity Recognition Tool

A web-based application for automatically extracting and identifying named entities from text using Natural Language Processing. The system recognizes people, organizations, locations, dates, monetary values, and other key information from unstructured text.

## Overview

This tool provides an intuitive interface for performing Named Entity Recognition (NER) on any text input. Users can paste text or upload documents, and the system will automatically identify and categorize important entities, displaying them with visual highlights and providing detailed analytics.

The application uses state-of-the-art NLP models to achieve high accuracy across different text types, including news articles, business documents, social media content, and academic papers.

## Features

The application can identify multiple entity types including persons, organizations, locations, dates, monetary amounts, facilities, products, and events.
It also analyzes text instantly as it is entered or pasted,and give immidiate feedback and result.

## Technology Stack

### Backend
- FastAPI for creating a modern, high-performance API
- spaCy or Hugging Face Transformers for NLP and entity recognition
- Uvicorn as the ASGI server
- Python 3.10 or higher

### Frontend
- React 18 for building the user interface
- Vite as the build tool and development server
- Tailwind CSS for styling
- Axios for making API requests

## Prerequisites
Before setting up the project, ensure you have installed python, nodejs, npm, git.

## Installation and Setup

### Clone the Repository
run following commands in bash:
```bash
git clone https://github.com/YOUR_USER_NAME/ner-ml-project.git
cd ner-ml-project
```

### Backend Setup
create a folder name backend in your main repo.

```bash
cd backend
```
To create virtual environment, run:
```bash
python -m venv venv
```
```bash
source venv/bin/activate
```
```bash
pip install -r requirements.txt
```
Download any one NER Model:
smaller version:
```bash
python -m spacy download en_core_web_sm
```
larger version:
```bash
python -m spacy download en_core_web_trf
```
start backend server on prot 8000:
```bash
uvicorn app.main:app --reload --port 8000
```
backend is running at:  http://localhost:8000

verify server status at: http://localhost:8000/health in your browser.

### Frontend Setup

create a folder name forntend in your main repo.
```bash
cd frontend
```
```bash
npm install
```
```bash
npm run dev
```

Application  will be running at: http://localhost:5173

### Basic Usage

1. Open the application in your browser at http://localhost:5173

2. Enter or paste text into the text area. You can also click one of the sample text buttons to load pre-written examples.

3. Click the "Analyze Text" button to process the text.

4. View the results with color-coded entity highlights in the main panel and a detailed entity list in the sidebar.

5. Click on any entity in the sidebar to highlight all occurrences of that entity in the text.

### Entity Types

Followig types of entities can be detected using this model:
- **PERSON**: Names of people, including both real and fictional characters
- **ORG**: Organizations such as companies, government agencies, and institutions
- **GPE**: Geopolitical entities like countries, cities, and states
- **LOC**: Non-geopolitical locations including mountain ranges, bodies of water, and regions
- **FAC**: Facilities such as buildings, airports, highways, and bridges
- **PRODUCT**: Physical objects including vehicles, foods, and consumer goods
- **EVENT**: Named events including wars, battles, sports events, and natural disasters
- **WORK_OF_ART**: Titles of books, songs, movies, and other creative works
- **LAW**: Named legal documents and laws
- **LANGUAGE**: Any named language
- **DATE**: Dates and time periods in various formats
- **TIME**: Times of day or durations shorter than a day
- **PERCENT**: Percentage values including the percent symbol
- **MONEY**: Monetary amounts including currency symbols
- **QUANTITY**: Measurements of weight, distance, and other quantities
- **ORDINAL**: Ordinal numbers such as first, second, third
- **CARDINAL**: Cardinal numbers that do not fall under other categories

## Training Custom Models

If you want to train a custom NER model on your own data:

### Downloading Datasets

The project includes scripts for downloading common NER datasets:
```bash
cd backend
python download_dataset.py
```
This will prompt you to choose from available datasets such as CoNLL-2003 or WNUT-17 or ONTO.

### Training Process
To train model:
```bash
python train_model.py
```

Trained model will be saved to the `custom_ner_model` directory.

### Using Your Custom Model

To use your trained model, update the model loading code in `backend/app/main.py`:
```python
nlp = spacy.load("./custom_ner_model")
```

Then restart the backend server.
