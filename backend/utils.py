import hashlib

def compute_sha1_from_file(file_path):
    with open(file_path, "rb") as file:
        bytes = file.read() 
        readable_hash = compute_sha1_from_content(bytes)
    return readable_hash

def compute_sha1_from_content(content):
    readable_hash = hashlib.sha1(content).hexdigest()
    return readable_hash
