"""
Diffie-Hellman Key Exchange Module

This module provides Python fallback implementation for Diffie-Hellman key exchange.
"""

from .DiffieHellman import (
    diffie_hellman_fallback,
    diffie_hellman_key_exchange,
    generate_random_parameters,
    power_mod,
    is_primitive_root,
    generate_safe_prime_and_generator
)

__all__ = [
    'diffie_hellman_fallback',
    'diffie_hellman_key_exchange', 
    'generate_random_parameters',
    'power_mod',
    'is_primitive_root',
    'generate_safe_prime_and_generator'
]
