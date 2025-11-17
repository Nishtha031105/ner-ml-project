from textblob import TextBlob

def analyze_sentiment(text):
    """
    Analyze sentiment of text
    
    Returns:
        dict with sentiment info including polarity, subjectivity, and label
    """
    
    # Create TextBlob object
    blob = TextBlob(text)
    
    # Get polarity (-1 to 1, negative to positive)
    polarity = blob.sentiment.polarity
    
    # Get subjectivity (0 to 1, objective to subjective)
    subjectivity = blob.sentiment.subjectivity
    
    # Determine sentiment label
    if polarity > 0.1:
        label = "Positive"
        emoji = "😊"
    elif polarity < -0.1:
        label = "Negative"
        emoji = "😞"
    else:
        label = "Neutral"
        emoji = "😐"
    
    return {
        "polarity": round(polarity, 3),
        "subjectivity": round(subjectivity, 3),
        "label": label,
        "emoji": emoji,
        "description": get_sentiment_description(polarity, subjectivity)
    }

def get_sentiment_description(polarity, subjectivity):
    """Generate human-readable sentiment description"""
    
    # Polarity description
    if polarity > 0.5:
        pol_desc = "very positive"
    elif polarity > 0.1:
        pol_desc = "positive"
    elif polarity < -0.5:
        pol_desc = "very negative"
    elif polarity < -0.1:
        pol_desc = "negative"
    else:
        pol_desc = "neutral"
    
    # Subjectivity description
    if subjectivity > 0.6:
        subj_desc = "highly subjective (opinion-based)"
    elif subjectivity > 0.3:
        subj_desc = "somewhat subjective"
    else:
        subj_desc = "objective (fact-based)"
    
    return f"This text is {pol_desc} and {subj_desc}."

def analyze_entity_sentiment(text, entities):
    """
    Analyze sentiment around each entity
    
    Returns sentiment for text mentioning each entity
    """
    entity_sentiments = []
    
    for entity in entities:
        entity_text = entity["text"]
        
        # Find sentences containing this entity
        blob = TextBlob(text)
        sentences = blob.sentences
        
        entity_sentences = []
        for sentence in sentences:
            if entity_text in str(sentence):
                entity_sentences.append(str(sentence))
        
        # Analyze sentiment of those sentences
        if entity_sentences:
            combined_text = " ".join(entity_sentences)
            sentiment = TextBlob(combined_text).sentiment.polarity
            
            entity_sentiments.append({
                "entity": entity_text,
                "label": entity["label"],
                "sentiment": round(sentiment, 3),
                "sentiment_label": "Positive" if sentiment > 0.1 else "Negative" if sentiment < -0.1 else "Neutral"
            })
    
    return entity_sentiments