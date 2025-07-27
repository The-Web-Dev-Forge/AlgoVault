#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <algorithm>
#include <cstring>
#include <cstdint>

// Try to use OpenSSL if available
#ifdef __APPLE__
    #include <CommonCrypto/CommonHMAC.h>
    #define HAS_COMMONCRYPTO 1
#else
    #define HAS_COMMONCRYPTO 0
#endif

// Fallback system call method
#include <cstdlib>

std::string system_hmac_sha256(const std::string& message, const std::string& key) {
    // Use system openssl command as fallback
    std::string safe_message = message;
    std::string safe_key = key;
    
    // Escape single quotes in message and key
    size_t pos = 0;
    while ((pos = safe_message.find("'", pos)) != std::string::npos) {
        safe_message.replace(pos, 1, "'\"'\"'");
        pos += 5;
    }
    pos = 0;
    while ((pos = safe_key.find("'", pos)) != std::string::npos) {
        safe_key.replace(pos, 1, "'\"'\"'");
        pos += 5;
    }
    
    std::string command = "echo -n '" + safe_message + "' | openssl dgst -sha256 -hmac '" + safe_key + "' 2>/dev/null | awk '{print $2}'";
    
    FILE* pipe = popen(command.c_str(), "r");
    if (!pipe) return "";
    
    char buffer[128];
    std::string result = "";
    while (fgets(buffer, sizeof buffer, pipe) != NULL) {
        result += buffer;
    }
    pclose(pipe);
    
    // Remove newline
    if (!result.empty() && result.back() == '\n') {
        result.pop_back();
    }
    
    return result;
}

// HMAC Implementation
class HMAC {
private:
    static const int BLOCK_SIZE = 64; // SHA-256 block size
    static const int HASH_SIZE = 32;  // SHA-256 output size
    
    std::string bytesToHex(const std::vector<uint8_t>& bytes) {
        std::stringstream ss;
        ss << std::hex << std::setfill('0');
        for (auto byte : bytes) {
            ss << std::setw(2) << static_cast<int>(byte);
        }
        return ss.str();
    }
    
    std::vector<uint8_t> stringToBytes(const std::string& str) {
        return std::vector<uint8_t>(str.begin(), str.end());
    }
    
    std::vector<uint8_t> xorBytes(const std::vector<uint8_t>& a, const std::vector<uint8_t>& b) {
        std::vector<uint8_t> result(std::max(a.size(), b.size()));
        for (size_t i = 0; i < result.size(); ++i) {
            result[i] = (i < a.size() ? a[i] : 0) ^ (i < b.size() ? b[i] : 0);
        }
        return result;
    }
    
    std::vector<uint8_t> concatBytes(const std::vector<uint8_t>& a, const std::vector<uint8_t>& b) {
        std::vector<uint8_t> result = a;
        result.insert(result.end(), b.begin(), b.end());
        return result;
    }

#if HAS_COMMONCRYPTO
    std::vector<uint8_t> sha256Hash(const std::vector<uint8_t>& data) {
        std::vector<uint8_t> hash(CC_SHA256_DIGEST_LENGTH);
        CC_SHA256(data.data(), data.size(), hash.data());
        return hash;
    }
#endif

public:
    struct HMACResult {
        std::string hmac;
        bool success;
        std::string error;
        
        // Step-by-step details for visualization
        std::string originalKey;
        std::string processedKey;
        std::string keyAnalysis;
        std::string innerPad;
        std::string outerPad;
        std::string innerKeyMaterial;
        std::string outerKeyMaterial;
        std::string messageHex;
        std::string innerHash;
        std::string outerInput;
        std::string finalHmac;
        int blockSize;
        std::string algorithm;
    };
    
    HMACResult generateHMAC(const std::string& message, const std::string& key) {
        HMACResult result;
        result.success = false;
        result.originalKey = key;
        result.algorithm = "SHA-256";
        result.blockSize = BLOCK_SIZE;
        
        try {
#if HAS_COMMONCRYPTO
            // Use CommonCrypto on macOS for accurate HMAC calculation
            std::vector<uint8_t> hmac_result(CC_SHA256_DIGEST_LENGTH);
            
            CCHmac(kCCHmacAlgSHA256, 
                   key.c_str(), key.length(),
                   message.c_str(), message.length(),
                   hmac_result.data());
            
            result.hmac = bytesToHex(hmac_result);
            result.finalHmac = result.hmac;
            
            // Calculate step-by-step details for visualization
            std::vector<uint8_t> keyBytes = stringToBytes(key);
            std::vector<uint8_t> processedKey;
            
            if (keyBytes.size() > BLOCK_SIZE) {
                // Key is too long, hash it
                processedKey = sha256Hash(keyBytes);
                result.keyAnalysis = "Key length (" + std::to_string(keyBytes.size()) + 
                                   " bytes) exceeds block size (" + std::to_string(BLOCK_SIZE) + 
                                   " bytes). Key hashed to " + std::to_string(processedKey.size()) + " bytes.";
            } else {
                // Key is acceptable length
                processedKey = keyBytes;
                result.keyAnalysis = "Key length (" + std::to_string(keyBytes.size()) + 
                                   " bytes) is within block size (" + std::to_string(BLOCK_SIZE) + 
                                   " bytes). Using key directly.";
            }
            
            // Pad key to block size with zeros
            processedKey.resize(BLOCK_SIZE, 0x00);
            result.processedKey = bytesToHex(processedKey);
            
            // Create padding constants
            std::vector<uint8_t> ipad(BLOCK_SIZE, 0x36);
            std::vector<uint8_t> opad(BLOCK_SIZE, 0x5C);
            result.innerPad = bytesToHex(ipad);
            result.outerPad = bytesToHex(opad);
            
            // XOR key with inner pad
            std::vector<uint8_t> innerKeyMaterial = xorBytes(processedKey, ipad);
            result.innerKeyMaterial = bytesToHex(innerKeyMaterial);
            
            // Compute inner hash
            std::vector<uint8_t> messageBytes = stringToBytes(message);
            result.messageHex = bytesToHex(messageBytes);
            
            std::vector<uint8_t> innerInput = concatBytes(innerKeyMaterial, messageBytes);
            std::vector<uint8_t> innerHashBytes = sha256Hash(innerInput);
            result.innerHash = bytesToHex(innerHashBytes);
            
            // XOR key with outer pad
            std::vector<uint8_t> outerKeyMaterial = xorBytes(processedKey, opad);
            result.outerKeyMaterial = bytesToHex(outerKeyMaterial);
            
            // Compute final HMAC input
            std::vector<uint8_t> outerInputVec = concatBytes(outerKeyMaterial, innerHashBytes);
            result.outerInput = bytesToHex(outerInputVec);
            
            result.success = true;
            
#else
            // Fallback to system openssl command
            std::string fallback_result = system_hmac_sha256(message, key);
            if (!fallback_result.empty() && fallback_result.length() == 64) {
                result.hmac = fallback_result;
                result.finalHmac = fallback_result;
                result.success = true;
                result.keyAnalysis = "Using system OpenSSL command (fallback)";
                result.processedKey = "System call - details not available";
                result.innerPad = "System call - details not available";
                result.outerPad = "System call - details not available";
                result.innerKeyMaterial = "System call - details not available";
                result.outerKeyMaterial = "System call - details not available";
                result.messageHex = bytesToHex(stringToBytes(message));
                result.innerHash = "System call - details not available";
                result.outerInput = "System call - details not available";
            } else {
                result.error = "OpenSSL not available and no native implementation";
            }
#endif
            
        } catch (const std::exception& e) {
            result.error = std::string("HMAC generation failed: ") + e.what();
        } catch (...) {
            result.error = "Unknown error occurred during HMAC generation";
        }
        
        return result;
    }
    
    bool verifyHMAC(const std::string& message, const std::string& key, const std::string& expectedHmac) {
        HMACResult result = generateHMAC(message, key);
        if (!result.success) return false;
        
        // Convert both HMACs to lowercase for comparison
        std::string computed = result.hmac;
        std::string expected = expectedHmac;
        
        std::transform(computed.begin(), computed.end(), computed.begin(), ::tolower);
        std::transform(expected.begin(), expected.end(), expected.begin(), ::tolower);
        
        return computed == expected;
    }
};

// JSON output helper
void outputJSON(const HMAC::HMACResult& result) {
    std::cout << "{\n";
    std::cout << "  \"success\": " << (result.success ? "true" : "false") << ",\n";
    
    if (result.success) {
        std::cout << "  \"hmac\": \"" << result.hmac << "\",\n";
        std::cout << "  \"implementation\": \"C++\",\n";
        std::cout << "  \"steps\": {\n";
        std::cout << "    \"originalKey\": \"" << result.originalKey << "\",\n";
        std::cout << "    \"processedKey\": \"" << result.processedKey << "\",\n";
        std::cout << "    \"keyAnalysis\": \"" << result.keyAnalysis << "\",\n";
        std::cout << "    \"innerPad\": \"" << result.innerPad << "\",\n";
        std::cout << "    \"outerPad\": \"" << result.outerPad << "\",\n";
        std::cout << "    \"innerKeyMaterial\": \"" << result.innerKeyMaterial << "\",\n";
        std::cout << "    \"outerKeyMaterial\": \"" << result.outerKeyMaterial << "\",\n";
        std::cout << "    \"messageHex\": \"" << result.messageHex << "\",\n";
        std::cout << "    \"innerHash\": \"" << result.innerHash << "\",\n";
        std::cout << "    \"outerInput\": \"" << result.outerInput << "\",\n";
        std::cout << "    \"finalHmac\": \"" << result.finalHmac << "\",\n";
        std::cout << "    \"blockSize\": " << result.blockSize << ",\n";
        std::cout << "    \"algorithm\": \"" << result.algorithm << "\"\n";
        std::cout << "  }\n";
    } else {
        std::cout << "  \"error\": \"" << result.error << "\"\n";
    }
    
    std::cout << "}" << std::endl;
}

// Command line interface
int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "Usage: " << argv[0] << " <message> <key> [verify_hmac]" << std::endl;
        std::cout << "Examples:" << std::endl;
        std::cout << "  " << argv[0] << " \"Hello World\" \"secret_key\"" << std::endl;
        std::cout << "  " << argv[0] << " \"Hello World\" \"secret_key\" \"expected_hmac_value\"" << std::endl;
        return 1;
    }
    
    std::string message = argv[1];
    std::string key = argv[2];
    
    HMAC hmacGenerator;
    
    if (argc == 4) {
        // Verification mode
        std::string expectedHmac = argv[3];
        bool isValid = hmacGenerator.verifyHMAC(message, key, expectedHmac);
        std::cout << "{\"valid\": " << (isValid ? "true" : "false") << "}" << std::endl;
    } else {
        // Generation mode
        HMAC::HMACResult result = hmacGenerator.generateHMAC(message, key);
        outputJSON(result);
    }
    
    return 0;
}
