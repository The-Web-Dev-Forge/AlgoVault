#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <algorithm>
#include <cstring>
#include <cstdint>

// Try to use crypto libraries
#ifdef __APPLE__
    #include <CommonCrypto/CommonHMAC.h>
    #include <CommonCrypto/CommonDigest.h>
    #define HAS_COMMONCRYPTO 1
#else
    #define HAS_COMMONCRYPTO 0
    // Try OpenSSL on other platforms
    #ifdef __has_include
        #if __has_include(<openssl/hmac.h>)
            #include <openssl/hmac.h>
            #include <openssl/evp.h>
            #define HAS_OPENSSL 1
        #else
            #define HAS_OPENSSL 0
        #endif
    #else
        #define HAS_OPENSSL 0
    #endif
#endif

// Fallback system call method
#include <cstdlib>

std::string system_hmac(const std::string& message, const std::string& key, const std::string& algorithm) {
    // Use system openssl command as fallback for any algorithm
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
    
    // Convert algorithm to lowercase for openssl command
    std::string algo_lower = algorithm;
    std::transform(algo_lower.begin(), algo_lower.end(), algo_lower.begin(), ::tolower);
    
    std::string command = "echo -n '" + safe_message + "' | openssl dgst -" + algo_lower + " -hmac '" + safe_key + "' 2>/dev/null | awk '{print $2}'";
    
    FILE* pipe = popen(command.c_str(), "r");
    if (!pipe) return "";
    
    char buffer[256];
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

    // Get algorithm parameters
    void getAlgorithmParams(const std::string& algorithm, int& blockSize, int& digestSize) {
        std::string algo = algorithm;
        std::transform(algo.begin(), algo.end(), algo.begin(), ::tolower);
        
        if (algo == "md5") {
            blockSize = 64;
            digestSize = 16;
        } else if (algo == "sha1") {
            blockSize = 64;
            digestSize = 20;
        } else if (algo == "sha224") {
            blockSize = 64;
            digestSize = 28;
        } else if (algo == "sha256") {
            blockSize = 64;
            digestSize = 32;
        } else if (algo == "sha384") {
            blockSize = 128;
            digestSize = 48;
        } else if (algo == "sha512") {
            blockSize = 128;
            digestSize = 64;
        } else {
            // Default to SHA-256
            blockSize = 64;
            digestSize = 32;
        }
    }

#if HAS_COMMONCRYPTO
    CCHmacAlgorithm getCommonCryptoAlgorithm(const std::string& algorithm) {
        std::string algo = algorithm;
        std::transform(algo.begin(), algo.end(), algo.begin(), ::tolower);
        
        if (algo == "md5") return kCCHmacAlgMD5;
        else if (algo == "sha1") return kCCHmacAlgSHA1;
        else if (algo == "sha224") return kCCHmacAlgSHA224;
        else if (algo == "sha256") return kCCHmacAlgSHA256;
        else if (algo == "sha384") return kCCHmacAlgSHA384;
        else if (algo == "sha512") return kCCHmacAlgSHA512;
        
        return kCCHmacAlgSHA256; // Default
    }
    
    std::vector<uint8_t> sha256Hash(const std::vector<uint8_t>& data) {
        std::vector<uint8_t> hash(CC_SHA256_DIGEST_LENGTH);
        CC_SHA256(data.data(), data.size(), hash.data());
        return hash;
    }
    
    std::vector<uint8_t> computeHash(const std::vector<uint8_t>& data, const std::string& algorithm) {
        std::string algo = algorithm;
        std::transform(algo.begin(), algo.end(), algo.begin(), ::tolower);
        
        if (algo == "md5") {
            std::vector<uint8_t> hash(CC_MD5_DIGEST_LENGTH);
            CC_MD5(data.data(), data.size(), hash.data());
            return hash;
        } else if (algo == "sha1") {
            std::vector<uint8_t> hash(CC_SHA1_DIGEST_LENGTH);
            CC_SHA1(data.data(), data.size(), hash.data());
            return hash;
        } else if (algo == "sha224") {
            std::vector<uint8_t> hash(CC_SHA224_DIGEST_LENGTH);
            CC_SHA224(data.data(), data.size(), hash.data());
            return hash;
        } else if (algo == "sha256") {
            std::vector<uint8_t> hash(CC_SHA256_DIGEST_LENGTH);
            CC_SHA256(data.data(), data.size(), hash.data());
            return hash;
        } else if (algo == "sha384") {
            std::vector<uint8_t> hash(CC_SHA384_DIGEST_LENGTH);
            CC_SHA384(data.data(), data.size(), hash.data());
            return hash;
        } else if (algo == "sha512") {
            std::vector<uint8_t> hash(CC_SHA512_DIGEST_LENGTH);
            CC_SHA512(data.data(), data.size(), hash.data());
            return hash;
        }
        
        // Default to SHA256
        std::vector<uint8_t> hash(CC_SHA256_DIGEST_LENGTH);
        CC_SHA256(data.data(), data.size(), hash.data());
        return hash;
    }
#elif HAS_OPENSSL
    const EVP_MD* getOpenSSLDigest(const std::string& algorithm) {
        std::string algo = algorithm;
        std::transform(algo.begin(), algo.end(), algo.begin(), ::tolower);
        
        if (algo == "md5") return EVP_md5();
        else if (algo == "sha1") return EVP_sha1();
        else if (algo == "sha224") return EVP_sha224();
        else if (algo == "sha256") return EVP_sha256();
        else if (algo == "sha384") return EVP_sha384();
        else if (algo == "sha512") return EVP_sha512();
        
        return EVP_sha256(); // Default
    }
    
    std::vector<uint8_t> computeHash(const std::vector<uint8_t>& data, const std::string& algorithm) {
        const EVP_MD* md = getOpenSSLDigest(algorithm);
        unsigned int digestSize = EVP_MD_size(md);
        
        std::vector<uint8_t> hash(digestSize);
        unsigned int hashLen;
        
        EVP_MD_CTX* ctx = EVP_MD_CTX_new();
        EVP_DigestInit_ex(ctx, md, nullptr);
        EVP_DigestUpdate(ctx, data.data(), data.size());
        EVP_DigestFinal_ex(ctx, hash.data(), &hashLen);
        EVP_MD_CTX_free(ctx);
        
        hash.resize(hashLen);
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
    
    HMACResult generateHMAC(const std::string& message, const std::string& key, const std::string& algorithm = "sha256") {
        HMACResult result;
        result.success = false;
        result.originalKey = key;
        result.algorithm = algorithm;
        
        int blockSize, digestSize;
        getAlgorithmParams(algorithm, blockSize, digestSize);
        result.blockSize = blockSize;
        
        try {
#if HAS_COMMONCRYPTO
            // Use CommonCrypto on macOS for accurate HMAC calculation
            CCHmacAlgorithm hmacAlgo = getCommonCryptoAlgorithm(algorithm);
            std::vector<uint8_t> hmac_result(digestSize);
            
            CCHmac(hmacAlgo, 
                   key.c_str(), key.length(),
                   message.c_str(), message.length(),
                   hmac_result.data());
            
            result.hmac = bytesToHex(hmac_result);
            result.finalHmac = result.hmac;
            
            // Calculate step-by-step details for visualization
            std::vector<uint8_t> keyBytes = stringToBytes(key);
            std::vector<uint8_t> processedKey;
            
            if (keyBytes.size() > blockSize) {
                // Key is too long, hash it
                processedKey = computeHash(keyBytes, algorithm);
                result.keyAnalysis = "Key length (" + std::to_string(keyBytes.size()) + 
                                   " bytes) exceeds block size (" + std::to_string(blockSize) + 
                                   " bytes). Key hashed to " + std::to_string(processedKey.size()) + " bytes.";
            } else {
                // Key is acceptable length
                processedKey = keyBytes;
                result.keyAnalysis = "Key length (" + std::to_string(keyBytes.size()) + 
                                   " bytes) is within block size (" + std::to_string(blockSize) + 
                                   " bytes). Using key directly.";
            }
            
            // Pad key to block size with zeros
            processedKey.resize(blockSize, 0x00);
            result.processedKey = bytesToHex(processedKey);
            
            // Create padding constants
            std::vector<uint8_t> ipad(blockSize, 0x36);
            std::vector<uint8_t> opad(blockSize, 0x5C);
            result.innerPad = bytesToHex(ipad);
            result.outerPad = bytesToHex(opad);
            
            // XOR key with inner pad
            std::vector<uint8_t> innerKeyMaterial = xorBytes(processedKey, ipad);
            result.innerKeyMaterial = bytesToHex(innerKeyMaterial);
            
            // Compute inner hash
            std::vector<uint8_t> messageBytes = stringToBytes(message);
            result.messageHex = bytesToHex(messageBytes);
            
            std::vector<uint8_t> innerInput = concatBytes(innerKeyMaterial, messageBytes);
            std::vector<uint8_t> innerHashBytes = computeHash(innerInput, algorithm);
            result.innerHash = bytesToHex(innerHashBytes);
            
            // XOR key with outer pad
            std::vector<uint8_t> outerKeyMaterial = xorBytes(processedKey, opad);
            result.outerKeyMaterial = bytesToHex(outerKeyMaterial);
            
            // Compute final HMAC input
            std::vector<uint8_t> outerInputVec = concatBytes(outerKeyMaterial, innerHashBytes);
            result.outerInput = bytesToHex(outerInputVec);
            
            result.success = true;
            
#elif HAS_OPENSSL
            // Use OpenSSL for accurate HMAC calculation
            const EVP_MD* md = getOpenSSLDigest(algorithm);
            unsigned int hmacLen;
            
            std::vector<uint8_t> hmac_result(EVP_MD_size(md));
            
            unsigned char* digest = HMAC(md, key.c_str(), key.length(),
                                       reinterpret_cast<const unsigned char*>(message.c_str()), 
                                       message.length(), hmac_result.data(), &hmacLen);
            
            if (digest == nullptr) {
                result.error = "OpenSSL HMAC calculation failed";
                return result;
            }
            
            result.hmac = bytesToHex(hmac_result);
            result.finalHmac = result.hmac;
            
            // Calculate step-by-step details for visualization
            std::vector<uint8_t> keyBytes = stringToBytes(key);
            std::vector<uint8_t> processedKey;
            
            if (keyBytes.size() > blockSize) {
                processedKey = computeHash(keyBytes, algorithm);
                result.keyAnalysis = "Key length (" + std::to_string(keyBytes.size()) + 
                                   " bytes) exceeds block size (" + std::to_string(blockSize) + 
                                   " bytes). Key hashed to " + std::to_string(processedKey.size()) + " bytes.";
            } else {
                processedKey = keyBytes;
                result.keyAnalysis = "Key length (" + std::to_string(keyBytes.size()) + 
                                   " bytes) is within block size (" + std::to_string(blockSize) + 
                                   " bytes). Using key directly.";
            }
            
            processedKey.resize(blockSize, 0x00);
            result.processedKey = bytesToHex(processedKey);
            
            std::vector<uint8_t> ipad(blockSize, 0x36);
            std::vector<uint8_t> opad(blockSize, 0x5C);
            result.innerPad = bytesToHex(ipad);
            result.outerPad = bytesToHex(opad);
            
            std::vector<uint8_t> innerKeyMaterial = xorBytes(processedKey, ipad);
            result.innerKeyMaterial = bytesToHex(innerKeyMaterial);
            
            std::vector<uint8_t> messageBytes = stringToBytes(message);
            result.messageHex = bytesToHex(messageBytes);
            
            std::vector<uint8_t> innerInput = concatBytes(innerKeyMaterial, messageBytes);
            std::vector<uint8_t> innerHashBytes = computeHash(innerInput, algorithm);
            result.innerHash = bytesToHex(innerHashBytes);
            
            std::vector<uint8_t> outerKeyMaterial = xorBytes(processedKey, opad);
            result.outerKeyMaterial = bytesToHex(outerKeyMaterial);
            
            std::vector<uint8_t> outerInputVec = concatBytes(outerKeyMaterial, innerHashBytes);
            result.outerInput = bytesToHex(outerInputVec);
            
            result.success = true;
            
#else
            // Fallback to system openssl command
            std::string fallback_result = system_hmac(message, key, algorithm);
            if (!fallback_result.empty() && fallback_result.length() >= 32) {
                result.hmac = fallback_result;
                result.finalHmac = fallback_result;
                result.success = true;
                result.keyAnalysis = "Using system OpenSSL command (fallback) for " + algorithm;
                result.processedKey = "System call - details not available";
                result.innerPad = "System call - details not available";
                result.outerPad = "System call - details not available";
                result.innerKeyMaterial = "System call - details not available";
                result.outerKeyMaterial = "System call - details not available";
                result.messageHex = bytesToHex(stringToBytes(message));
                result.innerHash = "System call - details not available";
                result.outerInput = "System call - details not available";
            } else {
                result.error = "OpenSSL not available and no native implementation for " + algorithm;
            }
#endif
            
        } catch (const std::exception& e) {
            result.error = std::string("HMAC generation failed: ") + e.what();
        } catch (...) {
            result.error = "Unknown error occurred during HMAC generation";
        }
        
        return result;
    }
    
    bool verifyHMAC(const std::string& message, const std::string& key, const std::string& expectedHmac, const std::string& algorithm = "sha256") {
        HMACResult result = generateHMAC(message, key, algorithm);
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
        std::cout << "Usage: " << argv[0] << " <message> <key> [expected_hmac] [algorithm]" << std::endl;
        std::cout << "Algorithms: md5, sha1, sha224, sha256, sha384, sha512 (default: sha256)" << std::endl;
        std::cout << "Examples:" << std::endl;
        std::cout << "  " << argv[0] << " \"Hello World\" \"secret_key\"" << std::endl;
        std::cout << "  " << argv[0] << " \"Hello World\" \"secret_key\" \"\" \"sha512\"" << std::endl;
        std::cout << "  " << argv[0] << " \"Hello World\" \"secret_key\" \"expected_value\" \"md5\"" << std::endl;
        return 1;
    }
    
    std::string message = argv[1];
    std::string key = argv[2];
    std::string algorithm = "sha256"; // Default algorithm
    
    // Determine algorithm from arguments
    if (argc >= 5) {
        algorithm = argv[4];
    } else if (argc == 4) {
        // If 4 arguments, check if 3rd argument looks like an algorithm or HMAC
        std::string third_arg = argv[3];
        std::transform(third_arg.begin(), third_arg.end(), third_arg.begin(), ::tolower);
        if (third_arg == "md5" || third_arg == "sha1" || third_arg == "sha224" || 
            third_arg == "sha256" || third_arg == "sha384" || third_arg == "sha512") {
            // Third argument is algorithm, not expected HMAC
            algorithm = third_arg;
        }
    }
    
    HMAC hmacGenerator;
    
    if (argc >= 4 && argv[3][0] != '\0') {
        // Check if third argument is not an algorithm (i.e., it's expected HMAC)
        std::string third_arg = argv[3];
        std::transform(third_arg.begin(), third_arg.end(), third_arg.begin(), ::tolower);
        if (third_arg != "md5" && third_arg != "sha1" && third_arg != "sha224" && 
            third_arg != "sha256" && third_arg != "sha384" && third_arg != "sha512") {
            // Verification mode
            std::string expectedHmac = argv[3];
            bool isValid = hmacGenerator.verifyHMAC(message, key, expectedHmac, algorithm);
            std::cout << "{\"valid\": " << (isValid ? "true" : "false") << "}" << std::endl;
        } else {
            // Generation mode with algorithm specified
            HMAC::HMACResult result = hmacGenerator.generateHMAC(message, key, algorithm);
            outputJSON(result);
        }
    } else {
        // Generation mode
        HMAC::HMACResult result = hmacGenerator.generateHMAC(message, key, algorithm);
        outputJSON(result);
    }
    
    return 0;
}
