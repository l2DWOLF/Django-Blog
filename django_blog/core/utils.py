def parse_int(value:str, default=None):
    try:
        return int(value)
    except(ValueError, TypeError):
        return default
    
def to_lower_strip(value:str, default=None):
    try:
        return str(value.lower().strip())
    except(ValueError, TypeError):
        return default