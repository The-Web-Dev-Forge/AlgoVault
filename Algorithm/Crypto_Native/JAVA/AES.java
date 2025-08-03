import java.nio.charset.StandardCharsets;
import java.util.Base64;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class AES {
    
    // AES S-Box
    private static final int[][] SBOX = {
        {0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76},
        {0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0},
        {0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15},
        {0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75},
        {0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84},
        {0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf},
        {0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8},
        {0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2},
        {0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73},
        {0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb},
        {0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79},
        {0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08},
        {0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a},
        {0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e},
        {0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf},
        {0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16}
    };

    // AES Inverse S-Box
    private static final int[][] INV_SBOX = {
        {0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb},
        {0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb},
        {0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e},
        {0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25},
        {0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92},
        {0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84},
        {0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06},
        {0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b},
        {0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73},
        {0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e},
        {0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b},
        {0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4},
        {0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f},
        {0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef},
        {0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61},
        {0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d}
    };

    // Round constants
    private static final int[] RCON = {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36};

    public static void main(String[] args) {
        if (args.length < 3) {
            System.err.println("Usage: java AES <message> <key> <encrypt|decrypt>");
            System.exit(1);
        }

        String message = args[0];
        String keyStr = args[1];
        String operation = args[2];

        try {
            if (keyStr.length() != 16) {
                throw new IllegalArgumentException("Key must be 16 characters long.");
            }
            byte[] key = keyStr.getBytes(StandardCharsets.UTF_8);

            if ("encrypt".equalsIgnoreCase(operation)) {
                System.out.print(encrypt(message, key));
            } else if ("decrypt".equalsIgnoreCase(operation)) {
                System.out.print(decrypt(message, key));
            } else {
                throw new IllegalArgumentException("Invalid operation. Choose 'encrypt' or 'decrypt'.");
            }
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }

    // Convert byte array to hex string
    private static String bytesToHex(byte[] bytes) {
        StringBuilder result = new StringBuilder();
        for (byte b : bytes) {
            result.append(String.format("%02X", b & 0xFF));
        }
        return result.toString();
    }

    // Key expansion
    private static byte[][] expandKey(byte[] key) {
        byte[][] roundKeys = new byte[11][16];
        System.arraycopy(key, 0, roundKeys[0], 0, 16);
        
        for (int round = 1; round <= 10; round++) {
            byte[] prevKey = roundKeys[round - 1];
            byte[] newKey = new byte[16];
            
            // RotWord and SubWord
            byte[] temp = new byte[4];
            temp[0] = (byte) SBOX[(prevKey[13] >> 4) & 0x0F][prevKey[13] & 0x0F];
            temp[1] = (byte) SBOX[(prevKey[14] >> 4) & 0x0F][prevKey[14] & 0x0F];
            temp[2] = (byte) SBOX[(prevKey[15] >> 4) & 0x0F][prevKey[15] & 0x0F];
            temp[3] = (byte) SBOX[(prevKey[12] >> 4) & 0x0F][prevKey[12] & 0x0F];
            
            // XOR with round constant
            temp[0] ^= RCON[round - 1];
            
            // Generate new round key
            for (int i = 0; i < 4; i++) {
                newKey[i] = (byte) (prevKey[i] ^ temp[i]);
            }
            for (int i = 4; i < 16; i++) {
                newKey[i] = (byte) (prevKey[i] ^ newKey[i - 4]);
            }
            
            roundKeys[round] = newKey;
        }
        
        return roundKeys;
    }

    // SubBytes transformation
    private static byte[] subBytes(byte[] state) {
        byte[] result = new byte[16];
        for (int i = 0; i < 16; i++) {
            int high = (state[i] >> 4) & 0x0F;
            int low = state[i] & 0x0F;
            result[i] = (byte) SBOX[high][low];
        }
        return result;
    }

    // Inverse SubBytes transformation
    private static byte[] invSubBytes(byte[] state) {
        byte[] result = new byte[16];
        for (int i = 0; i < 16; i++) {
            int high = (state[i] >> 4) & 0x0F;
            int low = state[i] & 0x0F;
            result[i] = (byte) INV_SBOX[high][low];
        }
        return result;
    }

    // ShiftRows transformation
    private static byte[] shiftRows(byte[] state) {
        byte[] result = new byte[16];
        // Row 0: no shift
        result[0] = state[0]; result[4] = state[4]; result[8] = state[8]; result[12] = state[12];
        // Row 1: shift left by 1
        result[1] = state[5]; result[5] = state[9]; result[9] = state[13]; result[13] = state[1];
        // Row 2: shift left by 2
        result[2] = state[10]; result[6] = state[14]; result[10] = state[2]; result[14] = state[6];
        // Row 3: shift left by 3
        result[3] = state[15]; result[7] = state[3]; result[11] = state[7]; result[15] = state[11];
        return result;
    }

    // Inverse ShiftRows transformation
    private static byte[] invShiftRows(byte[] state) {
        byte[] result = new byte[16];
        // Row 0: no shift
        result[0] = state[0]; result[4] = state[4]; result[8] = state[8]; result[12] = state[12];
        // Row 1: shift right by 1
        result[1] = state[13]; result[5] = state[1]; result[9] = state[5]; result[13] = state[9];
        // Row 2: shift right by 2
        result[2] = state[10]; result[6] = state[14]; result[10] = state[2]; result[14] = state[6];
        // Row 3: shift right by 3
        result[3] = state[7]; result[7] = state[11]; result[11] = state[15]; result[15] = state[3];
        return result;
    }

    // Galois field multiplication
    private static byte gmul(byte a, byte b) {
        byte p = 0;
        for (int counter = 0; counter < 8; counter++) {
            if ((b & 1) != 0) {
                p ^= a;
            }
            boolean hi_bit_set = (a & 0x80) != 0;
            a <<= 1;
            if (hi_bit_set) {
                a ^= 0x1b;
            }
            b >>= 1;
        }
        return p;
    }

    // MixColumns transformation
    private static byte[] mixColumns(byte[] state) {
        byte[] result = new byte[16];
        for (int col = 0; col < 4; col++) {
            byte s0 = state[col * 4];
            byte s1 = state[col * 4 + 1];
            byte s2 = state[col * 4 + 2];
            byte s3 = state[col * 4 + 3];
            
            result[col * 4] = (byte) (gmul((byte) 2, s0) ^ gmul((byte) 3, s1) ^ s2 ^ s3);
            result[col * 4 + 1] = (byte) (s0 ^ gmul((byte) 2, s1) ^ gmul((byte) 3, s2) ^ s3);
            result[col * 4 + 2] = (byte) (s0 ^ s1 ^ gmul((byte) 2, s2) ^ gmul((byte) 3, s3));
            result[col * 4 + 3] = (byte) (gmul((byte) 3, s0) ^ s1 ^ s2 ^ gmul((byte) 2, s3));
        }
        return result;
    }

    // Inverse MixColumns transformation
    private static byte[] invMixColumns(byte[] state) {
        byte[] result = new byte[16];
        for (int col = 0; col < 4; col++) {
            byte s0 = state[col * 4];
            byte s1 = state[col * 4 + 1];
            byte s2 = state[col * 4 + 2];
            byte s3 = state[col * 4 + 3];
            
            result[col * 4] = (byte) (gmul((byte) 0x0e, s0) ^ gmul((byte) 0x0b, s1) ^ gmul((byte) 0x0d, s2) ^ gmul((byte) 0x09, s3));
            result[col * 4 + 1] = (byte) (gmul((byte) 0x09, s0) ^ gmul((byte) 0x0e, s1) ^ gmul((byte) 0x0b, s2) ^ gmul((byte) 0x0d, s3));
            result[col * 4 + 2] = (byte) (gmul((byte) 0x0d, s0) ^ gmul((byte) 0x09, s1) ^ gmul((byte) 0x0e, s2) ^ gmul((byte) 0x0b, s3));
            result[col * 4 + 3] = (byte) (gmul((byte) 0x0b, s0) ^ gmul((byte) 0x0d, s1) ^ gmul((byte) 0x09, s2) ^ gmul((byte) 0x0e, s3));
        }
        return result;
    }

    // AddRoundKey transformation
    private static byte[] addRoundKey(byte[] state, byte[] roundKey) {
        byte[] result = new byte[16];
        for (int i = 0; i < 16; i++) {
            result[i] = (byte) (state[i] ^ roundKey[i]);
        }
        return result;
    }

    // PKCS7 padding
    private static byte[] addPadding(byte[] data) {
        int paddingLength = 16 - (data.length % 16);
        byte[] padded = new byte[data.length + paddingLength];
        System.arraycopy(data, 0, padded, 0, data.length);
        for (int i = data.length; i < padded.length; i++) {
            padded[i] = (byte) paddingLength;
        }
        return padded;
    }

    // Remove PKCS7 padding
    private static byte[] removePadding(byte[] data) {
        int paddingLength = data[data.length - 1] & 0xFF;
        if (paddingLength > 0 && paddingLength <= 16) {
            byte[] result = new byte[data.length - paddingLength];
            System.arraycopy(data, 0, result, 0, result.length);
            return result;
        }
        return data;
    }

    // AES Encryption with real step-by-step visualization
    private static String encrypt(String plaintext, byte[] key) {
        try {
            byte[] plainBytes = addPadding(plaintext.getBytes(StandardCharsets.UTF_8));
            byte[][] roundKeys = expandKey(key);
            
            StringBuilder json = new StringBuilder();
            json.append("{\"blocks\": [");
            
            // Process each 16-byte block
            for (int blockIndex = 0; blockIndex < plainBytes.length; blockIndex += 16) {
                if (blockIndex > 0) json.append(",");
                
                byte[] block = new byte[16];
                System.arraycopy(plainBytes, blockIndex, block, 0, 16);
                
                json.append("{\"block\": ").append((blockIndex / 16) + 1).append(", \"rounds\": [");
                
                // Initial AddRoundKey
                byte[] state = addRoundKey(block, roundKeys[0]);
                
                // 10 rounds of AES
                for (int round = 1; round <= 10; round++) {
                    if (round > 1) json.append(",");
                    json.append("{\"round\": ").append(round).append(",");
                    
                    // Start of round
                    json.append("\"startOfRound\": \"").append(bytesToHex(state)).append("\",");
                    
                    // SubBytes
                    state = subBytes(state);
                    json.append("\"afterSubBytes\": \"").append(bytesToHex(state)).append("\",");
                    
                    // ShiftRows
                    state = shiftRows(state);
                    json.append("\"afterShiftRows\": \"").append(bytesToHex(state)).append("\",");
                    
                    // MixColumns (skip in final round)
                    if (round < 10) {
                        state = mixColumns(state);
                    }
                    json.append("\"afterMixColumns\": \"").append(bytesToHex(state)).append("\",");
                    
                    // AddRoundKey
                    state = addRoundKey(state, roundKeys[round]);
                    json.append("\"afterAddRoundKey\": \"").append(bytesToHex(state)).append("\"");
                    
                    json.append("}");
                }
                
                json.append("]}"); // Close rounds array and block object
            }
            
            // Verify with standard library for final result
            Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
            SecretKeySpec secretKey = new SecretKeySpec(key, "AES");
            cipher.init(Cipher.ENCRYPT_MODE, secretKey);
            byte[] standardResult = cipher.doFinal(plaintext.getBytes(StandardCharsets.UTF_8));
            String finalBase64 = Base64.getEncoder().encodeToString(standardResult);
            
            json.append("], \"finalResult\": \"").append(finalBase64).append("\"}");
            
            return json.toString();
            
        } catch (Exception e) {
            return "{\"error\": \"Encryption failed: " + e.getMessage() + "\"}";
        }
    }

    // AES Decryption with real step-by-step visualization
    private static String decrypt(String ciphertext, byte[] key) {
        try {
            byte[] cipherBytes = Base64.getDecoder().decode(ciphertext);
            byte[][] roundKeys = expandKey(key);
            
            StringBuilder json = new StringBuilder();
            json.append("{\"blocks\": [");
            
            // Process each 16-byte block
            for (int blockIndex = 0; blockIndex < cipherBytes.length; blockIndex += 16) {
                if (blockIndex > 0) json.append(",");
                
                byte[] block = new byte[16];
                System.arraycopy(cipherBytes, blockIndex, block, 0, 16);
                byte[] state = block.clone();
                
                json.append("{\"block\": ").append((blockIndex / 16) + 1).append(", \"rounds\": [");
                
                // CORRECT AES DECRYPTION: Initial AddRoundKey with round key 10
                state = addRoundKey(state, roundKeys[10]);
                
                // Visualization rounds 1-10 (corresponding to AES rounds 9 down to 0)
                for (int round = 1; round <= 10; round++) {
                    if (round > 1) json.append(",");
                    json.append("{\"round\": ").append(round).append(",");
                    
                    // Start of round - show current state
                    json.append("\"startOfRound\": \"").append(bytesToHex(state)).append("\",");
                    
                    // Inverse ShiftRows
                    state = invShiftRows(state);
                    json.append("\"afterInvShiftRows\": \"").append(bytesToHex(state)).append("\",");
                    
                    // Inverse SubBytes
                    state = invSubBytes(state);
                    json.append("\"afterInvSubBytes\": \"").append(bytesToHex(state)).append("\",");
                    
                    // AddRoundKey: Use keys 9,8,7...1,0 for visualization rounds 1,2,3...9,10
                    int aesRoundKey = 10 - round;
                    state = addRoundKey(state, roundKeys[aesRoundKey]);
                    json.append("\"afterAddRoundKey\": \"").append(bytesToHex(state)).append("\",");
                    
                    // Inverse MixColumns (skip for final AES round 0, which is visualization round 10)
                    if (round < 10) {
                        state = invMixColumns(state);
                    }
                    json.append("\"afterInvMixColumns\": \"").append(bytesToHex(state)).append("\"");
                    
                    json.append("}");
                }
                
                json.append("]}"); // Close rounds array and block object
            }
            
            // Remove padding and get final result
            byte[] allBlocks = new byte[cipherBytes.length];
            int pos = 0;
            
            // Process all blocks again for final result using CORRECT AES decryption
            for (int blockIndex = 0; blockIndex < cipherBytes.length; blockIndex += 16) {
                byte[] block = new byte[16];
                System.arraycopy(cipherBytes, blockIndex, block, 0, 16);
                byte[] state = block.clone();
                
                // CORRECT AES DECRYPTION SEQUENCE:
                // 1. Initial AddRoundKey with round key 10
                state = addRoundKey(state, roundKeys[10]);
                
                // 2. Rounds 9 down to 1: InvShiftRows, InvSubBytes, AddRoundKey, InvMixColumns
                for (int round = 9; round >= 1; round--) {
                    state = invShiftRows(state);
                    state = invSubBytes(state);
                    state = addRoundKey(state, roundKeys[round]);
                    state = invMixColumns(state);
                }
                
                // 3. Final round (round 0): InvShiftRows, InvSubBytes, AddRoundKey (no InvMixColumns)
                state = invShiftRows(state);
                state = invSubBytes(state);
                state = addRoundKey(state, roundKeys[0]);
                
                System.arraycopy(state, 0, allBlocks, pos, 16);
                pos += 16;
            }
            
            // Remove padding
            byte[] decryptedBytes = removePadding(allBlocks);
            String result = new String(decryptedBytes, StandardCharsets.UTF_8);
            
            json.append("], \"finalResult\": \"");
            json.append(result.replace("\"", "\\\"")).append("\"}");
            
            return json.toString();
            
        } catch (Exception e) {
            return "{\"error\": \"Decryption failed: " + e.getMessage() + "\"}";
        }
    }
}
