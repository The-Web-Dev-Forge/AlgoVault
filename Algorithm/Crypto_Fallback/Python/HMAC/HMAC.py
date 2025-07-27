import hashlib
import hmac as python_hmac

class HMACHash:
    """HMAC (Hash-based Message Authentication Code) implementation using various hash algorithms."""
    
    SUPPORTED_ALGORITHMS = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha224': hashlib.sha224,
        'sha256': hashlib.sha256,
        'sha384': hashlib.sha384,
        'sha512': hashlib.sha512
    }
    
    @staticmethod
    def generate_hmac(message, key, algorithm='sha256', output_format='hex'):
        """
        Generate HMAC for a message with a secret key.
        
        Args:
            message (str): The message to authenticate
            key (str): The secret key
            algorithm (str): Hash algorithm to use (md5, sha1, sha224, sha256, sha384, sha512)
            output_format (str): Output format - 'hex', 'HEX', or 'base64'
            
        Returns:
            str: The HMAC in the specified format
        """
        try:
            # Convert inputs to bytes
            message_bytes = message.encode('utf-8')
            key_bytes = key.encode('utf-8')
            
            # Get the hash function
            if algorithm not in HMACHash.SUPPORTED_ALGORITHMS:
                raise ValueError(f"Unsupported algorithm: {algorithm}")
            
            hash_func = HMACHash.SUPPORTED_ALGORITHMS[algorithm]
            
            # Generate HMAC
            hmac_obj = python_hmac.new(key_bytes, message_bytes, hash_func)
            
            # Format output
            if output_format.lower() == 'hex':
                return hmac_obj.hexdigest()
            elif output_format.upper() == 'HEX':
                return hmac_obj.hexdigest().upper()
            elif output_format.lower() == 'base64':
                import base64
                return base64.b64encode(hmac_obj.digest()).decode('ascii')
            else:
                return hmac_obj.hexdigest()
                
        except Exception as e:
            raise Exception(f"HMAC generation failed: {str(e)}")
    
    @staticmethod
    def verify_hmac(message, key, expected_hmac, algorithm='sha256', output_format='hex'):
        """
        Verify an HMAC against the expected value.
        
        Args:
            message (str): The original message
            key (str): The secret key
            expected_hmac (str): The expected HMAC to verify against
            algorithm (str): Hash algorithm used
            output_format (str): Output format of the expected HMAC
            
        Returns:
            tuple: (generated_hmac, is_match)
        """
        try:
            generated_hmac = HMACHash.generate_hmac(message, key, algorithm, output_format)
            
            # Compare HMACs (case-insensitive for hex)
            if output_format.lower() in ['hex', 'HEX']:
                is_match = generated_hmac.lower() == expected_hmac.lower()
            else:
                is_match = generated_hmac == expected_hmac
            
            return generated_hmac, is_match
            
        except Exception as e:
            raise Exception(f"HMAC verification failed: {str(e)}")
    
    @staticmethod
    def get_algorithm_info(algorithm='sha256'):
        """
        Get information about a specific hash algorithm.
        
        Args:
            algorithm (str): The algorithm name
            
        Returns:
            dict: Algorithm information
        """
        algorithm_info = {
            'md5': {'digest_size': 16, 'block_size': 64, 'description': 'MD5 (128-bit)'},
            'sha1': {'digest_size': 20, 'block_size': 64, 'description': 'SHA-1 (160-bit)'},
            'sha224': {'digest_size': 28, 'block_size': 64, 'description': 'SHA-224 (224-bit)'},
            'sha256': {'digest_size': 32, 'block_size': 64, 'description': 'SHA-256 (256-bit)'},
            'sha384': {'digest_size': 48, 'block_size': 128, 'description': 'SHA-384 (384-bit)'},
            'sha512': {'digest_size': 64, 'block_size': 128, 'description': 'SHA-512 (512-bit)'}
        }
        
        return algorithm_info.get(algorithm, {})


def hmac_fallback(message, key, algorithm='sha256', operation='generate', expected_hmac='', output_format='hex'):
    """
    Fallback function for HMAC operations - compatible with the main application structure.
    
    Args:
        message (str): The message to authenticate
        key (str): The secret key
        algorithm (str): Hash algorithm to use
        operation (str): 'generate' or 'verify'
        expected_hmac (str): Expected HMAC for verification
        output_format (str): Output format
        
    Returns:
        str or tuple: HMAC string for generation, or (hmac, match_bool) for verification
    """
    if operation == 'verify':
        return HMACHash.verify_hmac(message, key, expected_hmac, algorithm, output_format)
    else:
        return HMACHash.generate_hmac(message, key, algorithm, output_format)
