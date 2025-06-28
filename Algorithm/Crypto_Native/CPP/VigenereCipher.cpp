/**
 * Vigenere Cipher Implementation
 * Command line interface for Vigenere Cipher encryption/decryption
 */

#include <iostream>
#include <string>
#include <cctype>
#include <vector>
#include <algorithm>
using namespace std;

/**
 * @class VigenereCipher
 * @brief This class implements the Vigenere Cipher encryption and decryption.
 */
class VigenereCipher {
public:
    /**
     * @brief Encrypts a given text using the Vigenere Cipher.
     * @param text The input text to be encrypted.
     * @param key The encryption key used for the Vigenere Cipher.
     * @return A string representing the encrypted text.
     */
    string encrypt(string text, string key) {
        string result = "";
        int keyIndex = 0;
        for (char c : text) {
            if (isalpha(c)) {
                char base = isupper(c) ? 'A' : 'a';
                int shift = toupper(key[keyIndex]) - 'A';
                result += char(base + (c - base + shift) % 26);
                keyIndex = (keyIndex + 1) % key.length();
            } else {
                result += c;
            }
        }
        return result;
    }

    /**
     * @brief Decrypts a given text using the Vigenere Cipher.
     * @param text The encrypted text to be decrypted.
     * @param key The encryption key used for the Vigenere Cipher.
     * @return A string representing the decrypted text.
     */
    string decrypt(string text, string key) {
        string result = "";
        int keyIndex = 0;
        for (char c : text) {
            if (isalpha(c)) {
                char base = isupper(c) ? 'A' : 'a';
                int shift = toupper(key[keyIndex]) - 'A';
                result += char(base + (c - base - shift + 26) % 26);
                keyIndex = (keyIndex + 1) % key.length();
            } else {
                result += c;
            }
        }
        return result;
    }

    /**
     * @brief Performs brute force analysis on encrypted text using common keywords.
     * @param text The encrypted text to analyze.
     * @return A string containing analysis results with common keyword attempts.
     */
    string bruteForceAnalysis(string text) {
        string result = "VIGENERE BRUTE FORCE ANALYSIS:\n";
        result += "================================\n\n";
        
        // Common keywords to try (most frequently used passwords/keys)
        vector<string> commonKeys = {
            // Single letters
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            
            // Common short words
            "KEY", "ABC", "THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL",
            "CAN", "HIS", "HER", "WAS", "ONE", "OUR", "OUT", "DAY", "GET", "HAS",
            
            // Common 4+ letter words
            "WORD", "CODE", "TEST", "HELP", "LOVE", "HOPE", "LIFE", "TIME", "WORK",
            "KEYS", "PASS", "USER", "ADMIN", "SECRET", "CIPHER", "CRYPTO", "SECURE",
            
            // Common patterns
            "ABCD", "ABCDE", "ABCDEF", "KEYKEY", "TESTTEST", "PASSWORD"
        };
        
        result += "Trying common keywords:\n";
        result += "------------------------\n";
        
        for (const string& testKey : commonKeys) {
            string decrypted = decrypt(text, testKey);
            
            // Only show first 100 characters for readability
            string preview = decrypted.length() > 100 ? 
                           decrypted.substr(0, 100) + "..." : decrypted;
            
            result += "Key '" + testKey + "' (" + to_string(testKey.length()) + " chars): " + preview + "\n";
        }
        
        result += "\n================================\n";
        result += "ANALYSIS TIPS:\n";
        result += "1. Look for readable English text\n";
        result += "2. Check for common words like 'THE', 'AND', 'A'\n";
        result += "3. Meaningful results indicate the correct key\n";
        result += "4. If no results look good, the key might be longer or unusual\n\n";
        
        result += "IF NO MEANINGFUL WORDS APPEAR:\n";
        result += "1. Try manual key guessing based on context/theme of the message\n";
        result += "2. The key might be longer than tested here (try 5+ letters)\n";
        result += "3. Try analyzing with Kasiski examination for key length\n";
        result += "4. Consider using frequency analysis to determine likely key letters\n";
        result += "5. The text may be using a different cipher or multiple layers of encryption\n";
        result += "6. For very short texts, statistical analysis may not be reliable\n";
        
        return result;
    }

    /**
     * @brief Performs frequency analysis on the encrypted text.
     * @param text The encrypted text to analyze.
     * @return A string containing frequency analysis results.
     */
    string frequencyAnalysis(string text) {
        string result = "VIGENERE FREQUENCY ANALYSIS:\n";
        result += "==============================\n\n";
        
        // Count letter frequencies
        vector<int> freq(26, 0);
        int totalLetters = 0;
        
        for (char c : text) {
            if (isalpha(c)) {
                freq[toupper(c) - 'A']++;
                totalLetters++;
            }
        }
        
        result += "Letter frequencies:\n";
        for (int i = 0; i < 26; i++) {
            char letter = 'A' + i;
            double percentage = totalLetters > 0 ? (double)freq[i] * 100.0 / totalLetters : 0.0;
            result += letter;
            result += ": " + to_string(freq[i]) + " (" + to_string(percentage).substr(0, 4) + "%)\n";
        }
        
        result += "\nCommon English letter frequencies:\n";
        result += "E: 12.7%, T: 9.1%, A: 8.2%, O: 7.5%, I: 7.0%, N: 6.7%\n";
        result += "S: 6.3%, H: 6.1%, R: 6.0%, D: 4.3%, L: 4.0%, C: 2.8%\n\n";
        
        result += "Analysis Tips:\n";
        result += "1. Compare the frequencies above with typical English\n";
        result += "2. Large deviations indicate the encryption method or key length\n";
        result += "3. In Vigenere ciphers, frequency patterns are flattened compared to Caesar\n";
        result += "4. For longer texts, try to estimate key length using Index of Coincidence\n\n";
        
        result += "INTERPRETING RESULTS:\n";
        result += "- If frequencies look random, a polyalphabetic cipher like Vigenere is likely\n";
        result += "- If one letter appears much more often than others, try Caesar cipher\n";
        result += "- If frequencies match English, the text might not be encrypted\n";
        result += "- If short text, frequencies may not be statistically significant\n";
        
        return result;
    }
};

int main(int argc, char* argv[]) {
    if (argc < 4) {
        cerr << "Usage: " << argv[0] << " <operation> <message> <keyword>" << endl;
        cerr << "operation: encrypt, decrypt, brute-force, or frequency" << endl;
        return 1;
    }

    string operation = argv[1];
    string message = argv[2];
    string keyword = argv[3];

    VigenereCipher cipher;
    string result;

    if (operation == "encrypt") {
        result = cipher.encrypt(message, keyword);
    } else if (operation == "decrypt") {
        result = cipher.decrypt(message, keyword);
    } else if (operation == "brute-force") {
        result = cipher.bruteForceAnalysis(message);
    } else if (operation == "frequency") {
        result = cipher.frequencyAnalysis(message);
    } else {
        cerr << "Invalid operation. Use 'encrypt', 'decrypt', 'brute-force', or 'frequency'" << endl;
        return 1;
    }

    cout << result << endl;
    return 0;
}
