import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
import random
import json
from pathlib import Path


def load_training_data(file_path):
    """Load training data from JSON file"""
    print(f"📥 Loading training data from {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✅ Loaded {len(data)} training examples")
    return data


def convert_to_spacy_format(training_data):
    """Convert our format (text + [start,end,label]) to spaCy's format"""
    spacy_data = []
    for item in training_data:
        entities = []
        for start, end, label in item["entities"]:
            entities.append((start, end, label))
        spacy_data.append((item["text"], {"entities": entities}))
    return spacy_data


def print_spacy_model_summary(nlp):
    """Print a simple summary of the spaCy NER architecture."""
    print("\n🧠 MODEL ARCHITECTURE SUMMARY")
    print("============================================================")

    # Pipeline info
    print(f"Pipeline components: {nlp.pipe_names}")

    # Tok2Vec (CNN encoder) – for blank models it's often embedded, not a separate pipe
    if "tok2vec" in nlp.pipe_names:
        tok2vec = nlp.get_pipe("tok2vec")
        print("\n🔹 Tok2Vec (CNN Encoder):")
        try:
            print(f"  • Model name: {getattr(tok2vec, 'name', 'tok2vec')}")
            print(f"  • Config: {tok2vec.model.cfg}")
        except Exception:
            print("  • Tok2Vec config not available in this version.")
    else:
        print("\n🔹 Tok2Vec: Not found as a separate component "
              "(for blank models, tok2vec is usually embedded in the NER model).")

    # NER classifier
    if "ner" in nlp.pipe_names:
        ner = nlp.get_pipe("ner")
        print("\n🔹 NER Classifier:")
        print(f"  • Labels: {ner.labels}")
        try:
            print(f"  • Model config: {ner.model.cfg}")
        except Exception:
            print("  • NER model config not available in this version.")
    else:
        print("\n🔹 NER Classifier: Not added yet (will be created during setup).")

    print("============================================================\n")


def train_ner_model(training_data, output_dir="./custom_ner_model", n_iter=30, sample_size=None):
    """Train custom NER model
    
    Args:
        training_data: List of training examples (our JSON format)
        output_dir: Where to save the model
        n_iter: Number of training iterations
        sample_size: If set, use only this many examples (for faster training)
    """
    print("\n" + "=" * 70)
    print("🚀 STARTING TRAINING PROCESS")
    print("=" * 70)

    # Sample data if requested (useful for quick tests)
    if sample_size and sample_size < len(training_data):
        print(f"\n⚠️  Using {sample_size} examples (out of {len(training_data)}) for faster training")
        training_data = random.sample(training_data, sample_size)

    # Create a blank English model
    print("\n📝 Creating blank spaCy model...")
    nlp = spacy.blank("en")

    # Create NER component
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner")
    else:
        ner = nlp.get_pipe("ner")

    # Collect all unique labels
    print("\n🏷️  Analyzing entity labels...")
    labels = set()
    for item in training_data:
        for start, end, label in item["entities"]:
            labels.add(label)
            ner.add_label(label)

    print(f"   Found {len(labels)} entity types: {sorted(labels)}")

    # Now that NER exists and labels are added, print architecture summary
    print_spacy_model_summary(nlp)

    # Convert to spaCy (text, {"entities": [...]}) format
    print("\n🔄 Converting data to spaCy format...")
    spacy_data = convert_to_spacy_format(training_data)

    # Train / validation split (90% train, 10% dev)
    split_ratio = 0.9
    split_index = max(1, int(len(spacy_data) * split_ratio))
    train_data = spacy_data[:split_index]
    dev_data = spacy_data[split_index:]

    print(f"\n📊 Using {len(train_data)} examples for training and {len(dev_data)} for validation.\n")

    # Initialize training
    nlp.begin_training()

    # Prepare dev examples for evaluation (if we have any)
    if dev_data:
        dev_examples = [
            Example.from_dict(nlp.make_doc(text), annotations)
            for text, annotations in dev_data
        ]
    else:
        dev_examples = []
        print("⚠️ Not enough data for validation set; skipping validation metrics.\n")

    # Training
    print(f"\n📚 Training for {n_iter} iterations...")
    print(f"   Dataset size: {len(train_data)} examples")
    print(f"   This may take 10-30 minutes depending on your computer...\n")

    for iteration in range(n_iter):
        random.shuffle(train_data)
        losses = {}

        # Create batches
        batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))

        for batch in batches:
            examples = []
            for text, annotations in batch:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                examples.append(example)

            # Update model
            nlp.update(examples, drop=0.5, losses=losses)

        # Per-epoch loss
        print(f"   ✓ Iteration {iteration + 1:2d}/{n_iter} - Loss: {losses.get('ner', 0):8.2f}")

        # Per-epoch Precision / Recall / F1 on validation set
        if dev_examples:
            scores = nlp.evaluate(dev_examples)
            ents_p = scores.get("ents_p", 0.0)
            ents_r = scores.get("ents_r", 0.0)
            ents_f = scores.get("ents_f", 0.0)
            print(
                f"      🔍 Epoch {iteration + 1:2d}: "
                f"Precision={ents_p:.2f} | Recall={ents_r:.2f} | F1={ents_f:.2f}"
            )

    # Final evaluation summary
    if dev_examples:
        print("\n📊 FINAL EVALUATION ON VALIDATION SET")
        final_scores = nlp.evaluate(dev_examples)
        print(
            f"   Precision: {final_scores['ents_p']:.2f} | "
            f"Recall: {final_scores['ents_r']:.2f} | "
            f"F1-score: {final_scores['ents_f']:.2f}"
        )

    # Simple model summary
    print("\n🧠 MODEL SUMMARY")
    print("   Pipeline components:", nlp.pipe_names)
    ner_pipe = nlp.get_pipe("ner")
    print("   NER labels:", ner_pipe.labels)

    # Save model
    print(f"\n💾 Saving model to {output_dir}...")
    output_path = Path(output_dir)
    if not output_path.exists():
        output_path.mkdir(parents=True)

    nlp.to_disk(output_path)
    print("   ✅ Model saved successfully!")

    # Test the model
    print("\n🧪 TESTING THE TRAINED MODEL")
    print("=" * 70)

    test_texts = [
        "Nishtha Sharma works at Microsoft in Pune, India.",
        "Elon Musk founded SpaceX in California in 2002.",
        "Apple CEO Tim Cook announced new products in Cupertino.",
        "The European Union imposed sanctions on Russia.",
        "Amazon acquired Whole Foods for $13.7 billion."
    ]

    for text in test_texts:
        doc = nlp(text)
        print(f"\n📝 Text: {text}")
        if doc.ents:
            print("   Entities found:")
            for ent in doc.ents:
                print(f"      • {ent.text:20s} → {ent.label_}")
        else:
            print("   ⚠️  No entities detected")

    print("\n" + "=" * 70)
    print("🎉 TRAINING COMPLETE!")
    print("=" * 70)
    print(f"\nYour model is ready at: {output_dir}")
    print("\nNext steps:")
    print("1. Update main.py to load this model")
    print("2. Restart your backend server")
    print("3. Test in your web app!")
    print("=" * 70)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("           CUSTOM NER MODEL TRAINING")
    print("=" * 70)

    # Check which datasets are available
    conll_exists = Path("conll2003_training_data.json").exists()
    wnut_exists = Path("wnut17_training_data.json").exists()
    ontonotes_exists = Path("ontonotes_training_data.json").exists()

    if not conll_exists and not wnut_exists and not ontonotes_exists:
        print("\n❌ ERROR: No training data found!")
        print("   Please run download_dataset.py first to download CoNLL-2003 or WNUT-17")
        exit(1)

    print("\nAvailable datasets:")
    if conll_exists:
        print("  1. CoNLL-2003 (conll2003_training_data.json)")
    if wnut_exists:
        print("  2. WNUT-17 (wnut17_training_data.json)")
    if ontonotes_exists:
        print("  3. OntoNotes 5.0 (ontonotes_training_data.json)")

    # Choose dataset
    if conll_exists and wnut_exists and ontonotes_exists:
        choice = input("\nWhich dataset to use? (1/2/3): ").strip()
        if choice == "1":
            data_file = "conll2003_training_data.json"
        elif choice == "2":
            data_file = "wnut17_training_data.json"
        elif choice == "3":
            data_file = "ontonotes_training_data.json"
        else:
            data_file = "conll2003_training_data.json"
            print(f"\n   Invalid choice, defaulting to: {data_file}")
    elif conll_exists:
        data_file = "conll2003_training_data.json"
        print(f"\n   Using: {data_file}")
    elif wnut_exists:
        data_file = "wnut17_training_data.json"
        print(f"\n   Using: {data_file}")
    else:
        data_file = "ontonotes_training_data.json"
        print(f"\n   Using: {data_file}")

    # Load data
    training_data = load_training_data(data_file)

    # Ask about sample size
    print(f"\nFull dataset has {len(training_data)} examples.")
    print("Training options:")
    print("  1. Quick training (1000 examples, ~5 minutes) - Good for testing")
    print("  2. Medium training (5000 examples, ~15 minutes) - Balanced")
    print("  3. Full training (all examples, ~30 minutes) - Best accuracy")

    train_choice = input("\nChoose option (1/2/3): ").strip()

    if train_choice == "1":
        sample_size = min(1000, len(training_data))
        n_iter = 20
    elif train_choice == "2":
        sample_size = min(5000, len(training_data))
        n_iter = 25
    else:
        sample_size = None
        n_iter = 30

    # Train model
    train_ner_model(training_data, sample_size=sample_size, n_iter=n_iter)
