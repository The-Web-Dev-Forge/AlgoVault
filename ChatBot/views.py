from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
import google.generativeai as genai
from django.conf import settings

# Configure Gemini AI
try:
    import google.generativeai as genai
    if settings.GEMINI_API_KEY:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # Use only working models (tested and verified)
        model_names = [
            'gemini-1.5-flash',        # Primary - Working perfectly
        ]
        
        model = None
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                print(f"✅ Successfully initialized Gemini model: {model_name}")
                break
            except Exception as e:
                print(f"❌ Failed to initialize {model_name}: {e}")
                continue
        
        if not model:
            print("❌ Failed to initialize any Gemini model")
    else:
        model = None
        print("❌ GEMINI_API_KEY not found in settings")
except ImportError:
    genai = None
    model = None
except Exception as e:
    print(f"Error initializing Gemini: {e}")
    genai = None
    model = None

def chatbot_page(request):
    """Render the chatbot page"""
    return render(request, 'ChatBot/chatbot.html')

@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    """Handle chat API requests with advanced AI training"""
    try:
        if not genai:
            return JsonResponse({
                'error': 'Google Generative AI package is not installed. Please install it with: pip install google-generativeai'
            }, status=500)
            
        if not settings.GEMINI_API_KEY:
            return JsonResponse({
                'error': 'Gemini API key not configured. Please add your API key to the .env file.'
            }, status=500)
        
        if not model:
            return JsonResponse({
                'error': 'AI model not initialized. Please check your API key configuration.'
            }, status=500)
        
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # Generate enhanced response using all 4 training methods
        enhanced_prompt = create_enhanced_training_prompt(user_message)
        
        # Generate response using Gemini
        response = model.generate_content(enhanced_prompt)
        
        # Apply response formatting template
        formatted_response = format_response_with_template(response.text, user_message)
        
        return JsonResponse({
            'response': formatted_response,
            'status': 'success'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'An error occurred: {str(e)}'
        }, status=500)


def create_enhanced_training_prompt(user_message):
    """
    METHOD 1: Enhanced System Prompting with Personality & Guidelines
    """
    system_prompt = """🔐 You are VaultAI, the expert AI assistant for AlgoVault - the ultimate cryptography learning platform!

🎯 PERSONALITY: Professional, educational, encouraging, patient crypto teacher who makes complex concepts simple
🧠 EXPERTISE: Cryptography, cybersecurity, mathematics, computer science, algorithm analysis
📚 RESPONSE STYLE: START CONCISE, then offer more depth

🛠️ AVAILABLE TOOLS ON ALGOVAULT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📜 Classical Ciphers: Caesar, Vigenère, Hill, Playfair
🔒 Modern Encryption: AES, DES, RSA encryption  
🔑 Hashing Functions: MD5, SHA-256, SHA-512
🤝 Key Exchange: Diffie-Hellman Protocol
🤖 AI Assistance: Interactive learning support

🎓 CRITICAL RESPONSE GUIDELINES:
1. **START WITH BASIC ANSWER** - Give a simple, 2-3 sentence explanation first
2. **ASK FOR DEPTH** - Always end with: "Want me to explain more?" or "Need more details?"
3. **USE SIMPLE ANALOGIES** - Locks, keys, secret codes for basic explanations
4. **BE CONCISE FIRST** - Don't overwhelm with information upfront
5. **OFFER ALGOVAULT TOOLS** - Suggest relevant interactive tools
6. **REDIRECT NON-CRYPTO** - Politely guide back to cryptography topics
7. **STRATEGIC EMOJIS** - Use sparingly for engagement

🎯 RESPONSE PATTERN:
- **Basic Question**: Simple answer (2-3 lines) + "Want more details?"
- **Follow-up**: Then provide detailed explanation
- **Advanced Question**: Can give more technical depth immediately
- Always suggest: "Try it on AlgoVault!" for hands-on learning"""

    # METHOD 2: Few-Shot Examples for Consistent Style
    few_shot_examples = """
🎓 EXAMPLE CONVERSATIONS TO LEARN FROM:

User: "What is encryption?"
VaultAI: "🔐 Encryption is like putting your message in a locked box - it scrambles text so only someone with the right key can read it!

🚀 Want me to explain the process step-by-step? Or try our Caesar Cipher tool on AlgoVault to see it in action!"

User: "How does AES work?"
VaultAI: "🔒 AES breaks your data into blocks and applies multiple rounds of mathematical transformations using your secret key - it's military-grade protection!

� Want the technical details about the rounds and transformations? Or check out our interactive AES tool on AlgoVault first!"

User: "I'm confused about hash functions"
VaultAI: "🔍 Hash functions create a unique 'digital fingerprint' from any input - like a one-way mathematical stamp that can't be reversed!

💡 Want me to explain how they work with examples? Or try our MD5 and SHA-512 tools on AlgoVault to see them in action!"

User: "Tell me more about AES rounds"
VaultAI: "🔄 Great! AES uses 10-14 rounds depending on key size. Each round has 4 steps:
1. SubBytes - Substitutes bytes using S-box
2. ShiftRows - Shifts row positions  
3. MixColumns - Mixes column data
4. AddRoundKey - XORs with round key

🎯 This creates avalanche effect - tiny input change = completely different output! Try our AES tool to see each round in action!"

Now respond to this user question with the CONCISE-FIRST approach:"""

    # METHOD 3: Context-Aware User Level Detection
    user_level = detect_user_level(user_message)
    context_guidance = get_contextual_guidance(user_level)

    # METHOD 4: Topic Detection for Response Templates
    topic_type = detect_topic_type(user_message)

    # Combine all methods into final prompt
    enhanced_prompt = f"""{system_prompt}

{few_shot_examples}

🎯 USER LEVEL DETECTED: {user_level.upper()}
{context_guidance}

🔍 TOPIC TYPE: {topic_type}

User Question: "{user_message}"

VaultAI Response:"""

    return enhanced_prompt


def detect_user_level(user_message):
    """METHOD 3: Detect user expertise level from their message"""
    message_lower = user_message.lower()
    
    # Advanced indicators
    advanced_keywords = [
        'mathematical', 'algorithm complexity', 'cryptanalysis', 'polynomial time',
        'computational complexity', 'discrete logarithm', 'elliptic curve',
        'boolean function', 'linear cryptanalysis', 'differential cryptanalysis',
        'side-channel attack', 'quantum cryptography', 'lattice-based',
        'provable security', 'semantic security', 'perfect forward secrecy'
    ]
    
    # Intermediate indicators  
    intermediate_keywords = [
        'how does', 'explain the process', 'what are the steps', 'implementation',
        'algorithm', 'technical details', 'compare', 'difference between',
        'advantages', 'disadvantages', 'security analysis', 'key size'
    ]
    
    # Beginner indicators
    beginner_keywords = [
        'what is', 'what are', 'i dont understand', 'confused', 'explain simply',
        'basic', 'introduction', 'new to', 'beginner', 'help me understand',
        'easy explanation', 'simple terms'
    ]
    
    if any(keyword in message_lower for keyword in advanced_keywords):
        return 'advanced'
    elif any(keyword in message_lower for keyword in intermediate_keywords):
        return 'intermediate'
    elif any(keyword in message_lower for keyword in beginner_keywords):
        return 'beginner'
    else:
        return 'intermediate'  # default


def get_contextual_guidance(user_level):
    """METHOD 3: Provide level-specific guidance"""
    guidance = {
        'beginner': """
🌟 GUIDANCE: This user is new to cryptography
• Give VERY SHORT basic answer first (1-2 sentences)
• Use simple analogies (locks, keys, secret codes)
• Always ask: "Want me to explain more?" or "Need more details?"
• Avoid technical terms in initial response
• Suggest Caesar Cipher as starting point""",
        
        'intermediate': """
🎯 GUIDANCE: This user understands basics but wants more depth
• Give concise answer first, then offer technical details
• Include proper terminology but explain it
• Ask: "Want the technical breakdown?" or "Need implementation details?"
• Balance theory with practical examples
• Suggest intermediate tools like AES or hash functions""",
        
        'advanced': """
🚀 GUIDANCE: This user has strong technical background
• Can give more detailed answer initially but still be concise
• Include mathematical foundations when relevant
• Ask: "Want me to dive deeper into the math?" or "Need attack analysis?"
• Reference academic concepts and research
• Suggest advanced topics and implementation details"""
    }
    return guidance.get(user_level, guidance['intermediate'])


def detect_topic_type(user_message):
    """METHOD 4: Detect the type of topic for response templating"""
    message_lower = user_message.lower()
    
    # Algorithm-specific questions
    algorithms = ['caesar', 'vigenere', 'hill', 'aes', 'des', 'rsa', 'md5', 'sha', 'diffie-hellman']
    if any(alg in message_lower for alg in algorithms):
        return 'algorithm'
    
    # Concept questions
    concepts = ['encryption', 'decryption', 'hash', 'cipher', 'key', 'cryptography', 'security']
    if any(concept in message_lower for concept in concepts):
        return 'concept'
    
    # Implementation questions
    if any(word in message_lower for word in ['implement', 'code', 'programming', 'how to build']):
        return 'implementation'
    
    # Comparison questions
    if any(word in message_lower for word in ['compare', 'difference', 'vs', 'versus', 'better']):
        return 'comparison'
    
    return 'general'


def format_response_with_template(response_text, user_message):
    """METHOD 4: Apply response templates for structured answers"""
    topic_type = detect_topic_type(user_message)
    user_level = detect_user_level(user_message)
    
    # Don't over-format if response is already well-structured
    if '🔐' in response_text or '🎯' in response_text:
        return response_text
    
    # For basic questions, ensure the response asks if user wants more detail
    basic_questions = ['what is', 'what are', 'explain', 'tell me about']
    is_basic_question = any(phrase in user_message.lower() for phrase in basic_questions)
    
    # Add follow-up question if missing and it's a basic question
    if is_basic_question and user_level == 'beginner':
        if '?' not in response_text[-50:]:  # Check if there's already a question at the end
            response_text += "\n\n🤔 Want me to explain more details?"
    
    # Add AlgoVault call-to-action if not present
    if 'algovault' not in response_text.lower():
        if topic_type == 'algorithm':
            response_text += "\n\n🚀 **Try it yourself:** Experience this algorithm hands-on with our interactive tools on AlgoVault!"
        elif topic_type == 'concept':
            response_text += "\n\n💡 **Hands-on learning:** Explore our comprehensive cryptography tools on AlgoVault!"
        else:
            response_text += "\n\n🎓 **Practice:** Try our interactive cryptography tools on AlgoVault!"
    
    return response_text
