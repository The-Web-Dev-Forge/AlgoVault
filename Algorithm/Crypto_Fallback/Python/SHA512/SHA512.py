"""
SHA-512 Hash Python Implementation

This module provides the implementation of the SHA-512 hash function using Python's hashlib.
"""

import hashlib

def sha512_hash(message):
    """
    Perform SHA-512 hashing
    
    Parameters:
    message (str): The text to be hashed
    
    Returns:
    str: The hexadecimal representation of the hash
    """
    sha512_hash = hashlib.sha512()  # Create a SHA-512 hash object
    sha512_hash.update(message.encode('utf-8'))  # Update with the message bytes
    result_hex = sha512_hash.hexdigest()  # Get the hash in hexadecimal format
    
    return result_hex
