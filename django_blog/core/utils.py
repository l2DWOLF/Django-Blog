def parse_int(value:str, default=None):
    try:
        return int(value)
    except(ValueError, TypeError):
        return default