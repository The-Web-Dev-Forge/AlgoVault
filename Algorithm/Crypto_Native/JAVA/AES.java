import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Base64;

public class AES{

    private static final int BLOCK_SIZE = 16;
    private static final int NUM_ROUNDS = 10;
    private static final int KEY_SCHEDULE_SIZE = BLOCK_SIZE * (NUM_ROUNDS + 1);

    private static final byte[][] S_BOX = {
        {(byte)0x63, (byte)0x7c, (byte)0x77, (byte)0x7b, (byte)0xf2, (byte)0x6b, (byte)0x6f, (byte)0xc5, (byte)0x30, (byte)0x01, (byte)0x67, (byte)0x2b, (byte)0xfe, (byte)0xd7, (byte)0xab, (byte)0x76},
        {(byte)0xca, (byte)0x82, (byte)0xc9, (byte)0x7d, (byte)0xfa, (byte)0x59, (byte)0x47, (byte)0xf0, (byte)0xad, (byte)0xd4, (byte)0xa2, (byte)0xaf, (byte)0x9c, (byte)0xa4, (byte)0x72, (byte)0xc0},
        {(byte)0xb7, (byte)0xfd, (byte)0x93, (byte)0x26, (byte)0x36, (byte)0x3f, (byte)0xf7, (byte)0xcc, (byte)0x34, (byte)0xa5, (byte)0xe5, (byte)0xf1, (byte)0x71, (byte)0xd8, (byte)0x31, (byte)0x15},
        {(byte)0x04, (byte)0xc7, (byte)0x23, (byte)0xc3, (byte)0x18, (byte)0x96, (byte)0x05, (byte)0x9a, (byte)0x07, (byte)0x12, (byte)0x80, (byte)0xe2, (byte)0xeb, (byte)0x27, (byte)0xb2, (byte)0x75},
        {(byte)0x09, (byte)0x83, (byte)0x2c, (byte)0x1a, (byte)0x1b, (byte)0x6e, (byte)0x5a, (byte)0xa0, (byte)0x52, (byte)0x3b, (byte)0xd6, (byte)0xb3, (byte)0x29, (byte)0xe3, (byte)0x2f, (byte)0x84},
        {(byte)0x53, (byte)0xd1, (byte)0x00, (byte)0xed, (byte)0x20, (byte)0xfc, (byte)0xb1, (byte)0x5b, (byte)0x6a, (byte)0xcb, (byte)0xbe, (byte)0x39, (byte)0x4a, (byte)0x4c, (byte)0x58, (byte)0xcf},
        {(byte)0xd0, (byte)0xef, (byte)0xaa, (byte)0xfb, (byte)0x43, (byte)0x4d, (byte)0x33, (byte)0x85, (byte)0x45, (byte)0xf9, (byte)0x02, (byte)0x7f, (byte)0x50, (byte)0x3c, (byte)0x9f, (byte)0xa8},
        {(byte)0x51, (byte)0xa3, (byte)0x40, (byte)0x8f, (byte)0x92, (byte)0x9d, (byte)0x38, (byte)0xf5, (byte)0xbc, (byte)0xb6, (byte)0xda, (byte)0x21, (byte)0x10, (byte)0xff, (byte)0xf3, (byte)0xd2},
        {(byte)0xcd, (byte)0x0c, (byte)0x13, (byte)0xec, (byte)0x5f, (byte)0x97, (byte)0x44, (byte)0x17, (byte)0xc4, (byte)0xa7, (byte)0x7e, (byte)0x3d, (byte)0x64, (byte)0x5d, (byte)0x19, (byte)0x73},
        {(byte)0x60, (byte)0x81, (byte)0x4f, (byte)0xdc, (byte)0x22, (byte)0x2a, (byte)0x90, (byte)0x88, (byte)0x46, (byte)0xee, (byte)0xb8, (byte)0x14, (byte)0xde, (byte)0x5e, (byte)0x0b, (byte)0xdb},
        {(byte)0xe0, (byte)0x32, (byte)0x3a, (byte)0x0a, (byte)0x49, (byte)0x06, (byte)0x24, (byte)0x5c, (byte)0xc2, (byte)0xd3, (byte)0xac, (byte)0x62, (byte)0x91, (byte)0x95, (byte)0xe4, (byte)0x79},
        {(byte)0xe7, (byte)0xc8, (byte)0x37, (byte)0x6d, (byte)0x8d, (byte)0xd5, (byte)0x4e, (byte)0xa9, (byte)0x6c, (byte)0x56, (byte)0xf4, (byte)0xea, (byte)0x65, (byte)0x7a, (byte)0xae, (byte)0x08},
        {(byte)0xba, (byte)0x78, (byte)0x25, (byte)0x2e, (byte)0x1c, (byte)0xa6, (byte)0xb4, (byte)0xc6, (byte)0xe8, (byte)0xdd, (byte)0x74, (byte)0x1f, (byte)0x4b, (byte)0xbd, (byte)0x8b, (byte)0x8a},
        {(byte)0x70, (byte)0x3e, (byte)0xb5, (byte)0x66, (byte)0x48, (byte)0x03, (byte)0xf6, (byte)0x0e, (byte)0x61, (byte)0x35, (byte)0x57, (byte)0xb9, (byte)0x86, (byte)0xc1, (byte)0x1d, (byte)0x9e},
        {(byte)0xe1, (byte)0xf8, (byte)0x98, (byte)0x11, (byte)0x69, (byte)0xd9, (byte)0x8e, (byte)0x94, (byte)0x9b, (byte)0x1e, (byte)0x87, (byte)0xe9, (byte)0xce, (byte)0x55, (byte)0x28, (byte)0xdf},
        {(byte)0x8c, (byte)0xa1, (byte)0x89, (byte)0x0d, (byte)0xbf, (byte)0xe6, (byte)0x42, (byte)0x68, (byte)0x41, (byte)0x99, (byte)0x2d, (byte)0x0f, (byte)0xb0, (byte)0x54, (byte)0xbb, (byte)0x16}
    };

    private static final byte[][] INV_S_BOX = {
        {(byte)0x52, (byte)0x09, (byte)0x6a, (byte)0xd5, (byte)0x30, (byte)0x36, (byte)0xa5, (byte)0x38, (byte)0xbf, (byte)0x40, (byte)0xa3, (byte)0x9e, (byte)0x81, (byte)0xf3, (byte)0xd7, (byte)0xfb},
        {(byte)0x7c, (byte)0xe3, (byte)0x39, (byte)0x82, (byte)0x9b, (byte)0x2f, (byte)0xff, (byte)0x87, (byte)0x34, (byte)0x8e, (byte)0x43, (byte)0x44, (byte)0xc4, (byte)0xde, (byte)0xe9, (byte)0xcb},
        {(byte)0x54, (byte)0x7b, (byte)0x94, (byte)0x32, (byte)0xa6, (byte)0xc2, (byte)0x23, (byte)0x3d, (byte)0xee, (byte)0x4c, (byte)0x95, (byte)0x0b, (byte)0x42, (byte)0xfa, (byte)0xc3, (byte)0x4e},
        {(byte)0x08, (byte)0x2e, (byte)0xa1, (byte)0x66, (byte)0x28, (byte)0xd9, (byte)0x24, (byte)0xb2, (byte)0x76, (byte)0x5b, (byte)0xa2, (byte)0x49, (byte)0x6d, (byte)0x8b, (byte)0xd1, (byte)0x25},
        {(byte)0x72, (byte)0xf8, (byte)0xf6, (byte)0x64, (byte)0x86, (byte)0x68, (byte)0x98, (byte)0x16, (byte)0xd4, (byte)0xa4, (byte)0x5c, (byte)0xcc, (byte)0x5d, (byte)0x65, (byte)0xb6, (byte)0x92},
        {(byte)0x6c, (byte)0x70, (byte)0x48, (byte)0x50, (byte)0xfd, (byte)0xed, (byte)0xb9, (byte)0xda, (byte)0x5e, (byte)0x15, (byte)0x46, (byte)0x57, (byte)0xa7, (byte)0x8d, (byte)0x9d, (byte)0x84},
        {(byte)0x90, (byte)0xd8, (byte)0xab, (byte)0x00, (byte)0x8c, (byte)0xbc, (byte)0xd3, (byte)0x0a, (byte)0xf7, (byte)0xe4, (byte)0x58, (byte)0x05, (byte)0xb8, (byte)0xb3, (byte)0x45, (byte)0x06},
        {(byte)0xd0, (byte)0x2c, (byte)0x1e, (byte)0x8f, (byte)0xca, (byte)0x3f, (byte)0x0f, (byte)0x02, (byte)0xc1, (byte)0xaf, (byte)0xbd, (byte)0x03, (byte)0x01, (byte)0x13, (byte)0x8a, (byte)0x6b},
        {(byte)0x3a, (byte)0x91, (byte)0x11, (byte)0x41, (byte)0x4f, (byte)0x67, (byte)0xdc, (byte)0xea, (byte)0x97, (byte)0xf2, (byte)0xcf, (byte)0xce, (byte)0xf0, (byte)0xb4, (byte)0xe6, (byte)0x73},
        {(byte)0x96, (byte)0xac, (byte)0x74, (byte)0x22, (byte)0xe7, (byte)0xad, (byte)0x35, (byte)0x85, (byte)0xe2, (byte)0xf9, (byte)0x37, (byte)0xe8, (byte)0x1c, (byte)0x75, (byte)0xdf, (byte)0x6e},
        {(byte)0x47, (byte)0xf1, (byte)0x1a, (byte)0x71, (byte)0x1d, (byte)0x29, (byte)0xc5, (byte)0x89, (byte)0x6f, (byte)0xb7, (byte)0x62, (byte)0x0e, (byte)0xaa, (byte)0x18, (byte)0xbe, (byte)0x1b},
        {(byte)0xfc, (byte)0x56, (byte)0x3e, (byte)0x4b, (byte)0xc6, (byte)0xd2, (byte)0x79, (byte)0x20, (byte)0x9a, (byte)0xdb, (byte)0xc0, (byte)0xfe, (byte)0x78, (byte)0xcd, (byte)0x5a, (byte)0xf4},
        {(byte)0x1f, (byte)0xdd, (byte)0xa8, (byte)0x33, (byte)0x88, (byte)0x07, (byte)0xc7, (byte)0x31, (byte)0xb1, (byte)0x12, (byte)0x10, (byte)0x59, (byte)0x27, (byte)0x80, (byte)0xec, (byte)0x5f},
        {(byte)0x60, (byte)0x51, (byte)0x7f, (byte)0xa9, (byte)0x19, (byte)0xb5, (byte)0x4a, (byte)0x0d, (byte)0x2d, (byte)0xe5, (byte)0x7a, (byte)0x9f, (byte)0x93, (byte)0xc9, (byte)0x9c, (byte)0xef},
        {(byte)0xa0, (byte)0xe0, (byte)0x3b, (byte)0x4d, (byte)0xae, (byte)0x2a, (byte)0xf5, (byte)0xb0, (byte)0xc8, (byte)0xeb, (byte)0xbb, (byte)0x3c, (byte)0x83, (byte)0x53, (byte)0x99, (byte)0x61},
        {(byte)0x17, (byte)0x2b, (byte)0x04, (byte)0x7e, (byte)0xba, (byte)0x77, (byte)0xd6, (byte)0x26, (byte)0xe1, (byte)0x69, (byte)0x14, (byte)0x63, (byte)0x55, (byte)0x21, (byte)0x0c, (byte)0x7d}
    };

    private static final byte[] RCON = {
        (byte)0x01, (byte)0x02, (byte)0x04, (byte)0x08, (byte)0x10, (byte)0x20, (byte)0x40, (byte)0x80, (byte)0x1b, (byte)0x36
    };

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

    private static String encrypt(String plaintext, byte[] key) {
        byte[] input = plaintext.getBytes(StandardCharsets.UTF_8);
        int paddingLength = BLOCK_SIZE - (input.length % BLOCK_SIZE);
        byte[] paddedInput = Arrays.copyOf(input, input.length + paddingLength);
        for (int i = input.length; i < paddedInput.length; i++) {
            paddedInput[i] = (byte) paddingLength;
        }

        byte[] expandedKey = new byte[KEY_SCHEDULE_SIZE];
        keyExpansion(key, expandedKey);

        byte[] ciphertext = new byte[paddedInput.length];
        StringBuilder json = new StringBuilder("{\"blocks\": [");

        for (int blockStart = 0; blockStart < paddedInput.length; blockStart += BLOCK_SIZE) {
            byte[] state = Arrays.copyOfRange(paddedInput, blockStart, blockStart + BLOCK_SIZE);
            if (blockStart > 0) json.append(",");
            json.append("{\"block\": ").append(blockStart / BLOCK_SIZE + 1).append(", \"rounds\": [");

            addRoundKey(state, expandedKey, 0);

            for (int round = 0; round < NUM_ROUNDS; round++) {
                json.append(round > 0 ? "," : "").append("{");
                json.append("\"round\": ").append(round + 1).append(",");
                json.append("\"startOfRound\": \"").append(bytesToHex(state)).append("\",");

                subBytes(state);
                json.append("\"afterSubBytes\": \"").append(bytesToHex(state)).append("\",");

                shiftRows(state);
                json.append("\"afterShiftRows\": \"").append(bytesToHex(state)).append("\",");

                if (round < NUM_ROUNDS - 1) {
                    mixColumns(state);
                    json.append("\"afterMixColumns\": \"").append(bytesToHex(state)).append("\",");
                } else {
                    json.append("\"afterMixColumns\": \"").append(bytesToHex(state)).append("\",");
                }

                addRoundKey(state, expandedKey, round + 1);
                json.append("\"afterAddRoundKey\": \"").append(bytesToHex(state)).append("\"}");
            }
            json.append("]}");
            System.arraycopy(state, 0, ciphertext, blockStart, BLOCK_SIZE);
        }

        json.append("], \"finalResult\": \"").append(Base64.getEncoder().encodeToString(ciphertext)).append("\"}");
        return json.toString();
    }

    private static String decrypt(String ciphertextBase64, byte[] key) {
        byte[] ciphertext = Base64.getDecoder().decode(ciphertextBase64);

        byte[] expandedKey = new byte[KEY_SCHEDULE_SIZE];
        keyExpansion(key, expandedKey);

        byte[] decrypted = new byte[ciphertext.length];
        StringBuilder json = new StringBuilder("{\"blocks\": [");

        for (int blockStart = 0; blockStart < ciphertext.length; blockStart += BLOCK_SIZE) {
            byte[] state = Arrays.copyOfRange(ciphertext, blockStart, blockStart + BLOCK_SIZE);
            if (blockStart > 0) json.append(",");
            json.append("{\"block\": ").append(blockStart / BLOCK_SIZE + 1).append(", \"rounds\": [");

            addRoundKey(state, expandedKey, NUM_ROUNDS);

            for (int round = NUM_ROUNDS - 1; round >= 0; round--) {
                json.append(round < NUM_ROUNDS - 1 ? "," : "").append("{");
                json.append("\"round\": ").append(NUM_ROUNDS - round).append(",");
                json.append("\"startOfRound\": \"").append(bytesToHex(state)).append("\",");

                invShiftRows(state);
                json.append("\"afterInvShiftRows\": \"").append(bytesToHex(state)).append("\",");

                invSubBytes(state);
                json.append("\"afterInvSubBytes\": \"").append(bytesToHex(state)).append("\",");

                addRoundKey(state, expandedKey, round);
                json.append("\"afterAddRoundKey\": \"").append(bytesToHex(state)).append("\",");

                if (round > 0) {
                    invMixColumns(state);
                    json.append("\"afterInvMixColumns\": \"").append(bytesToHex(state)).append("\"}");
                } else {
                    json.append("\"afterInvMixColumns\": \"").append(bytesToHex(state)).append("\"}");
                }
            }
            json.append("]}");
            System.arraycopy(state, 0, decrypted, blockStart, BLOCK_SIZE);
        }

        int paddingBytes = decrypted[decrypted.length - 1] & 0xFF;
        if (paddingBytes < 1 || paddingBytes > BLOCK_SIZE || decrypted.length < paddingBytes) {
            paddingBytes = 0;
        } else {
            boolean validPadding = true;
            for (int i = 0; i < paddingBytes; i++) {
                if ((decrypted[decrypted.length - 1 - i] & 0xFF) != paddingBytes) {
                    validPadding = false;
                    break;
                }
            }
            if (!validPadding) {
                paddingBytes = 0;
            }
        }

        byte[] finalDecrypted = Arrays.copyOf(decrypted, decrypted.length - paddingBytes);
        String finalDecryptedText = new String(finalDecrypted, StandardCharsets.UTF_8);
        finalDecryptedText = finalDecryptedText.replace("\"", "\\\"");

        json.append("], \"finalResult\": \"").append(finalDecryptedText).append("\"}");
        return json.toString();
    }

    private static void subBytes(byte[] state) {
        for (int i = 0; i < BLOCK_SIZE; i++) {
            state[i] = S_BOX[(state[i] >> 4) & 0x0F][state[i] & 0x0F];
        }
    }

    private static void invSubBytes(byte[] state) {
        for (int i = 0; i < BLOCK_SIZE; i++) {
            state[i] = INV_S_BOX[(state[i] >> 4) & 0x0F][state[i] & 0x0F];
        }
    }

    private static void shiftRows(byte[] state) {
        byte temp;
        // Row 1
        temp = state[1]; state[1] = state[5]; state[5] = state[9]; state[9] = state[13]; state[13] = temp;
        // Row 2
        temp = state[2]; state[2] = state[10]; state[10] = temp;
        temp = state[6]; state[6] = state[14]; state[14] = temp;
        // Row 3
        temp = state[3]; state[3] = state[15]; state[15] = state[11]; state[11] = state[7]; state[7] = temp;
    }

    private static void invShiftRows(byte[] state) {
        byte temp;
        // Row 1
        temp = state[13]; state[13] = state[9]; state[9] = state[5]; state[5] = state[1]; state[1] = temp;
        // Row 2
        temp = state[2]; state[2] = state[10]; state[10] = temp;
        temp = state[6]; state[6] = state[14]; state[14] = temp;
        // Row 3
        temp = state[3]; state[3] = state[7]; state[7] = state[11]; state[11] = state[15]; state[15] = temp;
    }

    private static void mixColumns(byte[] state) {
        for (int c = 0; c < 4; c++) {
            byte[] a = new byte[4];
            for (int i = 0; i < 4; i++) a[i] = state[i * 4 + c];
            state[0 * 4 + c] = (byte) (mul((byte)2, a[0]) ^ mul((byte)3, a[1]) ^ a[2] ^ a[3]);
            state[1 * 4 + c] = (byte) (a[0] ^ mul((byte)2, a[1]) ^ mul((byte)3, a[2]) ^ a[3]);
            state[2 * 4 + c] = (byte) (a[0] ^ a[1] ^ mul((byte)2, a[2]) ^ mul((byte)3, a[3]));
            state[3 * 4 + c] = (byte) (mul((byte)3, a[0]) ^ a[1] ^ a[2] ^ mul((byte)2, a[3]));
        }
    }

    private static void invMixColumns(byte[] state) {
        for (int c = 0; c < 4; c++) {
            byte[] a = new byte[4];
            for (int i = 0; i < 4; i++) a[i] = state[i * 4 + c];
            state[0 * 4 + c] = (byte) (mul((byte)0x0e, a[0]) ^ mul((byte)0x0b, a[1]) ^ mul((byte)0x0d, a[2]) ^ mul((byte)0x09, a[3]));
            state[1 * 4 + c] = (byte) (mul((byte)0x09, a[0]) ^ mul((byte)0x0e, a[1]) ^ mul((byte)0x0b, a[2]) ^ mul((byte)0x0d, a[3]));
            state[2 * 4 + c] = (byte) (mul((byte)0x0d, a[0]) ^ mul((byte)0x09, a[1]) ^ mul((byte)0x0e, a[2]) ^ mul((byte)0x0b, a[3]));
            state[3 * 4 + c] = (byte) (mul((byte)0x0b, a[0]) ^ mul((byte)0x0d, a[1]) ^ mul((byte)0x09, a[2]) ^ mul((byte)0x0e, a[3]));
        }
    }

    private static void addRoundKey(byte[] state, byte[] expandedKey, int round) {
        for (int i = 0; i < BLOCK_SIZE; i++) {
            state[i] ^= expandedKey[round * BLOCK_SIZE + i];
        }
    }

    private static void keyExpansion(byte[] key, byte[] expandedKey) {
        System.arraycopy(key, 0, expandedKey, 0, BLOCK_SIZE);
        for (int i = BLOCK_SIZE; i < KEY_SCHEDULE_SIZE; i += 4) {
            byte[] temp = Arrays.copyOfRange(expandedKey, i - 4, i);
            if (i % BLOCK_SIZE == 0) {
                // RotWord
                byte t = temp[0]; temp[0] = temp[1]; temp[1] = temp[2]; temp[2] = temp[3]; temp[3] = t;
                // SubWord
                for (int j = 0; j < 4; j++) temp[j] = S_BOX[(temp[j] >> 4) & 0x0F][temp[j] & 0x0F];
                // XOR with Rcon
                temp[0] ^= RCON[(i / BLOCK_SIZE) - 1];
            }
            for (int j = 0; j < 4; j++) {
                expandedKey[i + j] = (byte) (expandedKey[i - BLOCK_SIZE + j] ^ temp[j]);
            }
        }
    }

    private static byte mul(byte a, byte b) {
        byte p = 0;
        for (int i = 0; i < 8; i++) {
            if ((b & 1) != 0) p ^= a;
            boolean highBit = (a & 0x80) != 0;
            a <<= 1;
            if (highBit) a ^= 0x1B;
            b >>= 1;
        }
        return p;
    }

    private static String bytesToHex(byte[] bytes) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) sb.append(String.format("%02X", b));
        return sb.toString();
    }
}
