
def hash_title(title) -> str:
    import hashlib
    hash = int(hashlib.sha256(title.encode('utf-8')).hexdigest(), 16) % 10**8
    return str(hash)
