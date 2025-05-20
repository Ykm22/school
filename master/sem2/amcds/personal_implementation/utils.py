import re

def extract_register_id(abstraction_id: str):
    match = re.search(r'\[(.*?)\]', abstraction_id)
    if match:
        result = match.group(1)
        return result
    return None
