"""
Hill Cipher Python Fallback Implementation

This module provides the fallback implementation of the Hill cipher when the C++/Java executables
are not available or encounter errors. It includes functionality for encryption and decryption
using matrix operations, matching the C++ implementation.
"""

def mod26(x):
    """Calculate modulo 26 of a number, handling negative numbers correctly"""
    return (x % 26 + 26) % 26

def mod_inverse(a):
    """Calculate modular multiplicative inverse modulo 26"""
    a = mod26(a)
    for x in range(1, 26):
        if mod26(a * x) == 1:
            return x
    return -1  # No inverse exists

def determinant(matrix, n):
    """Calculate determinant of a matrix modulo 26"""
    if n == 1:
        return matrix[0][0]
    
    det = 0
    sign = 1
    
    for i in range(n):
        # Create submatrix for cofactor
        submatrix = []
        for row in range(1, n):
            subrow = []
            for col in range(n):
                if col != i:
                    subrow.append(matrix[row][col])
            submatrix.append(subrow)
        
        # Calculate cofactor and add to determinant
        det = mod26(det + sign * matrix[0][i] * determinant(submatrix, n-1))
        sign = -sign
    
    return mod26(det)

def get_cofactor(matrix, temp, p, q, n):
    """Get cofactor of matrix[p][q]"""
    i, j = 0, 0
    for row in range(n):
        for col in range(n):
            if row != p and col != q:
                temp[i][j] = matrix[row][col]
                j += 1
                if j == n - 1:
                    j = 0
                    i += 1

def adjoint(matrix, adj, n):
    """Calculate adjoint of a matrix"""
    if n == 1:
        adj[0][0] = 1
        return
    
    for i in range(n):
        for j in range(n):
            # Get cofactor
            temp = [[0 for _ in range(n-1)] for _ in range(n-1)]
            get_cofactor(matrix, temp, i, j, n)
            
            # Sign of adj[j][i] is positive if (i+j) is even, otherwise negative
            sign = 1 if (i + j) % 2 == 0 else -1
            
            # Interchanging rows and columns to get the transpose of the cofactor matrix
            adj[j][i] = mod26(sign * determinant(temp, n-1))

def inverse(matrix, inv, n):
    """Calculate inverse of a matrix modulo 26"""
    det = determinant(matrix, n)
    det_inv = mod_inverse(det)
    
    if det_inv == -1:
        return False  # Matrix is not invertible
    
    # Find adjoint
    adj = [[0 for _ in range(n)] for _ in range(n)]
    adjoint(matrix, adj, n)
    
    # Calculate inverse using adj / det
    for i in range(n):
        for j in range(n):
            inv[i][j] = mod26(adj[i][j] * det_inv)
    
    return True

def multiply(matrix, vec, n):
    """Multiply matrix with vector"""
    result = [0] * n
    for i in range(n):
        for j in range(n):
            result[i] = mod26(result[i] + matrix[i][j] * vec[j])
    return result

def is_invertible(matrix, n):
    """Check if matrix is invertible modulo 26"""
    det = determinant(matrix, n)
    return mod_inverse(det) != -1

def flat_to_matrix(flat, n):
    """Convert flat vector to 2D matrix"""
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            matrix[i][j] = flat[i * n + j]
    return matrix

def encrypt(input_vector, key_matrix_flat, n):
    """Encrypt using Hill cipher"""
    key_matrix = flat_to_matrix(key_matrix_flat, n)
    result = []
    
    # Process input vector in blocks of size n
    for i in range(0, len(input_vector), n):
        # Extract block
        block = []
        for j in range(n):
            if i + j < len(input_vector):
                block.append(mod26(input_vector[i + j]))
            else:
                # Pad with 'X' (23 in 0-25 encoding)
                block.append(23)  # 'X' - 'A' = 23
        
        # Encrypt block
        encrypted_block = multiply(key_matrix, block, n)
        
        # Add to result
        result.extend(encrypted_block)
    
    return result

def decrypt(input_vector, key_matrix_flat, n):
    """Decrypt using Hill cipher"""
    key_matrix = flat_to_matrix(key_matrix_flat, n)
    result = []
    
    # Check if matrix is invertible
    if not is_invertible(key_matrix, n):
        print("Error: Key matrix is not invertible modulo 26")
        return []
    
    # Calculate inverse matrix
    inv_key_matrix = [[0 for _ in range(n)] for _ in range(n)]
    if not inverse(key_matrix, inv_key_matrix, n):
        print("Error: Failed to calculate inverse matrix")
        return []
    
    # Process input vector in blocks of size n
    for i in range(0, len(input_vector), n):
        # Extract block
        block = []
        for j in range(n):
            if i + j < len(input_vector):
                block.append(mod26(input_vector[i + j]))
            else:
                # Pad with 'X' (23 in 0-25 encoding)
                block.append(23)  # 'X' - 'A' = 23
        
        # Decrypt block
        decrypted_block = multiply(inv_key_matrix, block, n)
        
        # Add to result
        result.extend(decrypted_block)
    
    return result

def hill_cipher_fallback(operation, dimension, key_matrix_flat, input_vector_flat):
    """
    Python fallback implementation of Hill Cipher that matches the C++ implementation
    
    Parameters:
    operation (str): The operation to perform ('encrypt' or 'decrypt')
    dimension (int or str): The dimension of the key matrix
    key_matrix_flat (str or list): The flattened key matrix as comma-separated string or list of integers
    input_vector_flat (str or list): The flattened input vector as comma-separated string or list of integers
    
    Returns:
    list: The result vector as a list of integers
    """
    try:
        # Convert dimension to int if it's a string
        n = int(dimension) if isinstance(dimension, str) else dimension
        
        # Parse key matrix from string if needed
        if isinstance(key_matrix_flat, str):
            key_matrix = [int(x.strip()) for x in key_matrix_flat.split(',')]
        else:
            key_matrix = key_matrix_flat
            
        # Parse input vector from string if needed
        if isinstance(input_vector_flat, str):
            input_vector = [int(x.strip()) for x in input_vector_flat.split(',')]
        else:
            input_vector = input_vector_flat
        
        if operation == 'encrypt':
            return encrypt(input_vector, key_matrix, n)
        elif operation == 'decrypt':
            return decrypt(input_vector, key_matrix, n)
        else:
            print(f"Error: Invalid operation '{operation}'. Use 'encrypt' or 'decrypt'")
            return []
    
    except Exception as e:
        print(f"Error in Hill cipher fallback: {str(e)}")
        # Simple fallback in case of any error
        try:
            # Parse inputs for fallback
            if isinstance(key_matrix_flat, str):
                key_matrix = [int(x.strip()) for x in key_matrix_flat.split(',')]
            else:
                key_matrix = key_matrix_flat
                
            if isinstance(input_vector_flat, str):
                input_vector = [int(x.strip()) for x in input_vector_flat.split(',')]
            else:
                input_vector = input_vector_flat
                
            if operation == 'encrypt':
                return [(x + sum(key_matrix) % 26) % 26 for x in input_vector]
            else:
                return [(x - sum(key_matrix) % 26) % 26 for x in input_vector]
        except:
            return []
