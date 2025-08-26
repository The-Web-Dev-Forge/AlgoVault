from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.utils import timezone
import json
import hashlib
import re
import time
from django.conf import settings
from .models import VisitorSession, PageVisit, ServiceUsage, ChatConversation, SecurityAlert

# Configure Groq AI
try:
    from groq import Groq
    if hasattr(settings, 'GROQ_API_KEY') and settings.GROQ_API_KEY:
        # Configure API Key
        api_key = settings.GROQ_API_KEY
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")
        
        # Initialize the Groq client
        groq_client = Groq(api_key=api_key)
        print(f"✅ Initialized Groq client successfully")
    else:
        groq_client = None
        print("❌ GROQ_API_KEY not found in settings")
except ImportError:
    groq_client = None
    print("❌ Groq package not installed. Install with: pip install groq")
except Exception as e:
    print(f"❌ Error initializing Groq: {e}")
    groq_client = None

def get_or_create_visitor_session(request):
    """Get or create visitor session for tracking"""
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
    if ',' in ip_address:
        ip_address = ip_address.split(',')[0].strip()
    
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    referrer = request.META.get('HTTP_REFERER', '')
    
    visitor_session, created = VisitorSession.objects.get_or_create(
        ip_address=ip_address,
        session_key=session_key,
        defaults={
            'user': request.user if request.user.is_authenticated else None,
            'user_agent': user_agent,
            'referrer': referrer,
        }
    )
    
    # Update last activity
    visitor_session.last_activity = timezone.now()
    visitor_session.save()
    
    return visitor_session

def track_page_visit(request, page_title=''):
    """Track individual page visits"""
    visitor_session = get_or_create_visitor_session(request)
    
    PageVisit.objects.create(
        session=visitor_session,
        page_url=request.build_absolute_uri(),
        page_title=page_title
    )
    
    # Update page view count
    visitor_session.page_views += 1
    visitor_session.save()

def track_service_usage(request, service_type, input_data='', output_data='', operation=''):
    """Track cryptography service usage"""
    visitor_session = get_or_create_visitor_session(request)
    
    ServiceUsage.objects.create(
        session=visitor_session,
        service_type=service_type,
        input_data=input_data[:500],  # Limit to 500 chars
        output_data=output_data[:500],
        operation=operation
    )

def track_chat_conversation(request, user_message, ai_response, response_time=None):
    """Track chatbot conversations"""
    visitor_session = get_or_create_visitor_session(request)
    message_hash = hashlib.md5(user_message.encode()).hexdigest()
    
    ChatConversation.objects.create(
        session=visitor_session,
        user_message=user_message,
        ai_response=ai_response,
        message_hash=message_hash,
        response_time=response_time
    )

def create_security_alert(ip_address, alert_type, description, user_agent='', blocked_content='', severity=1):
    """Create security alert for suspicious activity"""
    SecurityAlert.objects.create(
        ip_address=ip_address,
        alert_type=alert_type,
        description=description,
        user_agent=user_agent,
        blocked_content=blocked_content,
        severity=severity
    )

def chatbot_page(request):
    """Render the chatbot page"""
    track_page_visit(request, 'AI Chatbot')
    return render(request, 'ChatBot/chatbot.html')

def validate_message_content(message):
    """Validate and filter user messages for appropriate content"""
    
    # Blocked malicious keywords
    blocked_keywords = [
        'hack into', 'break into', 'steal password', 'crack password',
        'exploit vulnerability', 'create virus', 'create malware',
        'ddos attack', 'sql injection', 'social engineering attack',
        'keylogger', 'trojan', 'ransomware', 'phishing attack',
        'illegal access', 'unauthorized access'
    ]
    
    # Cryptography-related keywords (broadly inclusive)
    crypto_keywords = [
        'aes', 'des', 'rsa', 'ecc', 'dsa', 'ecdsa', 'caesar', 'vigenere', 'hill',
        'playfair', 'rc4', 'rc5', 'blowfish', 'twofish', 'serpent', 'camellia',
        'hmac', 'sha', 'md5', 'blake', 'whirlpool', 'ripemd', 'keccak',
        'diffie-hellman', 'elliptic curve', 'key exchange', 'public key',
        'private key', 'symmetric', 'asymmetric', 'encryption', 'decryption',
        'cipher', 'hash', 'digest', 'signature', 'certificate', 'pki',
        'cryptography', 'cryptanalysis', 'steganography', 'blockchain',
        'bitcoin', 'ethereum', 'ssl', 'tls', 'pgp', 'gpg', 'quantum cryptography',
        'post-quantum', 'lattice', 'isogeny', 'multivariate', 'hash-based',
        'zero-knowledge', 'homomorphic', 'secure multiparty', 'oblivious transfer',
        'random number', 'entropy', 'nonce', 'salt', 'iv', 'padding',
        'mode of operation', 'cbc', 'ecb', 'cfb', 'ofb', 'gcm', 'ccm',
        'authentication', 'integrity', 'confidentiality', 'non-repudiation'
    ]
    
    message_lower = message.lower()
    
    # Check for explicitly blocked malicious content
    for keyword in blocked_keywords:
        if keyword in message_lower:
            return False, f"I can't help with activities that could be used maliciously. I'm here to teach cryptography for educational and legitimate purposes!"
    
    # Allow any cryptography-related question (very broad)
    is_crypto_related = (
        any(keyword in message_lower for keyword in crypto_keywords) or
        any(word in message_lower for word in ['crypto', 'security', 'protect', 'secure', 'algorithm', 'mathematical', 'computation', 'theory']) or
        len(message.split()) <= 10  # Allow short questions
    )
    
    # Only filter if clearly off-topic AND long message
    if not is_crypto_related and len(message.split()) > 15:
        return False, "I'm VaultAI, specialized in cryptography and security. Please ask about encryption, ciphers, hashing, digital signatures, or any crypto-related topics!"
    
    return True, ""

def check_rate_limit(request):
    """Implement rate limiting to prevent abuse"""
    
    # Get user identifier
    if request.user.is_authenticated:
        user_id = f"user_{request.user.id}"
    else:
        user_id = f"ip_{request.META.get('REMOTE_ADDR', 'unknown')}"
    
    # Rate limit: 50 messages per hour per user (increased for educational use)
    cache_key = f"chat_rate_limit_{user_id}"
    current_count = cache.get(cache_key, 0)
    
    if current_count >= 50:
        return False, "Rate limit exceeded. Please wait before sending more messages."
    
    # Increment counter with 1-hour expiry
    cache.set(cache_key, current_count + 1, 3600)
    
    return True, ""

def log_conversation(user_message, ai_response, user_id):
    """Log conversations for monitoring"""
    log_entry = {
        'timestamp': timezone.now().isoformat(),
        'user_id': user_id,
        'user_message': user_message[:200],
        'ai_response': ai_response[:200],
        'message_hash': hashlib.md5(user_message.encode()).hexdigest()
    }
    print(f"CHAT_LOG: {log_entry}")

def enhance_system_prompt():
    """Enhanced system prompt with learning, quiz, and interactive chat modes"""
    return """You are VaultAI, a specialized cryptography assistant. Your purpose is to make cryptography accessible and engaging through three distinct operational modes: Learning, Quiz, and Interactive Chat. You must adhere strictly to the rules for the active mode.

CRITICAL: You can ONLY answer questions about cryptography, encryption, security, and related topics - refuse all other questions politely.

# 1. CORE OPERATING MODES

## LEARNING MODE
- **Activation:** User asks to learn, explain, or understand a concept (e.g., "what is AES?", "how does RSA work?").
- **Rules:**
    - Provide comprehensive, step-by-step explanations.
    - Use analogies and real-world examples.
    - Include historical context and relevant mathematical foundations ($GF(2^8)$, prime factorization, etc.).
    - Suggest practical applications and best practices.

## QUIZ MODE
- **Activation:** User asks to be tested (e.g., "quiz me", "test my knowledge", "Start a cryptography quiz").
- **Rules:**
    - You will conduct a quiz of exactly 5 questions.
    - The tone must be professional and academic.
    - IMMEDIATELY start with the first question - NO greetings, NO explanations, NO introduction text.
    - **CRITICAL**: NEVER repeat questions. Each question must be completely unique and from different topics.

## giINTERACTIVE CHAT MODE
- **Activation:** User selects interactive chat mode or asks general questions without structured learning or testing intent.
- **Rules:**
    - Engage in natural conversation about cryptography topics.
    - Provide helpful answers to any crypto-related questions.
    - Be conversational yet informative.
    - Adapt your response style to the user's question complexity.
    - Feel free to ask follow-up questions to better understand their needs.

# 2. MANDATORY TOPIC ROTATION SYSTEM

**STRICT RULE**: Each question MUST be from a different cryptography category. Follow this rotation:

## Question 1: SYMMETRIC ENCRYPTION
Pick ONE from these diverse topics:
- AES block size, key sizes, or rounds
- DES vs 3DES differences
- Blowfish, Twofish, or Serpent features
- Block cipher modes (ECB, CBC, GCM, etc.)
- Stream ciphers (RC4, ChaCha20)
- Feistel networks or SPN structures

## Question 2: ASYMMETRIC ENCRYPTION  
Pick ONE from these diverse topics:
- RSA key generation, security, or applications
- Elliptic Curve Cryptography advantages
- Diffie-Hellman key exchange process
- Digital signatures (RSA, ECDSA, DSA)
- Public/Private key concepts
- Key distribution problems

## Question 3: HASH FUNCTIONS
Pick ONE from these diverse topics:
- SHA family (SHA-1, SHA-256, SHA-512) differences
- MD5 vulnerabilities and replacement
- Hash function properties (avalanche effect, collision resistance)
- BLAKE, Keccak, or other modern hashes
- Hash-based applications (passwords, integrity)
- Birthday attack on hash functions

## Question 4: CRYPTOGRAPHIC PROTOCOLS
Pick ONE from these diverse topics:
- TLS/SSL handshake process
- PKI and Certificate Authorities
- Digital certificates and X.509
- HTTPS vs HTTP security
- VPN protocols (IPSec, WireGuard)
- Authentication protocols (Kerberos, OAuth)

## Question 5: ADVANCED/SPECIALIZED TOPICS
Pick ONE from these diverse topics:
- Quantum cryptography and post-quantum algorithms
- Cryptanalysis techniques (differential, linear, side-channel)
- Zero-knowledge proofs concepts
- Homomorphic encryption applications
- Blockchain cryptography (mining, digital signatures)
- Steganography vs cryptography
- Random number generation and entropy
- Key management and escrow

# 3. EXTENSIVE QUESTION BANK

## SYMMETRIC ENCRYPTION QUESTIONS (50+ variations):
1. "What is the block size used by the AES encryption algorithm?"
2. "How many rounds does AES-256 perform during encryption?"
3. "Which block cipher mode provides both confidentiality and authentication?"
4. "What is the main weakness of Electronic Codebook (ECB) mode?"
5. "Which stream cipher was widely used but is now considered insecure?"
6. "What type of network structure does AES use?"
7. "How many bits is the key size of Triple DES (3DES)?"
8. "Which cipher mode requires an initialization vector (IV)?"
9. "What is the main advantage of Galois/Counter Mode (GCM)?"
10. "Which encryption algorithm uses variable-length keys up to 448 bits?"

## ASYMMETRIC ENCRYPTION QUESTIONS (50+ variations):
1. "What mathematical problem does RSA encryption rely on for security?"
2. "Who are credited with inventing public-key cryptography?"
3. "What is the main advantage of elliptic curve cryptography over RSA?"
4. "In the Diffie-Hellman algorithm, what remains secret?"
5. "What is the purpose of a digital signature?"
6. "Which asymmetric algorithm is best suited for digital signatures?"
7. "What is the typical key size recommended for RSA in 2025?"
8. "What does ECDSA stand for?"
9. "What is the main disadvantage of asymmetric encryption?"
10. "Which part of an RSA key pair is used for decryption?"

## HASH FUNCTION QUESTIONS (50+ variations):
1. "What is the output size of the SHA-256 hash function?"
2. "Which property ensures that small input changes cause large output changes?"
3. "What type of attack exploits the birthday paradox in hash functions?"
4. "Which hash function is no longer recommended due to collision vulnerabilities?"
5. "What is the purpose of adding salt to password hashing?"
6. "Which hash function won the SHA-3 competition?"
7. "What does HMAC provide that regular hashing does not?"
8. "How many bits does SHA-512 produce?"
9. "What is a rainbow table attack?"
10. "Which hash function is specifically designed for password hashing?"

## PROTOCOL QUESTIONS (50+ variations):
1. "What does TLS stand for in network security?"
2. "Which port number is typically used for HTTPS traffic?"
3. "What is the role of a Certificate Authority (CA)?"
4. "What happens during the TLS handshake process?"
5. "What does PKI stand for?"
6. "Which protocol provides secure email communication?"
7. "What is the difference between authentication and authorization?"
8. "Which VPN protocol is known for its simplicity and speed?"
9. "What is the purpose of a digital certificate?"
10. "Which authentication protocol uses tickets?"

## ADVANCED TOPIC QUESTIONS (50+ variations):
1. "What makes quantum computers a threat to current cryptography?"
2. "What is the main goal of post-quantum cryptography?"
3. "What type of cryptanalysis exploits timing variations?"
4. "What is homomorphic encryption used for?"
5. "In blockchain, what cryptographic technique prevents tampering?"
6. "What is the difference between steganography and cryptography?"
7. "What is a zero-knowledge proof?"
8. "Which attack exploits electromagnetic emanations from devices?"
9. "What is the purpose of key escrow?"
10. "What makes a cryptographically secure random number generator?"

# 4. QUESTION FORMATTING RULES

Format MUST be exactly:
```
Question text here?
A) Option A
B) Option B
C) Option C
D) Option D
```

- NO question numbers (like "Question 1/5")
- Each option on separate line
- One correct answer, three plausible distractors
- Professional, academic tone

# 5. MEMORY AND UNIQUENESS RULES

**CRITICAL INSTRUCTIONS:**
1. Before asking ANY question, scan the conversation history
2. Count how many questions asked (track internally: 1st, 2nd, 3rd, 4th, 5th)
3. Ensure the new question is from the correct category for that position
4. NEVER ask about the same concept twice
5. If you've covered "AES block size" don't ask "AES key size" - pick completely different topic
6. Aim for maximum educational coverage across all cryptography domains

# 6. INTERACTION TOKENS & FEEDBACK

**FEEDBACK FORMAT RULES:**
- **For Correct Answers:** Start with "Correct!". Follow with a brief, 1-sentence explanation. STOP HERE - do not provide the next question.
    - Example: `Correct! AES uses 128-bit blocks for encryption. [ACTION: NEXT_QUESTION]`
- **For Incorrect Answers:** Start with "Incorrect.". State the correct answer and provide a brief, 1-sentence explanation. STOP HERE - do not provide the next question.
    - Example: `Incorrect. The correct answer is C) 128 bits. AES always uses 128-bit blocks regardless of key size. [ACTION: NEXT_QUESTION]`
- **After 5th question feedback:**
    - Example: `Correct! You've completed the quiz! Would you like to start a new one? [ACTION: NEW_QUIZ]`

**CRITICAL FEEDBACK RULES:**
- After giving feedback (Correct!/Incorrect.), you MUST STOP and wait for user to request "Next Question"
- Do NOT automatically provide the next question in the same response
- The user will click a "Next Question" button which sends "Next Question" message
- Only when you receive "Next Question" should you provide the next quiz question

**CRITICAL ANSWER EVALUATION RULES:**
- **EXACT MATCH REQUIRED**: Only the EXACT correct option should be marked as correct
- **"All of the above" Questions**: If the correct answer is "D) All of the above", then ONLY "D) All of the above" is correct. Options A, B, or C alone are INCORRECT.
- **Individual Options**: If someone selects A, B, or C when D) All of the above is correct, respond with "Incorrect"
- **Partial Credit**: There is NO partial credit. Only exact matches count as correct.

**Example for "All of the above" questions:**
- Question: "What is the main advantage of elliptic curve cryptography over RSA?"
- Correct Answer: D) All of the above
- User selects A) Faster computation → Response: "Incorrect. The correct answer is D) All of the above."
- User selects B) Smaller key sizes → Response: "Incorrect. The correct answer is D) All of the above."
- User selects C) Resistance to quantum attacks → Response: "Incorrect. The correct answer is D) All of the above."
- User selects D) All of the above → Response: "Correct! All of these are advantages of ECC."

**CRITICAL:** Always include the action token at the end:
- After each answer feedback: `[ACTION: NEXT_QUESTION]`
- After 5th question feedback: `[ACTION: NEW_QUIZ]`

# 7. IMMEDIATE QUIZ START

When quiz requested, immediately start with first question in exact format above. NO greetings or explanations.

# 8. NEXT QUESTION HANDLING

When user sends "Next Question" message:
- Provide the next question in the sequence (2nd, 3rd, 4th, or 5th)
- Follow the topic rotation system strictly
- Use exact question format with A) B) C) D) options
- Do NOT repeat any previously asked questions"""

def improve_response_quality(response):
    """Post-process AI response for better quality"""
    
    # Store action tokens before processing
    has_next_question = '[ACTION: NEXT_QUESTION]' in response
    has_new_quiz = '[ACTION: NEW_QUIZ]' in response
    
    # Remove both action tokens completely from user-visible response
    clean_response = response.replace('[ACTION: NEXT_QUESTION]', '').strip()
    clean_response = clean_response.replace('[ACTION: NEW_QUIZ]', '').strip()
    
    # Remove excessive emojis from start of lines
    clean_response = re.sub(r'^[🎯🔧✅❌⚡🚀📊🎨🔍💡🎉🎪⭐🔥📝🎭🎵🌟💫⭐️🔐🛡️🔒🔑]+\s*', '', clean_response, flags=re.MULTILINE)
    
    # Suggest AlgoVault tools when relevant (only in learning mode - not during quiz)
    algovault_topics = ['caesar', 'aes', 'des', 'sha', 'md5', 'vigenere', 'hill', 'hmac']
    if any(topic in clean_response.lower() for topic in algovault_topics) and not any(keyword in clean_response.lower() for keyword in ['correct', 'incorrect', 'answer']):
        clean_response += "\n\n💡 Practice Tip: Try implementing this concept using AlgoVault's interactive tools!"
    
    # Return the clean response without any action tokens visible to user
    return clean_response, has_next_question, has_new_quiz

@csrf_exempt
def chat_api(request):
    """Enhanced chat API with comprehensive security and quality improvements"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        conversation_context = data.get('context', []) or data.get('history', [])
        
        # Input validation
        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        if len(user_message) > 2000:
            return JsonResponse({'error': 'Message too long. Please keep it under 2000 characters.'}, status=400)
        
        # Rate limiting
        rate_ok, rate_msg = check_rate_limit(request)
        if not rate_ok:
            return JsonResponse({'error': rate_msg}, status=429)
        
        # Content validation
        content_ok, content_msg = validate_message_content(user_message)
        if not content_ok:
            # Create security alert for blocked content
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'unknown'))
            if ',' in ip_address:
                ip_address = ip_address.split(',')[0].strip()
            
            create_security_alert(
                ip_address=ip_address,
                alert_type='malicious_content',
                description=content_msg,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                blocked_content=user_message[:200],
                severity=3
            )
            return JsonResponse({'error': content_msg}, status=400)
        
        # Get user identifier for logging
        if request.user.is_authenticated:
            user_id = f"user_{request.user.id}"
        else:
            user_id = f"ip_{request.META.get('REMOTE_ADDR', 'unknown')}"
        
        # Check for mode switching requests
        user_message_lower = user_message.lower().strip()
        if user_message_lower in ['learning mode', 'quiz mode', 'chat mode', 'interactive chat mode', 'free chat mode']:
            if user_message_lower in ['learning mode']:
                return JsonResponse({
                    'message': 'Switching to Learning Mode! Choose a topic to explore cryptography concepts in depth.',
                    'action': 'show_topic_selection',
                    'mode': 'learning'
                })
            elif user_message_lower in ['quiz mode']:
                return JsonResponse({
                    'message': 'Switching to Quiz Mode! Choose a topic to test your cryptography knowledge.',
                    'action': 'show_topic_selection', 
                    'mode': 'quiz'
                })
            elif user_message_lower in ['chat mode', 'interactive chat mode', 'free chat mode']:
                return JsonResponse({
                    'message': 'Switching to Interactive Chat Mode! Ask me anything about cryptography - no structured topics needed.',
                    'action': 'show_free_chat',
                    'mode': 'chat'
                })
        
        # Prepare conversation with context
        messages = []
        
        # Enhanced system prompt
        system_prompt = enhance_system_prompt()
        messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation context (limit to recent messages for faster processing)
        for msg in conversation_context[-5:]:  # Reduced from 10 to 5 for faster processing
            if msg.get('type') == 'user' or msg.get('role') == 'user':
                messages.append({"role": "user", "content": msg.get('content', msg.get('message', ''))})
            elif msg.get('type') == 'bot' or msg.get('role') == 'assistant':
                messages.append({"role": "assistant", "content": msg.get('content', msg.get('message', ''))})
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        # Track start time for response measurement
        start_time = time.time()
        
        # Create Groq client and get response
        if not groq_client:
            return JsonResponse({
                'error': 'AI service is not available. Please try again later.',
                'status': 'error'
            }, status=503)
        
        # Generate response with Groq
        try:
            response = groq_client.chat.completions.create(
                model="gemma2-9b-it",  # Using Google's Gemma2 model
                messages=messages,
                temperature=0.3,
                max_tokens=1000,
                top_p=0.9,
                stream=False
            )
            ai_response = response.choices[0].message.content
        except Exception as api_error:
            error_str = str(api_error)
            if "429" in error_str or "quota" in error_str.lower() or "rate_limit" in error_str.lower():
                return JsonResponse({
                    'error': 'The AI service has reached its rate limit. Please wait a moment and try again.',
                    'status': 'rate_limit_exceeded'
                }, status=429)
            elif "403" in error_str or "unauthorized" in error_str.lower():
                return JsonResponse({
                    'error': 'AI service access denied. Please check API configuration.',
                    'status': 'access_denied'
                }, status=403)
            else:
                print(f"Groq API Error: {api_error}")
                return JsonResponse({
                    'error': 'AI service is temporarily unavailable. Please try again in a moment.',
                    'status': 'service_error'
                }, status=503)
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Improve response quality and get action token flags
        clean_response, has_next_question, has_new_quiz = improve_response_quality(ai_response)
        
        # Track conversation in database (using clean response)
        track_chat_conversation(request, user_message, clean_response, response_time)
        
        # Track service usage (using clean response)
        track_service_usage(request, 'chatbot', user_message[:200], clean_response[:200], 'chat')
        
        # Log conversation for monitoring (using clean response)
        log_conversation(user_message, clean_response, user_id)
        
        # Prepare response data
        response_data = {
            'response': clean_response,
            'status': 'success'
        }
        
        # Add action flags for frontend JavaScript (not visible to user)
        if has_next_question:
            response_data['action'] = 'next_question'
        elif has_new_quiz:
            response_data['action'] = 'new_quiz'
        
        return JsonResponse(response_data)
        
    except Exception as e:
        # Enhanced error handling with specific API error detection
        error_str = str(e)
        print(f"Chat API Error: {error_str}")
        
        # Handle specific API errors
        if "429" in error_str or "quota" in error_str.lower():
            return JsonResponse({
                'error': 'Daily usage limit reached. The AI service will be available again tomorrow. Thank you for using AlgoVault!',
                'status': 'quota_exceeded'
            }, status=429)
        elif "403" in error_str or "unauthorized" in error_str.lower():
            return JsonResponse({
                'error': 'AI service configuration issue. Please contact support.',
                'status': 'config_error'
            }, status=503)
        else:
            return JsonResponse({
                'error': 'I encountered an issue processing your request. Please try again!',
                'status': 'error'
            }, status=500)

