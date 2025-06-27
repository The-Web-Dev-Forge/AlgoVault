"""
Vigenere Cipher Python Fallback Implementation

This module provides the fallback implementation of the Vigenere cipher when the C++/Java executables
are not available or encounter errors. It includes functionality for encryption, decryption,
brute force analysis, and frequency analysis.
"""

def vigenere_cipher_fallback(message, keyword, operation):
    """
    Python fallback implementation of Vigenere Cipher - matches PDF specification
    
    Parameters:
    message (str): The text to be processed
    keyword (str): The keyword for encryption/decryption
    operation (str): The operation to perform ('encrypt', 'decrypt', 'brute-force', or 'frequency')
    
    Returns:
    str: The result of the cipher operation
    """
    
    def vigenere_decrypt_with_key(text, key):
        """Helper function to decrypt with a specific key"""
        result = ""
        key = key.upper()
        key_index = 0
        
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shift = ord(key[key_index % len(key)]) - ord('A')
                result += chr(base + (ord(char) - base - shift + 26) % 26)
                key_index += 1
            else:
                result += char
        
        return result
    
    if operation == 'brute-force':
        # Perform brute force analysis with common keywords
        result = "VIGENERE BRUTE FORCE ANALYSIS:\n"
        result += "================================\n\n"
        
        # Common keywords to try (most frequently used passwords/keys)
        common_keys = [
            # Single letters
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            
            # Common short words
            "KEY", "ABC", "THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL",
            "CAN", "HIS", "HER", "WAS", "ONE", "OUR", "OUT", "DAY", "GET", "HAS",
            
            # Common 4+ letter words
            "WORD", "CODE", "TEST", "HELP", "LOVE", "HOPE", "LIFE", "TIME", "WORK",
            "KEYS", "PASS", "USER", "ADMIN", "SECRET", "CIPHER", "CRYPTO", "SECURE",
            
            # Common patterns
            "ABCD", "ABCDE", "ABCDEF", "KEYKEY", "TESTTEST", "PASSWORD"
        ]
        
        result += "Trying common keywords:\n"
        result += "------------------------\n"
        
        for test_key in common_keys:
            decrypted = vigenere_decrypt_with_key(message, test_key)
            # Only show first 100 characters for readability
            preview = decrypted[:100] + ("..." if len(decrypted) > 100 else "")
            result += f"Key '{test_key}' ({len(test_key)} chars): {preview}\n"
        
        result += "\n================================\n"
        result += "ANALYSIS TIPS:\n"
        result += "1. Look for readable English text\n"
        result += "2. Check for common words like 'THE', 'AND', 'A'\n"
        result += "3. Meaningful results indicate the correct key\n"
        result += "4. If no results look good, the key might be longer or unusual\n\n"
        
        result += "IF NO MEANINGFUL WORDS APPEAR:\n"
        result += "1. Try manual key guessing based on context/theme of the message\n"
        result += "2. The key might be longer than tested here (try 5+ letters)\n"
        result += "3. Try analyzing with Kasiski examination for key length\n"
        result += "4. Consider using frequency analysis to determine likely key letters\n"
        result += "5. The text may be using a different cipher or multiple layers of encryption\n"
        result += "6. For very short texts, statistical analysis may not be reliable\n"
        
        return result
    
    elif operation == 'frequency':
        # Perform frequency analysis
        return frequency_analysis(message)
    
    # Regular encrypt/decrypt operations
    result = ""
    keyword = keyword.upper()  # Ensure keyword is uppercase
    key_index = 0
    
    for char in message:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(keyword[key_index % len(keyword)]) - ord('A')
            
            if operation == 'encrypt':
                result += chr(base + (ord(char) - base + shift) % 26)
            else:  # decrypt
                result += chr(base + (ord(char) - base - shift + 26) % 26)
            
            key_index += 1
        else:
            result += char
    
    return result

def frequency_analysis(message):
    """
    Perform frequency analysis on the given message
    
    Parameters:
    message (str): The text to analyze
    
    Returns:
    str: Formatted frequency analysis results
    """
    result = "VIGENERE FREQUENCY ANALYSIS:\n"
    result += "==============================\n\n"
    
    # Count letter frequencies
    freq = [0] * 26
    total_letters = 0
    
    for char in message:
        if char.isalpha():
            freq[ord(char.upper()) - ord('A')] += 1
            total_letters += 1
    
    result += "Letter frequencies:\n"
    for i in range(26):
        letter = chr(ord('A') + i)
        percentage = (freq[i] * 100.0 / total_letters) if total_letters > 0 else 0.0
        result += f"{letter}: {freq[i]} ({percentage:.1f}%)\n"
    
    result += "\nCommon English letter frequencies:\n"
    result += "E: 12.7%, T: 9.1%, A: 8.2%, O: 7.5%, I: 7.0%, N: 6.7%\n"
    result += "S: 6.3%, H: 6.1%, R: 6.0%, D: 4.3%, L: 4.0%, C: 2.8%\n\n"
    
    result += "Analysis: Compare the frequencies above with typical English.\n"
    result += "Large deviations may indicate the key length or cipher method."
    
    return result
