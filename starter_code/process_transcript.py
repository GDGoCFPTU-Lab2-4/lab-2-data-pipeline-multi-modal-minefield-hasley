import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------
    
    # TODO: Remove noise tokens like [Music], [inaudible], [Laughter]
    text = re.sub(r'\[(?i:Music.*?|inaudible|Laughter)\]', '', text)
    
    # TODO: Strip timestamps [00:00:00]
    text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)
    
    # Clean extra whitespaces
    text = '\n'.join([line.strip() for line in text.split('\n') if line.strip()])
    
    # TODO: Find the price mentioned in Vietnamese words ("năm trăm nghìn")
    detected_price = None
    if "năm trăm nghìn" in text.lower():
        detected_price = 500000
        
    # TODO: Return a cleaned dictionary for the UnifiedDocument schema.
    doc = {
        "document_id": "video-transcript-001",
        "content": text,
        "source_type": "Video",
        "author": "Unknown",
        "timestamp": None,
        "source_metadata": {
            "detected_price_vnd": detected_price
        }
    }
    
    return doc

