#include <iostream>
#include <string>
#include <cstring>
#include <iomanip>
#include <stdint.h>

/**
 * SHA-512 Implementation - Corrected Version
 * Based on NIST FIPS 180-4 specification
*/

/**
 * Right rotate function for 64-bit values
 */
#define ROTR64(x, n) (((x) >> (n)) | ((x) << (64 - (n))))

/**
 * SHA-512 auxiliary functions
*/
#define Ch(x, y, z)    (((x) & (y)) ^ (~(x) & (z)))
#define Maj(x, y, z)   (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define Sigma0(x)      (ROTR64(x, 28) ^ ROTR64(x, 34) ^ ROTR64(x, 39))
#define Sigma1(x)      (ROTR64(x, 14) ^ ROTR64(x, 18) ^ ROTR64(x, 41))
#define sigma0(x)      (ROTR64(x, 1) ^ ROTR64(x, 8) ^ ((x) >> 7))
#define sigma1(x)      (ROTR64(x, 19) ^ ROTR64(x, 61) ^ ((x) >> 6))

/**
 * SHA-512 constants (first 64 bits of the fractional parts of the cube roots of the first 80 primes)
 */
static const uint64_t K[80] = {
    0x428a2f98d728ae22ULL, 0x7137449123ef65cdULL, 0xb5c0fbcfec4d3b2fULL, 0xe9b5dba58189dbbcULL,
    0x3956c25bf348b538ULL, 0x59f111f1b605d019ULL, 0x923f82a4af194f9bULL, 0xab1c5ed5da6d8118ULL,
    0xd807aa98a3030242ULL, 0x12835b0145706fbeULL, 0x243185be4ee4b28cULL, 0x550c7dc3d5ffb4e2ULL,
    0x72be5d74f27b896fULL, 0x80deb1fe3b1696b1ULL, 0x9bdc06a725c71235ULL, 0xc19bf174cf692694ULL,
    0xe49b69c19ef14ad2ULL, 0xefbe4786384f25e3ULL, 0x0fc19dc68b8cd5b5ULL, 0x240ca1cc77ac9c65ULL,
    0x2de92c6f592b0275ULL, 0x4a7484aa6ea6e483ULL, 0x5cb0a9dcbd41fbd4ULL, 0x76f988da831153b5ULL,
    0x983e5152ee66dfabULL, 0xa831c66d2db43210ULL, 0xb00327c898fb213fULL, 0xbf597fc7beef0ee4ULL,
    0xc6e00bf33da88fc2ULL, 0xd5a79147930aa725ULL, 0x06ca6351e003826fULL, 0x142929670a0e6e70ULL,
    0x27b70a8546d22ffcULL, 0x2e1b21385c26c926ULL, 0x4d2c6dfc5ac42aedULL, 0x53380d139d95b3dfULL,
    0x650a73548baf63deULL, 0x766a0abb3c77b2a8ULL, 0x81c2c92e47edaee6ULL, 0x92722c851482353bULL,
    0xa2bfe8a14cf10364ULL, 0xa81a664bbc423001ULL, 0xc24b8b70d0f89791ULL, 0xc76c51a30654be30ULL,
    0xd192e819d6ef5218ULL, 0xd69906245565a910ULL, 0xf40e35855771202aULL, 0x106aa07032bbd1b8ULL,
    0x19a4c116b8d2d0c8ULL, 0x1e376c085141ab53ULL, 0x2748774cdf8eeb99ULL, 0x34b0bcb5e19b48a8ULL,
    0x391c0cb3c5c95a63ULL, 0x4ed8aa4ae3418acbULL, 0x5b9cca4f7763e373ULL, 0x682e6ff3d6b2b8a3ULL,
    0x748f82ee5defb2fcULL, 0x78a5636f43172f60ULL, 0x84c87814a1f0ab72ULL, 0x8cc702081a6439ecULL,
    0x90befffa23631e28ULL, 0xa4506cebde82bde9ULL, 0xbef9a3f7b2c67915ULL, 0xc67178f2e372532bULL,
    0xca273eceea26619cULL, 0xd186b8c721c0c207ULL, 0xeada7dd6cde0eb1eULL, 0xf57d4f7fee6ed178ULL,
    0x06f067aa72176fbaULL, 0x0a637dc5a2c898a6ULL, 0x113f9804bef90daeULL, 0x1b710b35131c471bULL,
    0x28db77f523047d84ULL, 0x32caab7b40c72493ULL, 0x3c9ebe0a15c9bebcULL, 0x431d67c49c100d4cULL,
    0x4cc5d4becb3e42b6ULL, 0x597f299cfc657e2aULL, 0x5fcb6fab3ad6faecULL, 0x6c44198c4a475817ULL
};

/**
 * Convert bytes to 64-bit word (big-endian)
 */
uint64_t bytes_to_word64(const uint8_t* bytes) {
    return ((uint64_t)bytes[0] << 56) |
           ((uint64_t)bytes[1] << 48) |
           ((uint64_t)bytes[2] << 40) |
           ((uint64_t)bytes[3] << 32) |
           ((uint64_t)bytes[4] << 24) |
           ((uint64_t)bytes[5] << 16) |
           ((uint64_t)bytes[6] << 8) |
           ((uint64_t)bytes[7]);
}

/**
 * Convert 64-bit word to bytes (big-endian)
 */
void word64_to_bytes(uint64_t word, uint8_t* bytes) {
    bytes[0] = (word >> 56) & 0xFF;
    bytes[1] = (word >> 48) & 0xFF;
    bytes[2] = (word >> 40) & 0xFF;
    bytes[3] = (word >> 32) & 0xFF;
    bytes[4] = (word >> 24) & 0xFF;
    bytes[5] = (word >> 16) & 0xFF;
    bytes[6] = (word >> 8) & 0xFF;
    bytes[7] = word & 0xFF;
}

/**
 * Process a single 1024-bit block
 */
void sha512_process_block(uint64_t H[8], const uint8_t block[128]) {
    uint64_t W[80];
    uint64_t a, b, c, d, e, f, g, h;
    uint64_t T1, T2;
    int t;

    // Prepare message schedule W
    // First 16 words are directly from the message block
    for (t = 0; t < 16; t++) {
        W[t] = bytes_to_word64(&block[t * 8]);
    }

    // Extend to 80 words
    for (t = 16; t < 80; t++) {
        W[t] = sigma1(W[t-2]) + W[t-7] + sigma0(W[t-15]) + W[t-16];
    }

    // Initialize working variables
    a = H[0]; b = H[1]; c = H[2]; d = H[3];
    e = H[4]; f = H[5]; g = H[6]; h = H[7];

    // Main loop
    for (t = 0; t < 80; t++) {
        T1 = h + Sigma1(e) + Ch(e, f, g) + K[t] + W[t];
        T2 = Sigma0(a) + Maj(a, b, c);
        h = g;
        g = f;
        f = e;
        e = d + T1;
        d = c;
        c = b;
        b = a;
        a = T1 + T2;
    }

    // Add compressed chunk to current hash value
    H[0] += a; H[1] += b; H[2] += c; H[3] += d;
    H[4] += e; H[5] += f; H[6] += g; H[7] += h;
}

/**
 * Main SHA-512 function
 */
void sha512(const std::string& message, uint8_t digest[64]) {
    // Initial hash values (first 64 bits of fractional parts of square roots of first 8 primes)
    uint64_t H[8] = {
        0x6a09e667f3bcc908ULL, 0xbb67ae8584caa73bULL, 0x3c6ef372fe94f82bULL, 0xa54ff53a5f1d36f1ULL,
        0x510e527fade682d1ULL, 0x9b05688c2b3e6c1fULL, 0x1f83d9abfb41bd6bULL, 0x5be0cd19137e2179ULL
    };

    uint64_t message_len = message.length();
    uint64_t bit_len = message_len * 8;

    // Calculate padding
    uint64_t padding_len = (896 - (bit_len + 1) % 1024) % 1024;
    uint64_t total_len = bit_len + 1 + padding_len + 128; // +128 for length field
    uint64_t total_bytes = total_len / 8;

    // Create padded message
    uint8_t* padded_message = new uint8_t[total_bytes];
    memset(padded_message, 0, total_bytes);

    // Copy original message
    memcpy(padded_message, message.c_str(), message_len);

    // Add padding bit (0x80 = 10000000 in binary)
    padded_message[message_len] = 0x80;

    // Add length as 128-bit big-endian integer (we use only lower 64 bits)
    // Upper 64 bits are 0 (already set by memset)
    // Lower 64 bits go at the end
    word64_to_bytes(bit_len, &padded_message[total_bytes - 8]);

    // Process message in 1024-bit (128-byte) blocks
    for (uint64_t i = 0; i < total_bytes; i += 128) {
        sha512_process_block(H, &padded_message[i]);
    }

    // Convert hash values to bytes
    for (int i = 0; i < 8; i++) {
        word64_to_bytes(H[i], &digest[i * 8]);
    }

    delete[] padded_message;
}

// Modified main to accept command line input for use with Django
int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <message>" << std::endl;
        return 1;
    }
    
    std::string input = argv[1];
    uint8_t hash[64];
    sha512(input, hash);
    
    // Output hash as a hex string
    for (int i = 0; i < 64; i++) {
        std::cout << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
    }
    std::cout << std::endl;
    
    return 0;
}
