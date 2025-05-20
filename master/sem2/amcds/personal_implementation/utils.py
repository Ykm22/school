import re

def extract_register_id(abstraction_id: str):
    match = re.search(r'\[(.*?)\]', abstraction_id)
    if match:
        result = match.group(1)
        return result
    return None

def get_max_rank(processes: dict):
    max_rank = None
    print("idk if it works!")
    
    for key, proc in processes.items():
        if max_rank is None or proc.rank > max_rank.rank:
            max_rank = proc
    
    return max_rank

def get_max_rank_slice(processes: list):
    max_rank = None
    
    for proc in processes:
        if max_rank is None or proc.rank > max_rank.rank:
            max_rank = proc
    
    return max_rank
