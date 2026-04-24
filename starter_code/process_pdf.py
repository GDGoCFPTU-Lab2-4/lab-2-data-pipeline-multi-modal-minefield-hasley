import google.generativeai as genai
import os

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Use Gemini API to extract structured data from lecture_notes.pdf

def extract_pdf_data(file_path):
    # --- FILE CHECK (Handled for students) ---
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None
    # ------------------------------------------

    # TODO: Initialize Gemini API (make sure GEMINI_API_KEY is set)
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY is not set. Skipping PDF extraction.")
        return None
        
    genai.configure(api_key=api_key)
    
    # TODO: Load the PDF file
    try:
        pdf_file = genai.upload_file(path=file_path)
        
        # TODO: Send a prompt to Gemini to extract: Title, Author, and a Summary.
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        import time
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = model.generate_content(
                    [pdf_file, "Extract Title, Author, and a 3-sentence summary. Return ONLY a valid JSON object with keys: 'title', 'author', 'summary'. Do not use markdown blocks."]
                )
                import json
                try:
                    result = json.loads(response.text.strip())
                except json.JSONDecodeError:
                    # try to strip markdown if any
                    text = response.text.strip()
                    if text.startswith('```json'):
                        text = text[7:-3].strip()
                    elif text.startswith('```'):
                        text = text[3:-3].strip()
                    result = json.loads(text)
                
                # TODO: Return a dictionary that fits the UnifiedDocument schema.
                doc = {
                    "document_id": "pdf-001",
                    "content": result.get("summary", "No summary found"),
                    "source_type": "PDF",
                    "author": result.get("author", "Unknown"),
                    "timestamp": None,
                    "source_metadata": {
                        "title": result.get("title", "Unknown Title")
                    }
                }
                return doc
            except Exception as e:
                if "429" in str(e) or "Quota" in str(e):
                    time.sleep(2 ** attempt)
                else:
                    print(f"Error calling Gemini API: {e}")
                    break
    except Exception as e:
        print(f"Error uploading PDF to Gemini: {e}")
        
    return None

