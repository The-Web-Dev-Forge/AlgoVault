import subprocess
import os
import json
import base64
import hashlib
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import sys

def error_page(request, exception=None, message=None):
    """Renders the generic error page for unsupported or missing algorithm pages."""
    # Use message from URL pattern first, then GET params, then default
    if not message:
        message = request.GET.get('message')
    if not message:
        message = 'Sorry, Page not found.....'
    context = {
        'error_message': message
    }
    return render(request, 'ErrorPage.html', context)


# Add the Algorithm/Crypto_Fallback/Python directory to sys.path
algorithm_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Algorithm', 'Crypto_Fallback', 'Python')
if algorithm_path not in sys.path:
    sys.path.append(algorithm_path)

# Now import the fallback functions
from CaesarCipher.CaesarCipher import caesar_cipher_fallback
from VigenereCipher.VigenereCipher import vigenere_cipher_fallback  
from HillCipher.HillCipher import hill_cipher_fallback
from DES.DES import des_fallback
from SHA512.SHA512 import sha512_hash
from AES.AES import aes_fallback
from DiffieHellman.DiffieHellman import diffie_hellman_fallback
from MD5.MD5 import MD5Hash
from HMAC.HMAC import HMACHash, hmac_fallback

def home(request):
    """Renders the home page."""
    return render(request, 'base.html', {'active_page': 'home'})

def tools(request):
    """Renders the tools page."""
    return render(request, 'tools.html', {'active_page': 'tools'})

def about(request):
    """Renders the about page."""
    return render(request, 'about.html', {'active_page': 'about'})

def help_page(request):
    """Renders the help page."""
    return render(request, 'help.html', {'active_page': 'help'})

def landing(request):
    """Renders the landing page."""
    return render(request, 'landing.html', {'active_page': 'landing'})

def caesar_cipher(request):
    """Renders the Caesar Cipher tool page and processes encryption/decryption."""
    if request.method == 'POST':
        operation = request.POST.get('operation', '')
        shift = int(request.POST.get('shift', 0))
        text = request.POST.get('message', '')  # Changed from 'text' to 'message' to match frontend
        
        result = ''
        # Try C++ executable first
        try:
            exe_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Algorithm', 'Crypto_Native', 'CPP', 'CaesarCipher.exe')
            if os.path.exists(exe_path):
                process = subprocess.run([exe_path, operation, str(shift), text], 
                                        capture_output=True, text=True, check=True)
                result = process.stdout.strip()
            else:
                # Use Python fallback
                result = caesar_cipher_fallback(text, shift, operation)
        except (subprocess.CalledProcessError, OSError, FileNotFoundError):
            # Use Python fallback if C++ fails (including compatibility issues)
            result = caesar_cipher_fallback(text, shift, operation)
        
        context = {
            'active_page': 'caesar',
            'result_text': result,  # Changed from 'result' to 'result_text' to match template
            'operation': operation,
            'shift_value': shift,   # Changed from 'shift' to 'shift_value' to match template
            'original_message': text  # Changed from 'text' to 'original_message' to match template
        }
    else:
        context = {'active_page': 'caesar'}
    
    return render(request, 'caesar.html', context)

def vigenere_view(request):
    """Renders the main Vigenere Cipher tool page."""
    context = {'active_page': 'vigenere'}
    return render(request, 'vigenere.html', context)

@csrf_exempt
def vigenere_process_api(request):
    """API endpoint for Vigenere Cipher processing with C++/Java primary and Python fallback."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

    try:
        data = json.loads(request.body)
        operation = data.get('operation', 'encrypt').lower()
        text = data.get('message')  # Changed from 'text' to 'message' to match frontend
        key = data.get('keyword')   # Changed from 'key' to 'keyword' to match frontend

        if not all([operation, text, key]):
            return JsonResponse({'error': 'Missing required fields.'}, status=400)

        result_text = None
        
        # Try C++ executable first
        cpp_executable_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Algorithm', 'Crypto_Native', 'CPP', 'VigenereCipher.exe')
        if os.path.exists(cpp_executable_path):
            try:
                command = [cpp_executable_path, operation, text, key]
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                result_text = result.stdout.strip()
            except (subprocess.CalledProcessError, OSError, FileNotFoundError):
                pass  # Will try Java or fallback

        # Try Java executable if C++ failed
        java_source_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Algorithm', 'Crypto_Native', 'JAVA')
        java_executable_path = os.path.join(java_source_dir, 'VigenereProcessor.class')
        if result_text is None and os.path.exists(java_executable_path):
            try:
                command = ['java', '-cp', java_source_dir, 'VigenereProcessor', operation, text, key]
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                result_text = result.stdout.strip()
            except subprocess.CalledProcessError:
                pass  # Will use Python fallback

        # Use Python fallback if both C++ and Java failed
        if result_text is None:
            result_text = vigenere_cipher_fallback(text, key, operation)

        return JsonResponse({'result': result_text})

    except Exception as e:
        # Final fallback to Python
        try:
            result_text = vigenere_cipher_fallback(text, key, operation)
            return JsonResponse({'result': result_text})
        except Exception as fallback_error:
            return JsonResponse({'error': f'All implementations failed. Error: {str(e)}. Fallback error: {str(fallback_error)}'}, status=500)

def des_view(request):
    """Renders the main DES tool page."""
    context = {'active_page': 'des'}
    return render(request, 'des.html', context)

@csrf_exempt
def des_process_api(request):
    """API endpoint for DES processing with Java as the primary and only implementation, with Python as fallback.
    
    Java is the preferred implementation for DES encryption/decryption, providing a complete
    implementation of the DES algorithm including the initial permutation, 16 rounds of
    Feistel function processing, final permutation, and proper key schedule generation.
    Python is used only as a fallback if Java execution fails.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

    try:
        data = json.loads(request.body)
        operation = data.get('operation', 'encrypt').lower()
        message_str = data.get('message')
        key_str = data.get('key')

        if not all([operation, message_str, key_str]):
            return JsonResponse({'error': 'Missing required fields.'}, status=400)

        result_text = None
        
        # Java is the primary and preferred implementation for DES
        java_source_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Algorithm', 'Crypto_Native', 'JAVA')
        java_class_file = os.path.join(java_source_dir, 'DES.class')
        
        # Compile Java if class file doesn't exist
        if not os.path.exists(java_class_file):
            try:
                java_source_file = os.path.join(java_source_dir, 'DES.java')
                if os.path.exists(java_source_file):
                    compile_cmd = ['javac', java_source_file]
                    subprocess.run(compile_cmd, check=True, capture_output=True)
            except Exception as e:
                print(f"Failed to compile Java: {str(e)}")
        
        # Try to use Java implementation
        if os.path.exists(java_class_file) or os.path.exists(os.path.join(java_source_dir, 'DES.java')):
            try:
                # Prepare key (must be 8 bytes for DES)
                if len(key_str) < 8:
                    key_str = key_str + '\0' * (8 - len(key_str))  # Pad with nulls
                elif len(key_str) > 8:
                    key_str = key_str[:8]  # Truncate
                
                # Run Java with appropriate parameters - Java is the only proper implementation for DES
                command = ['java', '-cp', java_source_dir, 'DES', operation, key_str, message_str]
                result = subprocess.run(command, capture_output=True, text=True, check=False)
                
                if result.returncode == 0:
                    result_text = result.stdout.strip()
                else:
                    print(f"Java error: {result.stderr}")
            except Exception as e:
                print(f"Java execution error: {str(e)}")
                # Will use Python fallback only if Java fails

        # Use Python fallback only if Java failed - Python implementation is not as robust as Java
        if result_text is None:
            result_text = des_fallback(operation, key_str, message_str)

        return JsonResponse({'result': result_text})

    except Exception as e:
        # Final fallback to Python if Java completely fails
        try:
            if not all([operation, message_str, key_str]):
                return JsonResponse({'error': 'Missing required fields in fallback.'}, status=400)
                
            # Python fallback is a last resort when Java is unavailable
            result_text = des_fallback(operation, key_str, message_str)
            return JsonResponse({'result': result_text})
        except Exception as fallback_error:
            return JsonResponse({'error': f'All implementations failed. Error: {str(e)}. Fallback error: {str(fallback_error)}'}, status=500)

def sha512_view(request):
    """Renders the main SHA-512 tool page."""
    context = {'active_page': 'sha512'}
    return render(request, 'sha512.html', context)

@csrf_exempt
def sha512_process_api(request):
    """API endpoint for SHA-512 hashing with C++ as primary implementation and Python as fallback.
    
    C++ is the preferred implementation for SHA-512 hashing, providing a complete
    implementation of the SHA-512 algorithm based on NIST FIPS 180-4 specification.
    Python's hashlib is used only as a fallback if C++ execution fails.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

    try:
        data = json.loads(request.body)
        message = data.get('message')

        if message is None:
            return JsonResponse({'error': 'Missing required message field.'}, status=400)

        hash_result = None
        
        # C++ is the primary and preferred implementation for SHA-512
        cpp_executable_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Algorithm', 'Crypto_Native', 'CPP', 'SHA-512.exe')
        if os.path.exists(cpp_executable_path):
            try:
                # Run C++ with appropriate parameters
                command = [cpp_executable_path, message]
                result = subprocess.run(command, capture_output=True, text=True, check=False)
                
                if result.returncode == 0:
                    hash_result = result.stdout.strip()
                else:
                    print(f"C++ SHA-512 error: {result.stderr}")
            except (Exception, OSError, FileNotFoundError) as e:
                print(f"C++ SHA-512 execution error: {str(e)}")
                # Will use Python fallback only if C++ fails

        # Use Python fallback only if C++ failed - Python implementation is not preferred
        if hash_result is None:
            hash_result = sha512_hash(message)
        
        return JsonResponse({'result': hash_result})
    except Exception as e:
        # Final fallback to Python if C++ completely fails
        try:
            if message is None:
                return JsonResponse({'error': 'Missing required message field in fallback.'}, status=400)
                
            # Python fallback is a last resort when C++ is unavailable
            hash_result = sha512_hash(message)
            return JsonResponse({'result': hash_result})
        except Exception as fallback_error:
            return JsonResponse({'error': f'All implementations failed. Error: {str(e)}. Fallback error: {str(fallback_error)}'}, status=500)

def hill_view(request):
    """Renders the main Hill Cipher tool page."""
    context = {'active_page': 'hill'}
    return render(request, 'hill.html', context)

@csrf_exempt
def hill_process_api(request):
    """API endpoint for Hill Cipher processing with C++/Java primary and Python fallback."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

    try:
        data = json.loads(request.body)
        operation = data.get('operation')
        dimension = data.get('dimension')
        key_matrix_flat = data.get('key_matrix_flat')  # List of integers
        input_vector_flat = data.get('input_vector_flat')  # List of integers
        key_word = data.get('key_word')  # Optional key word
        input_text = data.get('input_text')  # Optional text input

        # Validate required fields
        if not operation:
            return JsonResponse({'error': 'Operation is required.'}, status=400)
        if not dimension:
            return JsonResponse({'error': 'Dimension is required.'}, status=400)
        
        # Validate that we have either key_matrix_flat or key_word
        if not key_matrix_flat and not key_word:
            return JsonResponse({'error': 'Either key_matrix_flat or key_word is required.'}, status=400)
        
        # Validate that we have either input_vector_flat or input_text
        if not input_vector_flat and not input_text:
            return JsonResponse({'error': 'Either input_vector_flat or input_text is required.'}, status=400)

        result_vector = None
        result_text = None

        # Try C++ executable first
        cpp_executable_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Algorithm', 'Crypto_Native', 'CPP', 'HillCipher.exe')
        if os.path.exists(cpp_executable_path):
            try:
                # Base command
                command = [cpp_executable_path, operation, str(dimension)]
                
                # Add key (either matrix or word)
                if key_word:
                    command.extend(["--key-word", key_word])
                else:
                    # Add key matrix elements
                    command.extend(map(str, key_matrix_flat))
                
                # Add input (either vector or text)
                if input_text:
                    command.extend(["--text", input_text])
                    result_type = "text"
                else:
                    # Add input vector elements
                    command.extend(map(str, input_vector_flat))
                    result_type = "vector"
                
                # Run the command
                result = subprocess.run(command, capture_output=True, text=True, check=False)
                
                # Check result based on expected type
                if result.returncode == 0:
                    if result_type == "vector":
                        result_vector = list(map(int, result.stdout.strip().split()))
                    else:
                        result_text = result.stdout.strip()
            except (Exception, OSError, FileNotFoundError) as e:
                print(f"C++ execution error: {str(e)}")
                pass  # Will try Java or fallback

        # Try Java executable if C++ failed
        java_source_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Algorithm', 'Crypto_Native', 'JAVA')
        java_executable_path = os.path.join(java_source_dir, 'HillProcessor.class')
        if (result_vector is None and result_text is None) and os.path.exists(java_executable_path):
            try:
                # Note: This would need to be updated if Java implementation supports word keys and text input
                args = [operation, str(dimension)]
                args.extend(map(str, key_matrix_flat or []))
                args.extend(map(str, input_vector_flat or []))
                command = ['java', '-cp', java_source_dir, 'HillProcessor'] + args
                
                result = subprocess.run(command, capture_output=True, text=True, check=False)
                
                if result.returncode == 0:
                    result_vector = list(map(int, result.stdout.strip().split()))
            except Exception:
                pass  # Will use Python fallback

        # Use Python fallback if both C++ and Java failed
        if result_vector is None and result_text is None:
            # Prepare inputs for Python fallback
            if key_word and not key_matrix_flat:
                # Convert key word to matrix for Python fallback
                key_matrix_flat = []
                for c in key_word.upper():
                    if c.isalpha():
                        key_matrix_flat.append(ord(c) - ord('A'))
                # Pad if needed
                needed = dimension * dimension
                while len(key_matrix_flat) < needed:
                    key_matrix_flat.append(ord('X') - ord('A'))
                # Truncate if too long
                key_matrix_flat = key_matrix_flat[:needed]
            
            if input_text and not input_vector_flat:
                # Convert input text to vector for Python fallback
                input_vector_flat = []
                for c in input_text.upper():
                    if c.isalpha():
                        input_vector_flat.append(ord(c) - ord('A'))
            
            # Now we have key_matrix_flat and input_vector_flat, use Python fallback
            result_vector = hill_cipher_fallback(operation, dimension, key_matrix_flat, input_vector_flat)
            
            # If original input was text, convert result back to text
            if input_text:
                result_text = ''.join([chr(n + ord('A')) for n in result_vector])

        # Return the appropriate result
        if result_text is not None:
            return JsonResponse({'result_text': result_text})
        elif result_vector is not None:
            return JsonResponse({'result_vector': result_vector})
        else:
            return JsonResponse({'error': 'Processing failed with all implementations.'}, status=500)

    except Exception as e:
        # Final fallback to Python
        try:
            if not key_matrix_flat and key_word:
                # Convert key word to matrix for fallback
                key_matrix_flat = []
                for c in key_word.upper():
                    if c.isalpha():
                        key_matrix_flat.append(ord(c) - ord('A'))
                # Pad if needed
                needed = dimension * dimension
                while len(key_matrix_flat) < needed:
                    key_matrix_flat.append(ord('X') - ord('A'))
                # Truncate if too long
                key_matrix_flat = key_matrix_flat[:needed]
            
            if not input_vector_flat and input_text:
                # Convert input text to vector for fallback
                input_vector_flat = []
                for c in input_text.upper():
                    if c.isalpha():
                        input_vector_flat.append(ord(c) - ord('A'))
            
            # Process with Python fallback
            result_vector = hill_cipher_fallback(operation, dimension, key_matrix_flat, input_vector_flat)
            
            # If original input was text, convert result back to text
            if input_text:
                # Store original length for padding removal in decryption
                original_length = len(''.join(c for c in input_text.upper() if c.isalpha()))
                
                # Convert result to text
                result_text = ''.join([chr(n + ord('A')) for n in result_vector])
                
                # Remove padding for decryption
                if operation == 'decrypt' and len(result_text) > original_length:
                    # Remove trailing X padding
                    while result_text and result_text[-1] == 'X' and len(result_text) > original_length:
                        result_text = result_text[:-1]
                
                return JsonResponse({'result_text': result_text})
            else:
                return JsonResponse({'result_vector': result_vector})
                
        except Exception as fallback_error:
            return JsonResponse({'error': f'All implementations failed. Error: {str(e)}. Fallback error: {str(fallback_error)}'}, status=500)

def format_state_to_grid(hex_string):
    """Converts a 32-char hex string into a 4x4 grid of 2-char hex bytes for column-major state."""
    grid = []
    for i in range(4): # Rows
        row = []
        for j in range(4): # Columns
            index = (j * 4 + i) * 2
            row.append(hex_string[index:index+2])
        grid.append(row)
    return grid

def aes_view(request):
    context = {}
    if request.method == 'POST':
        message = request.POST.get('message', '')
        key = request.POST.get('key', '')
        operation = request.POST.get('operation', 'encrypt')

        if not message or not key:
            context['error'] = 'Message and Key are required.'
        elif len(key) != 16:
            context['error'] = 'AES key must be exactly 16 characters long.'
        else:
            output_data = None
            try:
                # Use Java implementation as primary
                java_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Algorithm', 'Crypto_Native', 'JAVA')
                java_file = os.path.join(java_dir, 'AES.java')
                class_file = os.path.join(java_dir, 'AES.class')
                
                # Compile Java file if class doesn't exist or is older than source
                if not os.path.exists(class_file) or os.path.getmtime(java_file) > os.path.getmtime(class_file):
                    compile_result = subprocess.run(['javac', java_file], capture_output=True, text=True)
                    if compile_result.returncode != 0:
                        raise Exception(f"Java compilation failed: {compile_result.stderr}")
                
                # Run the Java program
                command = ['java', '-cp', java_dir, 'AES', message, key, operation]
                result = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
                
                if result.stdout.strip():
                    output_data = json.loads(result.stdout.strip())
                else:
                    raise Exception("Java AES returned no output")
                    
            except:
                # Python fallback if Java fails
                try:
                    output_data = aes_fallback(operation, message, key)
                    
                    # Check if Python fallback succeeded
                    if not output_data or output_data.get('finalResult', '').startswith('Error'):
                        raise Exception("Python fallback also failed")
                        
                except:
                    # Both failed
                    pass
            
            # Process the output_data (whether from Java or Python fallback)
            if output_data:
                # Process each block in the JSON output
                blocks_data = output_data.get('blocks', [])
                for block in blocks_data:
                    rounds_data = block.get('rounds', [])
                    for round_info in rounds_data:
                        # Create a list of items to avoid modifying dict during iteration
                        items_to_process = list(round_info.items())
                        for step, hex_val in items_to_process:
                            if step != 'round' and isinstance(hex_val, str) and len(hex_val) == 32:
                                round_info[f'{step}_grid'] = format_state_to_grid(hex_val)

                context = {
                    'message': message,
                    'key': key,
                    'operation': operation,
                    'result': output_data.get('finalResult'),
                    'blocks_data': blocks_data, # Pass all block data to the template
                    'is_post': True
                }
            else:
                context['error'] = "Failed to process AES operation."

    return render(request, 'aes.html', context)

@csrf_exempt
def aes_process_api(request):
    """API endpoint for AES processing with Java primary and Python fallback."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        key = data.get('key', '')
        operation = data.get('operation', 'encrypt')

        if not message or not key:
            return JsonResponse({'error': 'Message and Key are required.'}, status=400)
        elif len(key) != 16:
            return JsonResponse({'error': 'AES key must be exactly 16 characters long.'}, status=400)

        output_data = None
        try:
            # Use Java implementation as primary
            java_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Algorithm', 'Crypto_Native', 'JAVA')
            java_file = os.path.join(java_dir, 'AES.java')
            class_file = os.path.join(java_dir, 'AES.class')
            
            # Compile Java file if class doesn't exist or is older than source
            if not os.path.exists(class_file) or os.path.getmtime(java_file) > os.path.getmtime(class_file):
                compile_result = subprocess.run(['javac', java_file], capture_output=True, text=True)
                if compile_result.returncode != 0:
                    raise Exception(f"Java compilation failed: {compile_result.stderr}")
            
            # Run the Java program
            command = ['java', '-cp', java_dir, 'AES', message, key, operation]
            result = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
            
            if result.stdout.strip():
                output_data = json.loads(result.stdout.strip())
            else:
                raise Exception("Java AES returned no output")
                
        except Exception as e:
            # Python fallback if Java fails
            try:
                output_data = aes_fallback(operation, message, key)
                
                # Check if Python fallback succeeded
                if not output_data or output_data.get('finalResult', '').startswith('Error'):
                    raise Exception("Python fallback also failed")
                    
            except Exception as python_e:
                # Both failed
                pass
        
        # Process the output_data for visualization
        if output_data:
            blocks_data = output_data.get('blocks', [])
            for block in blocks_data:
                rounds_data = block.get('rounds', [])
                for round_info in rounds_data:
                    # Create a list of items to avoid modifying dict during iteration
                    items_to_process = list(round_info.items())
                    for step, hex_val in items_to_process:
                        if step != 'round' and isinstance(hex_val, str) and len(hex_val) == 32:
                            round_info[f'{step}_grid'] = format_state_to_grid(hex_val)

            return JsonResponse({
                'result': output_data.get('finalResult', 'Processing completed'),
                'blocks_data': blocks_data,
                'operation': operation
            })
        else:
            return JsonResponse({'error': 'Failed to process AES operation.'}, status=500)

    except Exception as e:
        # Final fallback to Python
        try:
            result_text = aes_fallback(operation, message, key)
            return JsonResponse({'result': result_text.get('finalResult', 'Processing completed')})
        except Exception as fallback_error:
            return JsonResponse({'error': f'All implementations failed. Error: {str(e)}. Fallback error: {str(fallback_error)}'}, status=500)


def md5_view(request):
    # Render the form page initially or with previous inputs/results
    context = {
        'input_text': '',
        'output_format': 'hex',
        'operation': 'hash',
        'expected_hash': '',
        'result': None,
    }
    return render(request, 'md5.html', context)

def md5_process(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '').strip()
        output_format = request.POST.get('output_format', 'hex').strip()
        operation = request.POST.get('operation', 'hash').strip()
        expected_hash = request.POST.get('expected_hash', '').strip()

        context = {
            'input_text': input_text,
            'output_format': output_format,
            'operation': operation,
            'expected_hash': expected_hash,
            'result': None,
            'implementation_used': None,
        }

        if not input_text:
            context['result'] = "Error: Input text is required."
            return render(request, 'md5.html', context)

        try:
            # Try Java implementation first
            java_success = False
            java_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Algorithm', 'Crypto_Native', 'JAVA')
            java_class_path = os.path.join(java_dir, 'MD5.class')
            
            if os.path.exists(java_class_path):
                try:
                    if operation == 'verify':
                        if not expected_hash:
                            context['result'] = "Error: Expected hash is required for verification."
                            return render(request, 'md5.html', context)
                        
                        # Use Java for verification
                        command = ['java', '-cp', java_dir, 'MD5', input_text, output_format, expected_hash, 'verify']
                        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=10)
                        
                        # Parse JSON output from Java
                        import json
                        java_result = json.loads(result.stdout.strip())
                        
                        generated_hash = java_result.get('generated_hash', '')
                        matches = java_result.get('matches', False)
                        
                        if matches:
                            context['result'] = f"✅ Hash verification successful! The input matches the expected hash.\nGenerated: {generated_hash}"
                        else:
                            context['result'] = f"❌ Hash verification failed!\nGenerated: {generated_hash}\nExpected: {expected_hash}"
                        
                        context['implementation_used'] = 'Java'
                        java_success = True
                        
                    else:
                        # Use Java for hash generation
                        command = ['java', '-cp', java_dir, 'MD5', input_text, output_format]
                        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=10)
                        
                        context['result'] = result.stdout.strip()
                        context['implementation_used'] = 'Java'
                        java_success = True
                        
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
                    # Java failed, will use Python fallback
                    java_success = False
            
            # Use Python fallback if Java failed or is not available
            if not java_success:
                try:
                    # Import Python fallback
                    from Algorithm.Crypto_Fallback.Python.MD5.MD5 import MD5Hash
                    
                    if operation == 'verify':
                        if not expected_hash:
                            context['result'] = "Error: Expected hash is required for verification."
                            return render(request, 'md5.html', context)
                        
                        generated_hash, matches = MD5Hash.verify_hash(input_text, expected_hash, output_format)
                        
                        if matches:
                            context['result'] = f"✅ Hash verification successful! The input matches the expected hash.\nGenerated: {generated_hash}"
                        else:
                            context['result'] = f"❌ Hash verification failed!\nGenerated: {generated_hash}\nExpected: {expected_hash}"
                        
                        context['implementation_used'] = 'Python (Fallback)'
                        
                    else:
                        # Use Python for hash generation
                        md5_hash = MD5Hash.generate_hash(input_text, output_format)
                        context['result'] = md5_hash
                        context['implementation_used'] = 'Python (Fallback)'
                        
                except ImportError:
                    # Final fallback to basic hashlib if Python implementation fails
                    md5_hash = hashlib.md5(input_text.encode('utf-8')).hexdigest()
                    
                    if operation == 'verify':
                        if not expected_hash:
                            context['result'] = "Error: Expected hash is required for verification."
                            return render(request, 'md5.html', context)
                        
                        if md5_hash.lower() == expected_hash.lower():
                            context['result'] = f"✅ Hash verification successful! The input matches the expected hash.\nGenerated: {md5_hash}"
                        else:
                            context['result'] = f"❌ Hash verification failed!\nGenerated: {md5_hash}\nExpected: {expected_hash}"
                    else:
                        # Format the output based on user preference
                        if output_format == 'HEX':
                            context['result'] = md5_hash.upper()
                        elif output_format == 'base64':
                            # Convert hex to bytes then to base64
                            hash_bytes = bytes.fromhex(md5_hash)
                            context['result'] = base64.b64encode(hash_bytes).decode('ascii')
                        else:  # hex (lowercase)
                            context['result'] = md5_hash.lower()
                    
                    context['implementation_used'] = 'Python (Basic Hashlib)'

        except Exception as e:
            context['result'] = f"Error generating MD5 hash: {str(e)}"
            context['implementation_used'] = 'Error'

        return render(request, 'md5.html', context)

    else:
        # If GET request, redirect to md5_view
        return md5_view(request)

def diffie_hellman_view(request):
    """Renders the main Diffie-Hellman key exchange tool page."""
    context = {
        'active_page': 'diffie',
        'p': '23',
        'g': '5',
        'alice_private': '6',
        'bob_private': '15',
        'result': None,
    }
    
    if request.method == 'POST':
        # Handle form submission for server-side processing
        p = request.POST.get('prime', '23')
        g = request.POST.get('generator', '5')
        alice_private = request.POST.get('alice_private', '6')
        bob_private = request.POST.get('bob_private', '15')
        
        # Update context with submitted values
        context.update({
            'p': p,
            'g': g,
            'alice_private': alice_private,
            'bob_private': bob_private,
        })
        
        try:
            # Try to use Python fallback directly
            from Algorithm.Crypto_Fallback.Python.DiffieHellman.DiffieHellman import diffie_hellman_fallback
            
            # Perform Diffie-Hellman key exchange
            result = diffie_hellman_fallback(p, g, alice_private, bob_private)
            
            if result['success']:
                context['result'] = result['result']
                context['success'] = True
            else:
                context['error'] = result['error']
                context['success'] = False
                
        except ImportError:
            context['error'] = "Python fallback implementation not available."
            context['success'] = False
        except Exception as e:
            context['error'] = f"Calculation error: {str(e)}"
            context['success'] = False
    
    return render(request, 'diffie_hellman.html', context)

@csrf_exempt
def diffie_hellman_process_api(request):
    """API endpoint for Diffie-Hellman key exchange calculation with Java and Python fallback."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

    try:
        data = json.loads(request.body)
        p = data.get('p', '23')
        g = data.get('g', '5')
        alice_private = data.get('alice_private', '6')
        bob_private = data.get('bob_private', '15')
        
        result_data = None
        java_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Algorithm', 'Crypto_Native', 'JAVA')
        java_class_path = os.path.join(java_dir, 'DiffieHellman.class')
        
        # Try Java implementation first
        try:
            if os.path.exists(java_class_path):
                command = ['java', '-cp', java_dir, 'DiffieHellman', str(p), str(g), str(alice_private), str(bob_private)]
                result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=10)
                output = result.stdout.strip()
                
                # Parse JSON output from Java
                import json
                java_result = json.loads(output)
                
                if java_result.get('success'):
                    result_data = {
                        'success': True,
                        'inputs': java_result['inputs'],
                        'results': java_result['results'],
                        'implementation': 'java'
                    }
                else:
                    raise Exception(java_result.get('error', 'Java execution failed'))
                    
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
            # Fall back to Python implementation
            try:
                from Algorithm.Crypto_Fallback.Python.DiffieHellman.DiffieHellman import diffie_hellman_fallback
                result = diffie_hellman_fallback(int(p), int(g), int(alice_private), int(bob_private))
                result_data = {
                    'success': result['success'],
                    'inputs': {
                        'prime_p': str(p),
                        'generator_g': str(g),
                        'private_a': str(alice_private),
                        'private_b': str(bob_private)
                    },
                    'results': result['result'] if result['success'] else {},
                    'implementation': 'python',
                    'fallback_reason': str(e)
                }
            except ImportError:
                return JsonResponse({'error': 'Neither Java nor Python implementation available.'}, status=500)
            except Exception as fallback_error:
                return JsonResponse({'error': f'Both Java and Python implementations failed: {str(fallback_error)}'}, status=500)
        
        return JsonResponse(result_data)

    except Exception as e:
        return JsonResponse({'error': f'Processing failed: {str(e)}'}, status=500)


def hmac_view(request):
    """Render the form page initially or with previous inputs/results"""
    context = {
        'input_text': '',
        'secret_key': '',
        'algorithm': 'sha256',
        'output_format': 'hex',
        'operation': 'generate',
        'expected_hmac': '',
        'result': None,
    }
    return render(request, 'hmac.html', context)


def hmac_process(request):
    """Process HMAC generation or verification with C++ primary implementation and detailed step visualization"""
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '').strip()
        secret_key = request.POST.get('secret_key', '').strip()
        algorithm = request.POST.get('algorithm', 'sha256').strip()
        output_format = request.POST.get('output_format', 'hex').strip()
        operation = request.POST.get('operation', 'generate').strip()
        expected_hmac = request.POST.get('expected_hmac', '').strip()

        context = {
            'input_text': input_text,
            'secret_key': secret_key,
            'algorithm': algorithm,
            'output_format': output_format,
            'operation': operation,
            'expected_hmac': expected_hmac,
            'result': None,
            'implementation_used': None,
            'steps': None,
        }

        if not input_text:
            context['result'] = "Error: Message is required."
            return render(request, 'hmac.html', context)

        if not secret_key:
            context['result'] = "Error: Secret key is required."
            return render(request, 'hmac.html', context)

        try:
            # Try C++ implementation first (supports all algorithms: MD5, SHA1, SHA224, SHA256, SHA384, SHA512)
            try:
                exe_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                      'Algorithm', 'Crypto_Native', 'CPP', 'HMAC')
                
                if os.path.exists(exe_path):
                    # Convert algorithm name to uppercase for C++ compatibility
                    cpp_algorithm = algorithm.upper()
                    
                    if operation == 'verify':
                        if not expected_hmac:
                            context['result'] = "Error: Expected HMAC is required for verification."
                            return render(request, 'hmac.html', context)
                        
                        # Run verification with algorithm parameter
                        process = subprocess.run([exe_path, input_text, secret_key, expected_hmac, cpp_algorithm], 
                                               capture_output=True, text=True, check=True)
                        result_json = json.loads(process.stdout.strip())
                        
                        if result_json.get('valid', False):
                            context['result'] = "✅ HMAC verification successful! The message is authentic."
                        else:
                            context['result'] = "❌ HMAC verification failed! The message may have been tampered with."
                        
                        context['implementation_used'] = 'C++ Native Implementation'
                        
                    else:
                        # Generate HMAC with detailed steps and algorithm parameter
                        process = subprocess.run([exe_path, input_text, secret_key, cpp_algorithm], 
                                               capture_output=True, text=True, check=True)
                        result_json = json.loads(process.stdout.strip())
                        
                        if result_json.get('success', False):
                            hmac_value = result_json['hmac']
                            
                            # Format the output based on user preference
                            if output_format == 'HEX':
                                formatted_result = hmac_value.upper()
                            elif output_format == 'base64':
                                # Convert hex to base64
                                hex_bytes = bytes.fromhex(hmac_value)
                                formatted_result = base64.b64encode(hex_bytes).decode('ascii')
                            else:  # hex (lowercase)
                                formatted_result = hmac_value.lower()
                            
                            context['result'] = formatted_result
                            context['implementation_used'] = 'C++ Native Implementation'
                            
                            # Prepare step-by-step visualization data
                            steps = result_json.get('steps', {})
                            context['steps'] = {
                                'original_key': steps.get('originalKey', ''),
                                'processed_key': steps.get('processedKey', ''),
                                'key_analysis': steps.get('keyAnalysis', ''),
                                'inner_pad': steps.get('innerPad', ''),
                                'outer_pad': steps.get('outerPad', ''),
                                'inner_key_material': steps.get('innerKeyMaterial', ''),
                                'outer_key_material': steps.get('outerKeyMaterial', ''),
                                'message_hex': steps.get('messageHex', ''),
                                'inner_hash': steps.get('innerHash', ''),
                                'outer_input': steps.get('outerInput', ''),
                                'final_hmac': steps.get('finalHmac', ''),
                                'block_size': steps.get('blockSize', 64),
                                'algorithm': steps.get('algorithm', algorithm.upper())
                            }
                        else:
                            raise subprocess.CalledProcessError(1, exe_path, result_json.get('error', 'Unknown error'))
                    
                    return render(request, 'hmac.html', context)
                
            except (subprocess.CalledProcessError, OSError, FileNotFoundError, json.JSONDecodeError) as e:
                # Fall back to Python implementation
                print(f"C++ HMAC failed, falling back to Python: {e}")
                pass

            # Python fallback implementation
            try:
                from Algorithm.Crypto_Fallback.Python.HMAC.HMAC import HMACHash
                
                if operation == 'verify':
                    if not expected_hmac:
                        context['result'] = "Error: Expected HMAC is required for verification."
                        return render(request, 'hmac.html', context)
                    
                    generated_hmac, matches = HMACHash.verify_hmac(
                        input_text, secret_key, expected_hmac, algorithm, output_format
                    )
                    
                    if matches:
                        context['result'] = f"✅ HMAC verification successful! The message is authentic.\nGenerated: {generated_hmac}"
                    else:
                        context['result'] = f"❌ HMAC verification failed! The message may have been tampered with.\nGenerated: {generated_hmac}\nExpected: {expected_hmac}"
                    
                    context['implementation_used'] = 'Python HMAC Library'
                    
                else:
                    # Generate HMAC with Python implementation
                    if algorithm == 'sha256':
                        # Use our detailed implementation for step visualization
                        hmac_result, step_details = hmac_fallback(input_text, secret_key)
                        
                        # Format the output based on user preference
                        if output_format == 'HEX':
                            context['result'] = hmac_result.upper()
                        elif output_format == 'base64':
                            hex_bytes = bytes.fromhex(hmac_result)
                            context['result'] = base64.b64encode(hex_bytes).decode('ascii')
                        else:  # hex (lowercase)
                            context['result'] = hmac_result.lower()
                        
                        context['implementation_used'] = 'Python Custom Implementation'
                        context['steps'] = step_details
                    else:
                        # Use standard library for other algorithms
                        hmac_result = HMACHash.generate_hmac(input_text, secret_key, algorithm, output_format)
                        context['result'] = hmac_result
                        context['implementation_used'] = 'Python HMAC Library'
                        
            except ImportError:
                # Final fallback to basic Python hmac library
                try:
                    import hmac
                    import hashlib
                    
                    # Map algorithm names to hashlib functions
                    hash_algorithms = {
                        'md5': hashlib.md5,
                        'sha1': hashlib.sha1,
                        'sha224': hashlib.sha224,
                        'sha256': hashlib.sha256,
                        'sha384': hashlib.sha384,
                        'sha512': hashlib.sha512
                    }
                    
                    if algorithm not in hash_algorithms:
                        context['result'] = f"Error: Unsupported algorithm: {algorithm}"
                        return render(request, 'hmac.html', context)
                    
                    hash_func = hash_algorithms[algorithm]
                    hmac_obj = hmac.new(
                        secret_key.encode('utf-8'),
                        input_text.encode('utf-8'),
                        hash_func
                    )
                    
                    if operation == 'verify':
                        if not expected_hmac:
                            context['result'] = "Error: Expected HMAC is required for verification."
                            return render(request, 'hmac.html', context)
                        
                        # Format the generated HMAC based on output format
                        if output_format == 'HEX':
                            generated_hmac = hmac_obj.hexdigest().upper()
                        elif output_format == 'base64':
                            import base64
                            generated_hmac = base64.b64encode(hmac_obj.digest()).decode('ascii')
                        else:  # hex (lowercase)
                            generated_hmac = hmac_obj.hexdigest().lower()
                        
                        # Compare HMACs (case-insensitive for hex)
                        if output_format.lower() in ['hex']:
                            matches = generated_hmac.lower() == expected_hmac.lower()
                        else:
                            matches = generated_hmac == expected_hmac
                        
                        if matches:
                            context['result'] = f"✅ HMAC verification successful! The message is authentic.\nGenerated: {generated_hmac}"
                        else:
                            context['result'] = f"❌ HMAC verification failed! The message may have been tampered with.\nGenerated: {generated_hmac}\nExpected: {expected_hmac}"
                    else:
                        # Format the output based on user preference
                        if output_format == 'HEX':
                            context['result'] = hmac_obj.hexdigest().upper()
                        elif output_format == 'base64':
                            import base64
                            context['result'] = base64.b64encode(hmac_obj.digest()).decode('ascii')
                        else:  # hex (lowercase)
                            context['result'] = hmac_obj.hexdigest().lower()
                    
                    context['implementation_used'] = 'Python Standard Library'
                    
                except Exception as e:
                    context['result'] = f"Error generating HMAC: {str(e)}"
                    context['implementation_used'] = 'Error'

            except Exception as e:
                context['result'] = f"Error generating HMAC: {str(e)}"
                context['implementation_used'] = 'Error'

        except Exception as e:
            context['result'] = f"Error generating HMAC: {str(e)}"
            context['implementation_used'] = 'Error'

        return render(request, 'hmac.html', context)

    else:
        # If GET request, redirect to hmac_view
        return hmac_view(request)
