import java.security.MessageDigest;
import java.util.Scanner;

public class MD5 {
    public static void main(String[] args) {
        if (args.length > 0) {
            // Check if this is a verification request (4 arguments: input, format, expected_hash, "verify")
            if (args.length >= 4 && "verify".equals(args[3])) {
                String input = args[0];
                String format = args[1];
                String expectedHash = args[2];
                
                String generatedHash = getMD5Hash(input, format);
                boolean matches = generatedHash.equalsIgnoreCase(expectedHash);
                
                // Output minimal verification result as JSON
                System.out.println("{");
                System.out.println("  \"generated_hash\": \"" + generatedHash + "\",");
                System.out.println("  \"expected_hash\": \"" + expectedHash + "\",");
                System.out.println("  \"matches\": " + matches);
                System.out.println("}");
                return;
            }
            
            // Regular hash generation mode
            String input = args[0];
            String format = args.length > 1 ? args[1] : "hex";
            String md5Hash = getMD5Hash(input, format);
            System.out.println(md5Hash);
        } else {
            // Create a Scanner object to read input from the user
            Scanner scanner = new Scanner(System.in);
            
            // Prompt the user to enter their name
            System.out.print("Enter your name: ");
            String name = scanner.nextLine();
            
            // Compute the MD5 hash of the name
            String md5Hash = getMD5Hash(name, "hex");
            
            // Display the MD5 hash
            System.out.println("MD5 Hash of \"" + name + "\": " + md5Hash);
            
            // Close the scanner
            scanner.close();
        }
    }

    /**
     * Computes the MD5 hash of a given input string.
     * @param input The input string to hash.
     * @param format The output format: "hex", "HEX", or "base64".
     * @return The MD5 hash in the specified format.
     */
    public static String getMD5Hash(String input, String format) {
        try {
            // Create a MessageDigest instance for MD5
            MessageDigest md = MessageDigest.getInstance("MD5");
            
            // Convert the input string to a byte array and compute the hash
            byte[] hashBytes = md.digest(input.getBytes("UTF-8"));
            
            // Format output based on requested format
            if ("base64".equalsIgnoreCase(format)) {
                // Convert to Base64
                return java.util.Base64.getEncoder().encodeToString(hashBytes);
            } else if ("HEX".equals(format) || "hex-upper".equalsIgnoreCase(format)) {
                // Convert to uppercase hexadecimal
                StringBuilder hexString = new StringBuilder();
                for (byte b : hashBytes) {
                    String hex = Integer.toHexString(0xff & b);
                    if (hex.length() == 1) {
                        hexString.append('0');
                    }
                    hexString.append(hex);
                }
                return hexString.toString().toUpperCase();
            } else {
                // Default: lowercase hexadecimal
                StringBuilder hexString = new StringBuilder();
                for (byte b : hashBytes) {
                    String hex = Integer.toHexString(0xff & b);
                    if (hex.length() == 1) {
                        hexString.append('0');
                    }
                    hexString.append(hex);
                }
                return hexString.toString();
            }
        } catch (Exception e) {
            // MD5 algorithm is not available or encoding failed
            throw new RuntimeException("Error generating MD5 hash.", e);
        }
    }
    
    /**
     * Computes the MD5 hash of a given input string (default hex format).
     * @param input The input string to hash.
     * @return The MD5 hash as a lowercase hexadecimal string.
     */
    public static String getMD5Hash(String input) {
        return getMD5Hash(input, "hex");
    }
}
