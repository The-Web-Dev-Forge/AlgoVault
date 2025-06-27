"""
DES Cipher Python Fallback Implementation

This module provides a fallback implementation of the DES cipher when the Java
executable is not available or encounters errors. This implementation uses PyCryptodome
for proper DES encryption/decryption.
"""

import base64
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

def des_fallback(operation, key_str, text_str):
    """
    Python fallback implementation of DES using PyCryptodome
    
    Parameters:
    operation (str): The operation to perform ('encrypt' or 'decrypt')
    key_str (str): The encryption/decryption key (must be 8 bytes)
    text_str (str): The text to be processed or base64-encoded ciphertext
    
    Returns:
    str: The result of the cipher operation (base64-encoded if encryption)
    """
    try:
        # Ensure key is 8 bytes (DES requirement)
        key_bytes = key_str.encode('utf-8')
        if len(key_bytes) < 8:
            # Pad with zeros if too short
            key_bytes = key_bytes + b'\0' * (8 - len(key_bytes))
        elif len(key_bytes) > 8:
            # Truncate if too long
            key_bytes = key_bytes[:8]
        
        # Create DES cipher in ECB mode
        cipher = DES.new(key_bytes, DES.MODE_ECB)
        
        if operation.lower() == 'encrypt':
            # Convert text to bytes and pad to block size
            data = text_str.encode('utf-8')
            padded_data = pad(data, DES.block_size)
            
            # Encrypt and encode to base64
            encrypted_bytes = cipher.encrypt(padded_data)
            return base64.b64encode(encrypted_bytes).decode('utf-8')
        
        elif operation.lower() == 'decrypt':
            try:
                # Decode from base64 and decrypt
                encrypted_bytes = base64.b64decode(text_str)
                decrypted_padded = cipher.decrypt(encrypted_bytes)
                
                # Remove padding and convert to string
                decrypted_bytes = unpad(decrypted_padded, DES.block_size)
                return decrypted_bytes.decode('utf-8')
            except Exception as e:
                return f"Decryption error: {str(e)}"
        
        else:
            return f"Invalid operation: {operation}. Use 'encrypt' or 'decrypt'"
            
    except Exception as e:
        return f"DES fallback error: {str(e)}"
