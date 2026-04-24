import pandas as pd

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------
    
    # TODO: Remove duplicate rows based on 'id'
    df = df.drop_duplicates(subset=['id'], keep='first')
    
    # TODO: Clean 'price' column: convert "$1200", "250000", "five dollars" to floats
    def clean_price(val):
        if pd.isna(val) or val == 'NULL' or val == 'N/A' or val == 'Liên hệ':
            return None
        val = str(val).lower().replace('$', '').replace(',', '').strip()
        try:
            return float(val)
        except ValueError:
            return None
    df['price'] = df['price'].apply(clean_price)
    
    # TODO: Normalize 'date_of_sale' into a single format (YYYY-MM-DD)
    df['date_of_sale'] = pd.to_datetime(df['date_of_sale'], format='mixed', errors='coerce').dt.strftime('%Y-%m-%d')
    
    # TODO: Return a list of dictionaries for the UnifiedDocument schema.
    result = []
    for _, row in df.iterrows():
        doc = {
            "document_id": f"csv-{row['id']}",
            "content": f"{row['product_name']} - {row['category']}",
            "source_type": "CSV",
            "author": str(row.get('seller_id', 'Unknown')),
            "timestamp": row['date_of_sale'] if pd.notna(row['date_of_sale']) else None,
            "source_metadata": {
                "price": row['price'],
                "currency": str(row['currency']),
                "stock_quantity": row.get('stock_quantity')
            }
        }
        result.append(doc)
    
    return result

