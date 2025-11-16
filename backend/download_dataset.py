from datasets import load_dataset
import json

def convert_conll2003_to_spacy():
    """Download CoNLL-2003 and convert to spaCy format"""
    
    print("📥 Downloading CoNLL-2003 dataset...")
    print("(This may take 2-3 minutes on first download)\n")
    
    # Load dataset
    dataset = load_dataset("lhoestq/conll2003")
    
    # Get training split
    train_data = dataset["train"]
    
    print(f"✅ Downloaded {len(train_data)} training examples")
    
    # Label mapping
    label_map = {
        0: "O",      # Outside entity
        1: "B-PER",  # Beginning of Person
        2: "I-PER",  # Inside Person
        3: "B-ORG",  # Beginning of Organization
        4: "I-ORG",  # Inside Organization
        5: "B-LOC",  # Beginning of Location
        6: "I-LOC",  # Inside Location
        7: "B-MISC", # Beginning of Miscellaneous
        8: "I-MISC"  # Inside Miscellaneous
    }
    
    # Convert to our format
    print("\n🔄 Converting to spaCy format...")
    training_data = []
    
    for idx, example in enumerate(train_data):
        tokens = example["tokens"]
        ner_tags = example["ner_tags"]
        
        # Reconstruct text from tokens
        text = " ".join(tokens)
        
        # Extract entities
        entities = []
        current_entity = None
        char_position = 0
        
        for token, tag in zip(tokens, ner_tags):
            tag_label = label_map[tag]
            
            # Start of new entity
            if tag_label.startswith("B-"):
                # Save previous entity if exists
                if current_entity:
                    entities.append(current_entity)
                
                # Start new entity
                entity_type = tag_label[2:]  # Remove "B-"
                current_entity = [char_position, char_position + len(token), entity_type]
            
            # Continuation of entity
            elif tag_label.startswith("I-") and current_entity:
                # Extend current entity end position
                current_entity[1] = char_position + len(token)
            
            # Outside entity
            else:
                if current_entity:
                    entities.append(current_entity)
                    current_entity = None
            
            char_position += len(token) + 1  # +1 for space
        
        # Add last entity if exists
        if current_entity:
            entities.append(current_entity)
        
        # Only add if has entities
        if entities:
            training_data.append({
                "text": text,
                "entities": entities
            })
        
        # Progress indicator
        if (idx + 1) % 1000 == 0:
            print(f"  Processed {idx + 1}/{len(train_data)} examples...")
    
    print(f"\n✅ Converted {len(training_data)} examples with entities")
    
    # Save to JSON
    output_file = "conll2003_training_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved to {output_file}")
    
    # Show sample
    print("\n📋 Sample training example:")
    sample = training_data[0]
    print(f"Text: {sample['text']}")
    print(f"Entities: {sample['entities']}")
    
    return training_data

def convert_wnut17_to_spacy():
    """Download WNUT-17 and convert to spaCy format"""
    
    print("📥 Downloading WNUT-17 dataset...")
    print("(This may take 1-2 minutes)\n")
    
    # Load dataset
    dataset = load_dataset("wnut_17", trust_remote_code=True)
    
    # Get training split
    train_data = dataset["train"]
    
    print(f"✅ Downloaded {len(train_data)} training examples")
    
    # Label mapping for WNUT-17
    label_map = {
        0: "O",
        1: "B-corporation",
        2: "I-corporation",
        3: "B-creative-work",
        4: "I-creative-work",
        5: "B-group",
        6: "I-group",
        7: "B-location",
        8: "I-location",
        9: "B-person",
        10: "I-person",
        11: "B-product",
        12: "I-product"
    }
    
    print("\n🔄 Converting to spaCy format...")
    training_data = []
    
    for idx, example in enumerate(train_data):
        tokens = example["tokens"]
        ner_tags = example["ner_tags"]
        
        # Reconstruct text
        text = " ".join(tokens)
        
        # Extract entities
        entities = []
        current_entity = None
        char_position = 0
        
        for token, tag in zip(tokens, ner_tags):
            tag_label = label_map[tag]
            
            if tag_label.startswith("B-"):
                if current_entity:
                    entities.append(current_entity)
                
                entity_type = tag_label[2:].upper()  # Remove "B-" and uppercase
                current_entity = [char_position, char_position + len(token), entity_type]
            
            elif tag_label.startswith("I-") and current_entity:
                current_entity[1] = char_position + len(token)
            
            else:
                if current_entity:
                    entities.append(current_entity)
                    current_entity = None
            
            char_position += len(token) + 1
        
        if current_entity:
            entities.append(current_entity)
        
        if entities:
            training_data.append({
                "text": text,
                "entities": entities
            })
        
        if (idx + 1) % 500 == 0:
            print(f"  Processed {idx + 1}/{len(train_data)} examples...")
    
    print(f"\n✅ Converted {len(training_data)} examples with entities")
    
    output_file = "wnut17_training_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved to {output_file}")
    
    print("\n📋 Sample training example:")
    sample = training_data[0]
    print(f"Text: {sample['text']}")
    print(f"Entities: {sample['entities']}")
    
    return training_data

if __name__ == "__main__":
    print("=" * 70)
    print("           DATASET DOWNLOADER AND CONVERTER")
    print("=" * 70)
    print("\nChoose dataset to download:")
    print("1. CoNLL-2003 (News articles, ~14,000 examples) - RECOMMENDED")
    print("2. WNUT-17 (Social media, ~3,000 examples)")
    print("3. Both datasets")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    print("\n" + "=" * 70)
    
    if choice == "1":
        convert_conll2003_to_spacy()
    elif choice == "2":
        convert_wnut17_to_spacy()
    elif choice == "3":
        convert_conll2003_to_spacy()
        print("\n" + "=" * 70 + "\n")
        convert_wnut17_to_spacy()
    else:
        print("Invalid choice!")
    
    print("\n" + "=" * 70)
    print("Dataset download and conversion complete!")
    print("You can now train your model using train_model.py")
    print("=" * 70)