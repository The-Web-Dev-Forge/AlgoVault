"""
Caesar Cipher Python Fallback Implementation

This module provides the fallback implementation of the Caesar cipher when the C++/Java executables
are not available or encounter errors. It includes functionality for encryption, decryption,
brute force analysis, and frequency analysis.
"""

def caesar_cipher_fallback(message, shift, operation):
    """
    Python fallback implementation of Caesar Cipher - matches PDF specification
    
    Parameters:
    message (str): The text to be processed
    shift (int): The shift value for encryption/decryption
    operation (str): The operation to perform ('encrypt', 'decrypt', 'brute-force', or 'frequency')
    
    Returns:
    str: The result of the cipher operation
    """
    if operation == 'brute-force':
        # Perform brute force analysis
        result = "BRUTE FORCE ANALYSIS RESULTS:\n"
        result += "================================\n\n"
        
        for test_shift in range(1, 26):
            decrypted = ""
            for char in message:
                if char.isalpha():
                    base = ord('A') if char.isupper() else ord('a')
                    decrypted += chr(base + (ord(char) - base + (26 - test_shift)) % 26)
                else:
                    decrypted += char
            result += f"Shift {test_shift}: {decrypted}\n"
        
        result += "\n================================\n"
        result += "Analyze the results above to find the most meaningful text.\n\n"
        result += "IF NO MEANINGFUL WORDS FOUND:\n"
        result += "1. Check if input is actually Caesar cipher (single-shift substitution)\n"
        result += "2. Consider if text might be double-encrypted\n" 
        result += "3. Verify the input contains valid encrypted text\n"
        result += "4. Try applying frequency analysis instead\n"
        result += "5. The text might be using a different cipher method (Vigenere, etc.)\n"
        result += "6. For very short texts, multiple valid decryptions may exist"
        return result
    
    # Regular encrypt/decrypt operations
    result = ""
    
    for char in message:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            if operation == 'encrypt':
                result += chr(base + (ord(char) - base + shift) % 26)
            else:  # decrypt - using 26 - shift method from PDF
                result += chr(base + (ord(char) - base + (26 - shift)) % 26)
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
    # Count letter frequencies
    freq = [0] * 26
    total_letters = 0
    
    for char in message:
        if char.isalpha():
            freq[ord(char.upper()) - ord('A')] += 1
            total_letters += 1
    
    result = "CAESAR FREQUENCY ANALYSIS:\n"
    result += "==============================\n\n"
    result += "Letter frequencies:\n"
    
    for i in range(26):
        letter = chr(ord('A') + i)
        percentage = (freq[i] * 100.0 / total_letters) if total_letters > 0 else 0.0
        result += f"{letter}: {freq[i]} ({percentage:.1f}%)\n"
    
    result += "\nCommon English letter frequencies:\n"
    result += "E: 12.7%, T: 9.1%, A: 8.2%, O: 7.5%, I: 7.0%, N: 6.7%\n"
    result += "S: 6.3%, H: 6.1%, R: 6.0%, D: 4.3%, L: 4.0%, C: 2.8%\n\n"
    
    result += "Analysis: Compare the frequencies above with typical English.\n"
    result += "For Caesar cipher, the entire distribution is shifted. Look for a\n"
    result += "letter with frequency close to E's (12.7%) and count the shift from E."
    
    return result
