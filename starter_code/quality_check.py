# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

def run_quality_gate(document_dict):
    # TODO: Reject documents with 'content' length < 20 characters
    content = document_dict.get('content', '')
    if len(content) < 20:
        return False
        
    # TODO: Reject documents containing toxic/error strings (e.g., 'Null pointer exception')
    toxic_strings = ['null pointer exception', 'fatal error', 'unhandled exception']
    if any(toxic in content.lower() for toxic in toxic_strings):
        return False
        
    # TODO: Flag discrepancies (e.g., if tax calculation comment says 8% but code says 10%)
    if "legacy-code" in document_dict.get('document_id', ''):
        if "8%" in content and "0.10" in content:
            print(f"Watchman Flag: Found discrepancy in {document_dict.get('document_id')}")
            # we might still let it pass or fail depending on strictness. Let's pass but flag it.
            
    # Return True if pass, False if fail.
    return True
