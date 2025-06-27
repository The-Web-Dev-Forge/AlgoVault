"""
AES Python fallback implementation using the cryptography library.
This is a simplified fallback when the Java implementation is not available.
"""

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    import base64
    import json
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False

"""
AES Python fallback implementation using the cryptography library.
This is a simplified fallback when the Java implementation is not available.
"""

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    import base64
    import json
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False

def aes_fallback(operation, message, key):
    """
    Simple AES fallback using Python cryptography library.
    Returns a simplified result format matching the Java implementation structure.
    """
    if not CRYPTOGRAPHY_AVAILABLE:
        # Provide a working demo result even without cryptography
        demo_result = "Demo mode - install cryptography for real AES"
        if operation.lower() == 'encrypt':
            # Simple base64 encoding as demo
            demo_result = base64.b64encode(message.encode()).decode()
        else:
            # Simple base64 decoding as demo
            try:
                demo_result = base64.b64decode(message).decode()
            except:
                demo_result = "Invalid base64 for demo decryption"
        
        return {
            "blocks": [{
                "block": 1,
                "rounds": [{
                    "round": 1,
                    "startOfRound": "DEMO4D4F44454C4F44454D4F44454D4F",
                    "afterSubBytes": "Install cryptography: pip install cryptography",
                    "afterShiftRows": "For full AES functionality with visualization",
                    "afterMixColumns": "Currently showing demo mode only",
                    "afterAddRoundKey": "Real encryption requires cryptography lib"
                }]
            }],
            "finalResult": demo_result
        }
    
    try:
        # Ensure key is exactly 16 bytes
        key_bytes = key.encode('utf-8')[:16].ljust(16, b'\0')
        
        if operation.lower() == 'encrypt':
            # Encrypt the message
            message_bytes = message.encode('utf-8')
            
            # Pad message to 16-byte blocks (PKCS7 padding)
            padding_length = 16 - (len(message_bytes) % 16)
            padded_message = message_bytes + bytes([padding_length] * padding_length)
            
            # Use AES in ECB mode for simplicity (matching Java implementation)
            cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_message) + encryptor.finalize()
            
            result = base64.b64encode(ciphertext).decode('utf-8')
            
            # Create visualization blocks
            blocks = []
            for i in range(0, len(padded_message), 16):
                block_data = padded_message[i:i+16]
                block_hex = block_data.hex().upper()
                
                blocks.append({
                    "block": (i // 16) + 1,
                    "rounds": [{
                        "round": r + 1,
                        "startOfRound": block_hex,
                        "afterSubBytes": "Python fallback - steps simplified",
                        "afterShiftRows": "Use Java implementation for details", 
                        "afterMixColumns": "This shows working encryption/decryption",
                        "afterAddRoundKey": f"Round {r+1} completed"
                    } for r in range(10)]  # AES-128 has 10 rounds
                })
            
        else:  # decrypt
            # Decode base64 input
            try:
                ciphertext = base64.b64decode(message)
            except:
                return {
                    "blocks": [],
                    "finalResult": "Error: Invalid base64 input for decryption"
                }
            
            # Decrypt
            cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            # Remove padding
            padding_length = padded_plaintext[-1]
            if padding_length <= 16 and all(b == padding_length for b in padded_plaintext[-padding_length:]):
                plaintext = padded_plaintext[:-padding_length]
            else:
                plaintext = padded_plaintext
            
            result = plaintext.decode('utf-8', errors='replace')
            
            # Create visualization blocks for decryption
            blocks = []
            for i in range(0, len(ciphertext), 16):
                block_data = ciphertext[i:i+16]
                block_hex = block_data.hex().upper()
                
                blocks.append({
                    "block": (i // 16) + 1,
                    "rounds": [{
                        "round": r + 1,
                        "startOfRound": block_hex,
                        "afterInvShiftRows": "Python fallback - steps simplified",
                        "afterInvSubBytes": "Use Java implementation for details",
                        "afterAddRoundKey": f"Decryption round {r+1}",
                        "afterInvMixColumns": "Working decryption process"
                    } for r in range(10)]  # AES-128 has 10 rounds
                })
        
        # Return structure matching Java output
        return {
            "blocks": blocks,
            "finalResult": result
        }
        
    except Exception as e:
        return {
            "blocks": [{
                "block": 1,
                "rounds": [{
                    "round": 1,
                    "startOfRound": "ERROR000000000000000000000000000",
                    "afterSubBytes": f"Error: {str(e)[:30]}",
                    "afterShiftRows": "Python fallback encountered an error",
                    "afterMixColumns": "Please check your input and try again",
                    "afterAddRoundKey": "Or install: pip install cryptography"
                }]
            }],
            "finalResult": f"Error in Python AES fallback: {str(e)}"
        }
