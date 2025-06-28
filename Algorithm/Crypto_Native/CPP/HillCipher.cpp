/**
 * Hill Cipher Implementation
 * Command line interface for Hill Cipher encryption/decryption
 */

#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <cctype>
#include <algorithm>
#include <sstream>
using namespace std;

/**
 * @class HillCipher
 * @brief This class implements the Hill Cipher encryption and decryption.
 */
class HillCipher {
private:
    int n; // Matrix dimension

    /**
     * @brief Calculates modulo 26 of a number, handling negative numbers
     * @param x The number to calculate modulo for
     * @return The positive modulo 26 result
     */
    int mod26(int x) {
        return (x % 26 + 26) % 26;
    }

    /**
     * @brief Calculates the modular multiplicative inverse modulo 26
     * @param a The number to find inverse for
     * @return The modular multiplicative inverse, or -1 if it doesn't exist
     */
    int modInverse(int a) {
        a = mod26(a);
        for (int x = 1; x < 26; x++) {
            if (mod26(a * x) == 1) {
                return x;
            }
        }
        return -1;
    }

    /**
     * @brief Performs matrix multiplication with a vector
     * @param matrix The matrix to multiply
     * @param vec The vector to multiply with
     * @return Resulting vector after multiplication
     */
    vector<int> multiply(const vector<vector<int>>& matrix, const vector<int>& vec) {
        vector<int> result(n);
        for (int i = 0; i < n; i++) {
            result[i] = 0;
            for (int j = 0; j < n; j++) {
                result[i] += matrix[i][j] * vec[j];
            }
            result[i] = mod26(result[i]);
        }
        return result;
    }

    /**
     * @brief Calculates the cofactor of a matrix element
     * @param matrix The input matrix
     * @param temp Temporary matrix for cofactor calculation
     * @param p Row index
     * @param q Column index
     * @param size Matrix size
     */
    void getCofactor(const vector<vector<int>>& matrix, vector<vector<int>>& temp, int p, int q, int size) {
        int i = 0, j = 0;
        for (int row = 0; row < size; row++) {
            for (int col = 0; col < size; col++) {
                if (row != p && col != q) {
                    temp[i][j++] = matrix[row][col];
                    if (j == size - 1) {
                        j = 0;
                        i++;
                    }
                }
            }
        }
    }

    /**
     * @brief Calculates the determinant of a matrix
     * @param matrix The input matrix
     * @param size Matrix size
     * @return The determinant modulo 26
     */
    int determinant(const vector<vector<int>>& matrix, int size) {
        if (size == 1) {
            return matrix[0][0];
        }
        int det = 0;
        vector<vector<int>> temp(size - 1, vector<int>(size - 1));
        int sign = 1;
        for (int i = 0; i < size; i++) {
            getCofactor(matrix, temp, 0, i, size);
            det = mod26(det + sign * matrix[0][i] * determinant(temp, size - 1));
            sign = -sign;
        }
        return mod26(det);
    }

    /**
     * @brief Calculates the adjoint matrix
     * @param matrix The input matrix
     * @param adj Output parameter for the adjoint matrix
     */
    void adjoint(const vector<vector<int>>& matrix, vector<vector<int>>& adj) {
        if (n == 1) {
            adj[0][0] = 1;
            return;
        }
        vector<vector<int>> temp(n, vector<int>(n));
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                getCofactor(matrix, temp, i, j, n);
                int sign = ((i + j) % 2 == 0) ? 1 : -1;
                adj[j][i] = mod26(sign * determinant(temp, n - 1));
            }
        }
    }

    /**
     * @brief Calculates the inverse matrix modulo 26
     * @param matrix The input matrix
     * @param inv Output parameter for the inverse matrix
     * @return true if matrix is invertible, false otherwise
     */
    bool inverse(const vector<vector<int>>& matrix, vector<vector<int>>& inv) {
        int det = determinant(matrix, n);
        int detInv = modInverse(det);
        if (detInv == -1) return false;
        
        vector<vector<int>> adj(n, vector<int>(n));
        adjoint(matrix, adj);
        
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                inv[i][j] = mod26(adj[i][j] * detInv);
            }
        }
        return true;
    }

    /**
     * @brief Checks if a key matrix is invertible modulo 26
     * @param matrix The key matrix to check
     * @return true if matrix is invertible, false otherwise
     */
    bool isInvertible(const vector<vector<int>>& matrix) {
        int det = determinant(matrix, n);
        return modInverse(det) != -1;
    }

    /**
     * @brief Converts a flat vector to a 2D matrix
     * @param flatMatrix The flat vector
     * @param dimension The dimension of the matrix
     * @return 2D matrix representation
     */
    vector<vector<int>> flatToMatrix(const vector<int>& flatMatrix) {
        vector<vector<int>> matrix(n, vector<int>(n));
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                matrix[i][j] = flatMatrix[i * n + j];
            }
        }
        return matrix;
    }

    /**
     * @brief Converts a 2D matrix to a flat vector
     * @param matrix The 2D matrix
     * @return flat vector representation
     */
    vector<int> matrixToFlat(const vector<vector<int>>& matrix) {
        vector<int> flat;
        for (const auto& row : matrix) {
            flat.insert(flat.end(), row.begin(), row.end());
        }
        return flat;
    }

public:
    /**
     * @brief Constructor with dimension parameter
     * @param dimension The dimension of the key matrix
     */
    HillCipher(int dimension) : n(dimension) {}

    /**
     * @brief Converts a string to key matrix
     * @param keyWord The key word
     * @return Flat vector representing the key matrix
     */
    vector<int> keyWordToMatrix(const string& keyWord) {
        string key = keyWord;
        // Convert to uppercase
        transform(key.begin(), key.end(), key.begin(), ::toupper);
        // Remove non-alphabetic characters
        key.erase(remove_if(key.begin(), key.end(), [](char c) { return !isalpha(c); }), key.end());
        
        // Pad with 'X' if needed
        int needed = n * n;
        if (key.length() < needed) {
            key.append(needed - key.length(), 'X');
        } else if (key.length() > needed) {
            key = key.substr(0, needed);
        }
        
        // Convert to numerical values (A=0, B=1, ..., Z=25)
        vector<int> keyMatrix;
        for (char c : key) {
            keyMatrix.push_back(c - 'A');
        }
        
        return keyMatrix;
    }

    /**
     * @brief Converts text to numeric vector
     * @param text The input text
     * @return Vector of numeric values (A=0, B=1, ..., Z=25)
     */
    vector<int> textToVector(const string& text) {
        vector<int> result;
        string processed = text;
        
        // Convert to uppercase
        transform(processed.begin(), processed.end(), processed.begin(), ::toupper);
        
        for (char c : processed) {
            if (isalpha(c)) {
                result.push_back(c - 'A');
            }
        }
        return result;
    }

    /**
     * @brief Converts numeric vector to text
     * @param vec The numeric vector
     * @return Text representation
     */
    string vectorToText(const vector<int>& vec) {
        string result;
        for (int val : vec) {
            result += (char)(mod26(val) + 'A');
        }
        return result;
    }

    /**
     * @brief Encrypts a given vector using the Hill Cipher.
     * @param inputVector The input vector to be encrypted.
     * @param keyMatrixFlat The flat key matrix used for encryption.
     * @return A vector representing the encrypted values.
     */
    vector<int> encrypt(const vector<int>& inputVector, const vector<int>& keyMatrixFlat) {
        vector<vector<int>> keyMatrix = flatToMatrix(keyMatrixFlat);
        vector<int> result;
        
        // Process input vector in blocks of size 'n'
        for (size_t i = 0; i < inputVector.size(); i += n) {
            // Extract a block from input vector
            vector<int> block;
            for (int j = 0; j < n && i + j < inputVector.size(); j++) {
                block.push_back(mod26(inputVector[i + j]));
            }
            
            // Pad the block with zeros if needed
            while (block.size() < (size_t)n) {
                block.push_back('X' - 'A'); // Pad with 'X' (value 23) instead of 0 (A)
            }
            
            // Encrypt the block
            vector<int> encryptedBlock = multiply(keyMatrix, block);
            
            // Add encrypted block to result
            result.insert(result.end(), encryptedBlock.begin(), encryptedBlock.end());
        }
        
        return result;
    }

    /**
     * @brief Decrypts a given vector using the Hill Cipher.
     * @param inputVector The encrypted vector to be decrypted.
     * @param keyMatrixFlat The flat key matrix used for encryption.
     * @return A vector representing the decrypted values.
     */
    vector<int> decrypt(const vector<int>& inputVector, const vector<int>& keyMatrixFlat) {
        vector<vector<int>> keyMatrix = flatToMatrix(keyMatrixFlat);
        vector<int> result;
        
        // Check if the key matrix is invertible
        if (!isInvertible(keyMatrix)) {
            cerr << "Error: Key matrix is not invertible modulo 26. Decryption is not possible." << endl;
            return result; // Return empty vector
        }
        
        // Calculate inverse of key matrix
        vector<vector<int>> invKeyMatrix(n, vector<int>(n));
        if (!inverse(keyMatrix, invKeyMatrix)) {
            cerr << "Error: Failed to calculate inverse matrix." << endl;
            return result; // Return empty vector
        }
        
        // Process input vector in blocks of size 'n'
        for (size_t i = 0; i < inputVector.size(); i += n) {
            // Extract a block from input vector
            vector<int> block;
            for (int j = 0; j < n && i + j < inputVector.size(); j++) {
                block.push_back(mod26(inputVector[i + j]));
            }
            
            // Pad the block with zeros if needed
            while (block.size() < (size_t)n) {
                block.push_back('X' - 'A'); // Pad with 'X' (value 23) instead of 0 (A)
            }
            
            // Decrypt the block
            vector<int> decryptedBlock = multiply(invKeyMatrix, block);
            
            // Add decrypted block to result
            result.insert(result.end(), decryptedBlock.begin(), decryptedBlock.end());
        }
        
        return result;
    }

    /**
     * @brief Encrypts text using Hill cipher
     * @param text The text to encrypt
     * @param keyMatrixFlat The flat key matrix
     * @return The encrypted text
     */
    string encryptText(const string& text, const vector<int>& keyMatrixFlat) {
        // Convert text to vector
        vector<int> inputVector = textToVector(text);
        
        // Store original length to handle padding later
        int originalLength = inputVector.size();
        
        // Pad if needed
        while (inputVector.size() % n != 0) {
            inputVector.push_back('X' - 'A');  // Pad with 'X'
        }
        
        // Encrypt
        vector<int> encrypted = encrypt(inputVector, keyMatrixFlat);
        
        // Convert back to text
        return vectorToText(encrypted);
    }

    /**
     * @brief Decrypts text using Hill cipher
     * @param text The text to decrypt
     * @param keyMatrixFlat The flat key matrix
     * @param originalLength The original length of the unpadded plaintext (if known)
     * @return The decrypted text
     */
    string decryptText(const string& text, const vector<int>& keyMatrixFlat, int originalLength = -1) {
        // Convert text to vector
        vector<int> inputVector = textToVector(text);
        
        // Pad if needed
        while (inputVector.size() % n != 0) {
            inputVector.push_back('X' - 'A');  // Pad with 'X'
        }
        
        // Decrypt
        vector<int> decrypted = decrypt(inputVector, keyMatrixFlat);
        
        // Convert back to text
        string result = vectorToText(decrypted);
        
        // Trim padding if original length is provided
        if (originalLength > 0 && originalLength < (int)result.length()) {
            result = result.substr(0, originalLength);
        } else {
            // If original length is not provided, try to remove trailing 'X' padding
            while (!result.empty() && result.back() == 'X') {
                result.pop_back();
            }
        }
        
        return result;
    }
};

/**
 * @brief Processes text input using Hill Cipher
 * @param text The input text
 * @param keyMatrixFlat The flat key matrix used for processing
 * @param dimension The dimension of the key matrix
 * @param operation The operation (encrypt/decrypt)
 * @return The processed text
 */
string processText(const string& text, const vector<int>& keyMatrixFlat, int dimension, const string& operation) {
    HillCipher cipher(dimension);
    
    // Store original length to handle padding correctly
    string cleanText;
    for (char c : text) {
        if (isalpha(c)) {
            cleanText += c;
        }
    }
    int originalLength = cleanText.length();
    
    // Process based on operation
    if (operation == "encrypt") {
        return cipher.encryptText(text, keyMatrixFlat);
    } else { // decrypt
        return cipher.decryptText(text, keyMatrixFlat, originalLength);
    }
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        cerr << "Usage: " << argv[0] << " <operation> <dimension> [--key-word <word> | <key_matrix_elements...>] [--text <input_text> | <input_vector_elements...>]" << endl;
        cerr << "operation: encrypt or decrypt" << endl;
        return 1;
    }

    string operation = argv[1];
    int dimension = stoi(argv[2]);
    
    HillCipher cipher(dimension);
    vector<int> keyMatrix;
    vector<int> inputVector;
    string inputText = "";
    bool useTextInput = false;
    bool useWordKey = false;
    string keyWord = "";
    
    // Parse arguments to handle both numeric and text inputs
    int argIndex = 3;
    while (argIndex < argc) {
        string arg = argv[argIndex];
        
        if (arg == "--key-word") {
            // Handle key word input
            if (argIndex + 1 < argc) {
                keyWord = argv[argIndex + 1];
                useWordKey = true;
                argIndex += 2;
            } else {
                cerr << "Missing key word after --key-word." << endl;
                return 1;
            }
        } else if (arg == "--text") {
            // Handle text input
            if (argIndex + 1 < argc) {
                inputText = argv[argIndex + 1];
                useTextInput = true;
                argIndex += 2;
            } else {
                cerr << "Missing text after --text." << endl;
                return 1;
            }
        } else {
            // Handle numeric input
            if (!useWordKey && keyMatrix.size() < dimension * dimension) {
                // Still collecting key matrix elements
                keyMatrix.push_back(stoi(arg));
            } else if (!useTextInput) {
                // Collecting input vector elements
                inputVector.push_back(stoi(arg));
            }
            argIndex++;
        }
    }
    
    // If using word key, convert it to matrix
    if (useWordKey) {
        keyMatrix = cipher.keyWordToMatrix(keyWord);
    }
    
    // Validate we have a complete key matrix
    if (keyMatrix.size() != dimension * dimension) {
        cerr << "Incomplete key matrix. Got " << keyMatrix.size() << " elements, expected " << (dimension * dimension) << "." << endl;
        return 1;
    }
    
    // Process based on input type
    if (useTextInput) {
        // Text-based processing
        string resultText = processText(inputText, keyMatrix, dimension, operation);
        
        // Output as text
        cout << resultText;
    } else {
        // Pure numeric processing
        if (inputVector.empty()) {
            cerr << "No input vector elements provided." << endl;
            return 1;
        }
        
        vector<int> result;
        if (operation == "encrypt") {
            result = cipher.encrypt(inputVector, keyMatrix);
        } else if (operation == "decrypt") {
            result = cipher.decrypt(inputVector, keyMatrix);
        } else {
            cerr << "Invalid operation. Use 'encrypt' or 'decrypt'" << endl;
            return 1;
        }
        
        // Output numeric result
        for (int val : result) {
            cout << val << " ";
        }
    }
    
    cout << endl;
    return 0;
}
