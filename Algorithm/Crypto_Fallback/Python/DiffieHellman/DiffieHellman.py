"""
Diffie-Hellman Key Exchange Python Fallback Implementation

This module provides a Python fallback implementation for the Diffie-Hellman
key exchange algorithm when native implementations are not available.

The Diffie-Hellman key exchange is a method for two parties to establish
a shared secret over an insecure channel.
"""

import random


def power_mod(base, exp, mod):
    """
    Calculate (base^exp) % mod efficiently using binary exponentiation.
    
    Args:
        base: The base number
        exp: The exponent
        mod: The modulus
    
    Returns:
        int: Result of (base^exp) % mod
    """
    result = 1
    base = base % mod
    
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    
    return result


def is_primitive_root(g, p):
    """
    Check if g is a primitive root modulo p.
    A primitive root g modulo p is an integer whose powers generate
    all non-zero elements modulo p.
    
    Args:
        g: Potential primitive root
        p: Prime modulus
    
    Returns:
        bool: True if g is a primitive root modulo p
    """
    if g <= 1 or g >= p:
        return False
    
    # Find all prime factors of p-1
    factors = []
    n = p - 1
    temp = n
    
    # Check for factor 2
    if temp % 2 == 0:
        factors.append(2)
        while temp % 2 == 0:
            temp //= 2
    
    # Check for odd factors
    i = 3
    while i * i <= temp:
        if temp % i == 0:
            factors.append(i)
            while temp % i == 0:
                temp //= i
        i += 2
    
    if temp > 2:
        factors.append(temp)
    
    # Check if g^((p-1)/factor) != 1 (mod p) for all prime factors
    for factor in factors:
        if power_mod(g, (p - 1) // factor, p) == 1:
            return False
    
    return True


def generate_safe_prime_and_generator(bit_length=8):
    """
    Generate a safe prime and its generator for Diffie-Hellman.
    
    Args:
        bit_length: Approximate bit length of the prime
    
    Returns:
        tuple: (prime, generator)
    """
    # For demonstration, use pre-computed safe primes
    safe_primes_and_generators = [
        (23, 5), (47, 5), (59, 2), (83, 2), (107, 2),
        (167, 5), (179, 2), (227, 17), (263, 5), (347, 19),
        (383, 5), (467, 2), (479, 13), (503, 5), (563, 2),
        (587, 2), (719, 11), (839, 11), (863, 5), (887, 3),
        (983, 5), (1019, 2), (1187, 2), (1223, 5)
    ]
    
    return random.choice(safe_primes_and_generators)


def diffie_hellman_key_exchange(p, g, private_a, private_b):
    """
    Perform complete Diffie-Hellman key exchange.
    
    Args:
        p: Prime modulus (public)
        g: Generator (public)
        private_a: Alice's private key
        private_b: Bob's private key
    
    Returns:
        dict: Contains all intermediate values and the shared secret
    """
    # Validate inputs
    if p <= 0 or g <= 0 or private_a <= 0 or private_b <= 0:
        raise ValueError("All parameters must be positive integers")
    
    if private_a >= p or private_b >= p:
        raise ValueError("Private keys must be less than the prime modulus")
    
    # Alice computes her public key: A = g^a mod p
    public_a = power_mod(g, private_a, p)
    
    # Bob computes his public key: B = g^b mod p
    public_b = power_mod(g, private_b, p)
    
    # Alice computes shared secret: S = B^a mod p
    shared_secret_alice = power_mod(public_b, private_a, p)
    
    # Bob computes shared secret: S = A^b mod p
    shared_secret_bob = power_mod(public_a, private_b, p)
    
    # Verify that both parties computed the same shared secret
    if shared_secret_alice != shared_secret_bob:
        raise RuntimeError("Shared secrets do not match - calculation error")
    
    return {
        'p': p,
        'g': g,
        'private_a': private_a,
        'private_b': private_b,
        'public_a': public_a,
        'public_b': public_b,
        'shared_secret': shared_secret_alice,
        'alice_calculation': f"{public_b}^{private_a} mod {p} = {shared_secret_alice}",
        'bob_calculation': f"{public_a}^{private_b} mod {p} = {shared_secret_bob}",
        'public_a_calculation': f"{g}^{private_a} mod {p} = {public_a}",
        'public_b_calculation': f"{g}^{private_b} mod {p} = {public_b}"
    }


def diffie_hellman_fallback(p, g, private_a, private_b):
    """
    Main fallback function for Diffie-Hellman key exchange.
    This function matches the interface expected by the Django views.
    
    Args:
        p: Prime modulus (as string or int)
        g: Generator (as string or int)
        private_a: Alice's private key (as string or int)
        private_b: Bob's private key (as string or int)
    
    Returns:
        dict: Results of the key exchange
    """
    try:
        # Convert string inputs to integers
        p = int(p)
        g = int(g)
        private_a = int(private_a)
        private_b = int(private_b)
        
        # Perform the key exchange
        result = diffie_hellman_key_exchange(p, g, private_a, private_b)
        
        return {
            'success': True,
            'result': result,
            'error': None
        }
        
    except ValueError as e:
        return {
            'success': False,
            'result': None,
            'error': f"Invalid input: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'result': None,
            'error': f"Calculation error: {str(e)}"
        }


def generate_random_parameters():
    """
    Generate random parameters for Diffie-Hellman key exchange.
    
    Returns:
        dict: Random parameters including p, g, and private keys
    """
    p, g = generate_safe_prime_and_generator()
    private_a = random.randint(2, p - 2)
    private_b = random.randint(2, p - 2)
    
    return {
        'p': p,
        'g': g,
        'private_a': private_a,
        'private_b': private_b
    }


if __name__ == "__main__":
    # Example usage
    print("Diffie-Hellman Key Exchange Example")
    print("=" * 40)
    
    # Use default parameters
    p, g = 23, 5
    private_a, private_b = 6, 15
    
    print(f"Public Parameters:")
    print(f"  Prime (p): {p}")
    print(f"  Generator (g): {g}")
    print(f"\nPrivate Keys:")
    print(f"  Alice's private key (a): {private_a}")
    print(f"  Bob's private key (b): {private_b}")
    
    result = diffie_hellman_fallback(p, g, private_a, private_b)
    
    if result['success']:
        data = result['result']
        print(f"\nPublic Keys:")
        print(f"  Alice's public key: {data['public_a_calculation']}")
        print(f"  Bob's public key: {data['public_b_calculation']}")
        print(f"\nShared Secret Calculation:")
        print(f"  Alice: {data['alice_calculation']}")
        print(f"  Bob: {data['bob_calculation']}")
        print(f"\nShared Secret: {data['shared_secret']}")
    else:
        print(f"Error: {result['error']}")
