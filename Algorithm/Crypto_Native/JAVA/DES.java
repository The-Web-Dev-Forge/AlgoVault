import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.Scanner;
import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.DESKeySpec;

/**
 * @class DESProcessor
 * @brief Implements DES encryption and decryption with initial permutation and Feistel rounds.
 */
public class DESProcessor {
    private static final int[] IP = {
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    };
    private static String plainText;
    private static String key;
    private static String[] roundKeys = new String[16];

    /**
     * @brief Main function to execute encryption and decryption process.
     * This function reads command line arguments, and performs encryption and decryption.
     */
    public static void main(String[] args) {
        try {
            if (args.length < 2) {
                System.err.println("Usage: java DESProcessor <operation> <key> <text>");
                System.err.println("operation: encrypt or decrypt");
                System.exit(1);
            }

            String operation = args[0];
            key = args[1];
            plainText = args[2];
            
            if ("encrypt".equalsIgnoreCase(operation)) {
                // Encrypt using Java's DES implementation
                byte[] encryptedBytes = encrypt();
                String cipherText = Base64.getEncoder().encodeToString(encryptedBytes);
                System.out.println(cipherText);
            } else if ("decrypt".equalsIgnoreCase(operation)) {
                // Decrypt text
                byte[] encryptedBytes = Base64.getDecoder().decode(plainText);
                String decryptedText = decrypt(encryptedBytes);
                System.out.println(decryptedText);
            } else {
                System.err.println("Invalid operation. Use 'encrypt' or 'decrypt'");
                System.exit(1);
            }
            
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }

    /**
     * @brief Performs initial permutation on the input text.
     * This function applies an initial permutation to rearrange the bits according to a predefined table.
     */
    private static String performInitialPermutation(String input) {
        StringBuilder output = new StringBuilder();
        char[] inputChars = input.toCharArray();
        for (int i = 0; i < 16; i++) {
            if (i < inputChars.length) {
                output.append(inputChars[i]);
            }
        }
        return output.toString();
    }

    /**
     * @brief Generates 16 subkeys for Feistel rounds.
     * It repeatedly appends the given key to generate enough key material and extracts 16 round keys.
     */
    private static void generateSubKeys() {
        StringBuilder baseKey = new StringBuilder(key);
        while (baseKey.length() < 16 * 8) {
            baseKey.append(key);
        }
        for (int i = 0; i < 16; i++) {
            roundKeys[i] = baseKey.substring(i * 8, (i + 1) * 8);
        }
    }

    /**
     * @brief Splits the block into two halves.
     * This function divides the input string into two equal halves.
     */
    private static String[] splitBlock(String block) {
        int mid = block.length() / 2;
        return new String[]{block.substring(0, mid), block.substring(mid)};
    }

    /**
     * @brief Performs 16 rounds of Feistel function.
     * The function applies 16 rounds of a Feistel network transformation using generated round keys.
     */
    private static String[] performRounds(String input) {
        String[] roundOutputs = new String[16];
        String[] blocks = splitBlock(input);
        String left = blocks[0];
        String right = blocks[1];
        for (int i = 0; i < 16; i++) {
            String temp = right;
            right = xorStrings(left, feistelFunction(right, roundKeys[i]));
            left = temp;
            roundOutputs[i] = left + right;
        }
        return roundOutputs;
    }

    /**
     * @brief Feistel function for each round.
     * Applies a simple XOR operation between the right half and the round key.
     */
    private static String feistelFunction(String right, String roundKey) {
        int len = Math.min(right.length(), roundKey.length());
        return xorStrings(right.substring(0, len), roundKey.substring(0, len));
    }

    /**
     * @brief Performs XOR operation between two strings.
     * This function executes a character-wise XOR operation between two strings of equal length.
     */
    private static String xorStrings(String str1, String str2) {
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < str1.length(); i++) {
            result.append((char)(str1.charAt(i) ^ str2.charAt(i)));
        }
        return result.toString();
    }

    /**
     * @brief Encrypts the plaintext using DES encryption.
     *
     * This function initializes the DES cipher in encryption mode, sets up the secret key,
     * and performs encryption on the given plaintext.
     *
     * @return A byte array containing the encrypted text.
     * @throws Exception If an error occurs during encryption.
     */
    private static byte[] encrypt() throws Exception {
        DESKeySpec desKeySpec = new DESKeySpec(key.getBytes());
        SecretKeyFactory keyFactory = SecretKeyFactory.getInstance("DES");
        SecretKey secretKey = keyFactory.generateSecret(desKeySpec);
        Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        return cipher.doFinal(plainText.getBytes());
    }

    /**
     * @brief Decrypts the given encrypted text using DES decryption.
     *
     * This function initializes the DES cipher in decryption mode, sets up the secret key,
     * and performs decryption on the given encrypted byte array to retrieve the original plaintext.
     * 
     * @param encryptedText A byte array containing the encrypted text.
     * @return A string representing the decrypted plaintext.
     * @throws Exception If an error occurs during decryption.
     */
    private static String decrypt(byte[] encryptedText) throws Exception {
        DESKeySpec desKeySpec = new DESKeySpec(key.getBytes());
        SecretKeyFactory keyFactory = SecretKeyFactory.getInstance("DES");
        SecretKey secretKey = keyFactory.generateSecret(desKeySpec);
        Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, secretKey);
        byte[] decryptedBytes = cipher.doFinal(encryptedText);
        return new String(decryptedBytes, StandardCharsets.UTF_8);
    }
}
