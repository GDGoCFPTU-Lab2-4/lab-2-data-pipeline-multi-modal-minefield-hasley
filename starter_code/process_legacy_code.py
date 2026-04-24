import ast

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    # TODO: Use the 'ast' module to find docstrings for functions
    tree = ast.parse(source_code)
    docstrings = []
    
    # Module docstring
    mod_doc = ast.get_docstring(tree)
    if mod_doc:
        docstrings.append(f"Module Docstring: {mod_doc}")
        
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            doc = ast.get_docstring(node)
            if doc:
                docstrings.append(f"{node.name} Docstring: {doc}")
                
    import re
    # TODO: (Optional/Advanced) Use regex to find business rules in comments like "# Business Logic Rule 001"
    comments = re.findall(r'#.*', source_code)
    business_rules = [c for c in comments if "Business Logic Rule" in c or "WARNING:" in c]
    
    combined_content = "\n\n".join(docstrings)
    if business_rules:
        combined_content += "\n\nExtracted Comments:\n" + "\n".join(business_rules)
        
    # TODO: Return a dictionary for the UnifiedDocument schema.
    doc = {
        "document_id": "legacy-code-001",
        "content": combined_content,
        "source_type": "Code",
        "author": "Unknown",
        "timestamp": None,
        "source_metadata": {}
    }
    return doc

