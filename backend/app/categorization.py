# Categorization using keyword patterns (no ML models needed)


def categorize_text(text, entities=None):
    """
    Categorize text into topics using keyword matching

    Returns category and confidence scores
    """
    return quick_categorize(text, entities)


def get_entity_hints(entities):
    """
    Provide additional categorization hints based on entities
    """
    hints = []

    # Count entity types
    entity_counts = {}
    for ent in entities:
        label = ent["label"]
        entity_counts[label] = entity_counts.get(label, 0) + 1

    # Business indicators
    if entity_counts.get("ORG", 0) > 2 or entity_counts.get("MONEY", 0) > 0:
        hints.append("Contains business/financial entities")

    # Geographic/Travel indicators
    if entity_counts.get("GPE", 0) > 3 or entity_counts.get("LOC", 0) > 2:
        hints.append("Contains multiple geographic references")

    # Time-sensitive (news)
    if entity_counts.get("DATE", 0) > 2:
        hints.append("Contains temporal references (news/events)")

    # People-focused
    if entity_counts.get("PERSON", 0) > 3:
        hints.append("Focuses on multiple individuals")

    return hints


def quick_categorize(text, entities):
    """
    Faster keyword-based categorization (fallback)
    """
    text_lower = text.lower()

    # Keyword patterns
    patterns = {
        "Business & Finance": [
            "company",
            "business",
            "revenue",
            "profit",
            "ceo",
            "investment",
            "stock",
            "market",
            "financial",
        ],
        "Technology & Science": [
            "technology",
            "software",
            "ai",
            "research",
            "data",
            "algorithm",
            "computer",
            "science",
            "innovation",
        ],
        "Politics & Government": [
            "government",
            "president",
            "election",
            "political",
            "parliament",
            "minister",
            "policy",
            "law",
        ],
        "Sports & Entertainment": [
            "game",
            "player",
            "team",
            "match",
            "championship",
            "movie",
            "music",
            "celebrity",
        ],
        "Health & Medicine": [
            "health",
            "medical",
            "doctor",
            "patient",
            "hospital",
            "treatment",
            "disease",
            "medicine",
        ],
    }

    scores = {}
    for category, keywords in patterns.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            scores[category] = score

    if scores:
        primary = max(scores, key=scores.get)
        return {
            "primary_category": primary,
            "confidence": min(scores[primary] / 10, 0.95),
            "method": "keyword-based",
        }

    return {"primary_category": "General", "confidence": 0.5, "method": "default"}
