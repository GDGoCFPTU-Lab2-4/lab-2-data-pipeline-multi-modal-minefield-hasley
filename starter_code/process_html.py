from bs4 import BeautifulSoup

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # ------------------------------------------
    
    # TODO: Use BeautifulSoup to find the table with id 'main-catalog'
    table = soup.find('table', id='main-catalog')
    if not table:
        return []
    
    # TODO: Extract rows, handling 'N/A' or 'Liên hệ' in the price column.
    # TODO: Return a list of dictionaries for the UnifiedDocument schema.
    result = []
    tbody = table.find('tbody')
    if not tbody:
        return []
        
    for row in tbody.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) < 6:
            continue
            
        sp_id = cols[0].get_text(strip=True)
        name = cols[1].get_text(strip=True)
        category = cols[2].get_text(strip=True)
        price_text = cols[3].get_text(strip=True)
        stock_text = cols[4].get_text(strip=True)
        rating = cols[5].get_text(strip=True)
        
        # Parse price
        price = None
        if price_text.lower() not in ['n/a', 'liên hệ']:
            try:
                price = float(price_text.lower().replace('vnd', '').replace(',', '').strip())
            except ValueError:
                price = None
                
        # Parse stock
        stock = None
        try:
            stock = int(stock_text)
        except ValueError:
            pass
            
        doc = {
            "document_id": f"html-{sp_id}",
            "content": f"{name} - {category}",
            "source_type": "HTML",
            "author": "Unknown",
            "timestamp": None,
            "source_metadata": {
                "price_vnd": price,
                "stock": stock,
                "rating": rating
            }
        }
        result.append(doc)
    
    return result

