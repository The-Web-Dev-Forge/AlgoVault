/**
 * Caesar Cipher Implementation
 * Command line interface for Caesar Cipher encryption/decryption
 */

#include <iostream>
#include <string>
#include <cctype>
using namespace std;

/**
 * @class CaesarCipher
 * @brief This class implements the Caesar Cipher encryption and decryption.
 */
class CaesarCipher {
public:
    /**
     * @brief Encrypts a given text using the Caesar Cipher.
     * @param text The input text to be encrypted.
     * @param shift The number of positions to shift each letter.
     * @return A string representing the encrypted text.
     */
    string encrypt(string text, int shift) {
        string result = "";
        for (char c : text) {
            if (isalpha(c)) {
                char base = isupper(c) ? 'A' : 'a';
                result += char(base + (c - base + shift) % 26);
            } else {
                result += c;
            }
        }
        return result;
    }

    /**
     * @brief Decrypts a given text using the Caesar Cipher.
     * @param text The encrypted text to be decrypted.
     * @param shift The number of positions the text was shifted during encryption.
     * @return A string representing the decrypted text.
     */
    string decrypt(string text, int shift) {
        return encrypt(text, 26 - shift);
    }

    /**
     * @brief Performs brute force analysis on encrypted text.
     * @param text The encrypted text to analyze.
     * @return A string containing all possible decryptions with their shift values.
     */
    string bruteForceAnalysis(string text) {
        string result = "BRUTE FORCE ANALYSIS RESULTS:\n";
        result += "================================\n\n";
        
        for (int shift = 1; shift <= 25; shift++) {
            string decrypted = decrypt(text, shift);
            result += "Shift " + to_string(shift) + ": " + decrypted + "\n";
        }
        
        result += "\n================================\n";
        result += "Analyze the results above to find the most meaningful text.\n\n";
        result += "IF NO MEANINGFUL WORDS APPEAR:\n";
        result += "1. The text may be using a different cipher (try Vigenere instead)\n";
        result += "2. The original text might be in a different language\n";
        result += "3. The message might contain specialized terminology or code words\n";
        result += "4. Try looking for partial words or patterns that seem non-random\n";
        result += "5. The text might have been encrypted multiple times\n";
        result += "6. Try frequency analysis to identify common letters (E,T,A,O,I,N in English)";
        
        return result;
    }
};

int main(int argc, char* argv[]) {
    if (argc != 4) {
        cerr << "Usage: " << argv[0] << " <message> <shift> <operation>" << endl;
        cerr << "operation: encrypt, decrypt, or brute-force" << endl;
        return 1;
    }

    string message = argv[1];
    int shift = stoi(argv[2]);
    string operation = argv[3];

    CaesarCipher cipher;
    string result;

    if (operation == "encrypt") {
        result = cipher.encrypt(message, shift);
    } else if (operation == "decrypt") {
        result = cipher.decrypt(message, shift);
    } else if (operation == "brute-force") {
        result = cipher.bruteForceAnalysis(message);
    } else {
        cerr << "Invalid operation. Use 'encrypt', 'decrypt', or 'brute-force'" << endl;
        return 1;
    }

    cout << result << endl;
    return 0;
}
