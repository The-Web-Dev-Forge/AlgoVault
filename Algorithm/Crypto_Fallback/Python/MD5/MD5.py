"""
MD5 Hash Algorithm Implementation
Python fallback implementation for MD5 hashing when Java implementation fails.
"""

import hashlib
import base64
from collections import Counter
import math


class MD5Hash:
    """
    Python MD5 hash implementation utility class.
    Serves as a fallback when Java implementation fails.
    """
    
    @staticmethod
    def generate_hash(input_text, output_format='hex'):
        """
        Generate MD5 hash with specified output format.
        
        Args:
            input_text (str): Text to hash
            output_format (str): Output format ('hex', 'hex-lower', 'hex-upper', 'HEX', 'base64')
            
        Returns:
            str: Formatted MD5 hash
        """
        if not input_text:
            raise ValueError("Input text cannot be empty")
            
        # Generate MD5 hash
        md5_hash = hashlib.md5(input_text.encode('utf-8')).hexdigest()
        
        # Format output based on requested format
        if output_format.lower() in ['hex', 'hex-lower']:
            return md5_hash.lower()
        elif output_format.lower() in ['hex-upper', 'HEX']:
            return md5_hash.upper()
        elif output_format.lower() == 'base64':
            hex_bytes = bytes.fromhex(md5_hash)
            return base64.b64encode(hex_bytes).decode('utf-8')
        else:
            return md5_hash.lower()  # default
    
    @staticmethod
    def verify_hash(input_text, expected_hash, output_format='hex'):
        """
        Verify if input text matches the expected hash.
        
        Args:
            input_text (str): Text to verify
            expected_hash (str): Expected hash value
            output_format (str): Format of the expected hash
            
        Returns:
            tuple: (generated_hash, matches_boolean)
        """
        generated_hash = MD5Hash.generate_hash(input_text, output_format)
        matches = generated_hash.lower() == expected_hash.lower()
        return generated_hash, matches
    
    @staticmethod
    def calculate_hash_properties(hash_string):
        """
        Calculate various properties of a hash string for analysis.
        
        Args:
            hash_string (str): Hash string to analyze
            
        Returns:
            dict: Dictionary containing hash properties
        """
        if not hash_string:
            return {
                'length': 0,
                'unique_chars': 0,
                'entropy': 0.0
            }
        
        # Calculate basic properties
        hash_length = len(hash_string)
        unique_chars = len(set(hash_string.lower()))
        
        # Calculate entropy
        counts = Counter(hash_string.lower())
        probs = [count / len(hash_string) for count in counts.values()]
        entropy = -sum(p * math.log2(p) for p in probs if p > 0)
        
        return {
            'length': hash_length,
            'unique_chars': unique_chars,
            'entropy': round(entropy, 2)
        }
