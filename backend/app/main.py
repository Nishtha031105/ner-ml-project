from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.sentiment import analyze_sentiment, analyze_entity_sentiment
from app.categorization import categorize_text, quick_categorize
from app.file_processor import extract_text_from_file, process_multiple_documents
import spacy

# Create the app
app = FastAPI()

# Allow frontend to talk to backend (fixes connection errors)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load spacy model for NER
try:
    nlp = spacy.load("./custom_ner_model")
except OSError:
    nlp = spacy.load("en_core_web_sm")

# Categorization and sentiment models are lazy-loaded on first use


# Define what data we expect to receive
class TextInput(BaseModel):
    text: str


# The main function - receives text, returns entities
@app.post("/analyze")
def analyze_text(input_data: TextInput):
    # Run AI on the text
    doc = nlp(input_data.text)

    # Extract all entities (names, places, etc.)
    entities = []
    for ent in doc.ents:
        entities.append(
            {
                "text": ent.text,  # The actual word/phrase
                "label": ent.label_,  # Type (PERSON, ORG, etc.)
                "start": ent.start_char,  # Where it starts in text
                "end": ent.end_char,  # Where it ends
            }
        )

    # Count how many of each type
    counts = {}
    for ent in entities:
        label = ent["label"]
        counts[label] = counts.get(label, 0) + 1

    # Sentiment analysis
    sentiment = analyze_sentiment(input_data.text)

    # Anayse sentiment per entity
    entity_sentiments = analyze_entity_sentiment(input_data.text, entities)

    # Categorization.
    try:
        if len(input_data.text) < 1000:
            category_result = categorize_text(input_data.text, entities)
        else:
            category_result = quick_categorize(input_data.text, entities)
    except Exception as e:
        print(f"Categorization error: {e}")
        category_result = quick_categorize(input_data.text, entities)

    return {
        "entities": entities,
        "counts": counts,
        "total_entities": len(entities),
        "sentiment": sentiment,
        "entity_sentiments": entity_sentiments,
        "category": category_result,
    }


@app.post("/analyze-file")
async def analyze_file(file: UploadFile = File(...)):
    """
    Analyze a single uploaded file
    """
    try:
        # Read file content
        content = await file.read()

        # Extract text
        text = extract_text_from_file(content, file.filename)

        if not text or len(text) < 10:
            return {"error": "Could not extract text from file or file is too short"}

        # Analyze the extracted text (same as /analyze endpoint)
        doc = nlp(text)

        entities = []
        for ent in doc.ents:
            entities.append(
                {
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char,
                }
            )

        counts = {}
        for ent in entities:
            label = ent["label"]
            counts[label] = counts.get(label, 0) + 1

        sentiment = analyze_sentiment(text)
        entity_sentiments = analyze_entity_sentiment(text, entities)

        try:
            category_result = quick_categorize(text, entities)
        except:
            category_result = {"primary_category": "Unknown", "confidence": 0}

        return {
            "filename": file.filename,
            "text": text,
            "entities": entities,
            "counts": counts,
            "total_entities": len(entities),
            "sentiment": sentiment,
            "entity_sentiments": entity_sentiments,
            "category": category_result,
        }

    except Exception as e:
        return {"error": str(e)}


@app.post("/analyze-multiple-files")
async def analyze_multiple_files(files: list[UploadFile] = File(...)):
    """
    Analyze multiple uploaded files
    """
    results = []

    for file in files:
        try:
            content = await file.read()
            text = extract_text_from_file(content, file.filename)

            if not text or len(text) < 10:
                results.append(
                    {
                        "filename": file.filename,
                        "status": "error",
                        "error": "Could not extract text or file too short",
                    }
                )
                continue

            # Analyze
            doc = nlp(text)

            entities = []
            for ent in doc.ents:
                entities.append(
                    {
                        "text": ent.text,
                        "label": ent.label_,
                    }
                )

            counts = {}
            for ent in entities:
                label = ent["label"]
                counts[label] = counts.get(label, 0) + 1

            sentiment = analyze_sentiment(text[:500])  # Use first 500 chars for speed
            category_result = quick_categorize(text, entities)

            results.append(
                {
                    "filename": file.filename,
                    "status": "success",
                    "text_preview": text[:200] + "..." if len(text) > 200 else text,
                    "text_length": len(text),
                    "entities": entities[:10],  # First 10 entities
                    "total_entities": len(entities),
                    "counts": counts,
                    "sentiment": sentiment,
                    "category": category_result,
                }
            )

        except Exception as e:
            results.append(
                {"filename": file.filename, "status": "error", "error": str(e)}
            )

    return {
        "total_files": len(files),
        "successful": sum(1 for r in results if r.get("status") == "success"),
        "failed": sum(1 for r in results if r.get("status") == "error"),
        "results": results,
    }


# Health check - to test if server is running
@app.get("/health")
def health():
    return {"status": "healthy"}
