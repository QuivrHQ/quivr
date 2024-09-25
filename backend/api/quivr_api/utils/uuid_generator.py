import hashlib
import uuid


def generate_uuid_from_string(input_string):
    # Hash the input string using SHA-1 (or any other hash function)
    hash_obj = hashlib.sha1(input_string.encode())
    # Get the hexadecimal digest of the hash
    hash_hex = hash_obj.hexdigest()
    # Create a UUID from the first 32 characters of the hash
    return uuid.UUID(hash_hex[:32])
