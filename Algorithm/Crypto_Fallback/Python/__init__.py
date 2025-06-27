"""
Python Fallback Package for Cryptographic Algorithms

This package provides fallback implementations for various cryptographic algorithms
when their corresponding C++/Java executables are not available or encounter errors.
"""

# Make all subpackages accessible
from .caesar import caesar_cipher_fallback
from .vigenere import vigenere_cipher_fallback
from .hill import hill_cipher_fallback
from .des import des_fallback
from .sha512 import sha512_hash
