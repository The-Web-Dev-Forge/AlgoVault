import java.math.BigInteger;

/**
 * A command-line utility to perform Diffie-Hellman key exchange calculations.
 * This program is designed to be called from a script or another application (e.g., a Python/Django backend).
 *
 * It takes four command-line arguments:
 * 1. A prime number (p)
 * 2. A generator (g)
 * 3. Alice's private key (a)
 * 4. Bob's private key (b)
 *
 * The program calculates the public keys for Alice and Bob, computes the shared secret from both perspectives,
 * and prints the results as a single-line JSON object to standard output.
 *
 * How to Compile:
 * javac DiffieHellman.java
 *
 * How to Run:
 * java DiffieHellman <p> <g> <a> <b>
 * e.g., java DiffieHellman 23 5 6 15
 */
public class DiffieHellman {

    public static void main(String[] args) {
        // 1. Validate command-line arguments
        if (args.length != 4) {
            // Output an error as JSON and exit if arguments are incorrect
            System.out.println("{\"success\": false, \"error\": \"Invalid arguments. Usage: java DiffieHellman <prime p> <generator g> <private_a> <private_b>\"}");
            System.exit(1); // Exit with a non-zero status code to indicate an error
        }

        try {
            // 2. Parse arguments into BigInteger for safe handling of large numbers
            BigInteger p = new BigInteger(args[0]);         // Public prime
            BigInteger g = new BigInteger(args[1]);         // Public generator
            BigInteger privateA = new BigInteger(args[2]);  // Alice's private key
            BigInteger privateB = new BigInteger(args[3]);  // Bob's private key

            // 3. Calculate public keys
            // Alice's public key A = g^privateA mod p
            BigInteger publicA = g.modPow(privateA, p);

            // Bob's public key B = g^privateB mod p
            BigInteger publicB = g.modPow(privateB, p);

            // 4. Calculate the shared secret from both perspectives
            // Alice computes the secret: S = B^privateA mod p
            BigInteger secretA = publicB.modPow(privateA, p);

            // Bob computes the secret: S = A^privateB mod p
            BigInteger secretB = publicA.modPow(privateB, p);

            // 5. Verify that the secrets match
            boolean secretsMatch = secretA.equals(secretB);

            // 6. Format the results into a single-line JSON string
            // This is the ideal format for machine-to-machine communication
            String jsonOutput = String.format(
                "{" +
                    "\"success\": true, " +
                    "\"inputs\": {" +
                        "\"prime_p\": \"%s\", " +
                        "\"generator_g\": \"%s\", " +
                        "\"private_a\": \"%s\", " +
                        "\"private_b\": \"%s\"" +
                    "}, " +
                    "\"results\": {" +
                        "\"public_a\": \"%s\", " +
                        "\"public_b\": \"%s\", " +
                        "\"shared_secret_alice\": \"%s\", " +
                        "\"shared_secret_bob\": \"%s\", " +
                        "\"secrets_match\": %b" +
                    "}" +
                "}",
                p.toString(), g.toString(), privateA.toString(), privateB.toString(), // Inputs
                publicA.toString(), publicB.toString(), // Public Keys
                secretA.toString(), secretB.toString(), // Shared Secrets
                secretsMatch // Verification
            );

            // Print the final JSON string to standard output
            System.out.println(jsonOutput);

        } catch (NumberFormatException e) {
            // Handle cases where arguments are not valid integers
            System.out.println("{\"success\": false, \"error\": \"Invalid number format. All arguments must be valid integers.\"}");
            System.exit(1);
        } catch (Exception e) {
            // Catch any other potential errors during calculation
            System.out.println("{\"success\": false, \"error\": \"An unexpected error occurred: " + e.getMessage() + "\"}");
            System.exit(1);
        }
    }
}
