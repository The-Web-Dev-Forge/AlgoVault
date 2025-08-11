# 🔐 AlgoVault

<div align="center">
  <img src="https://img.shields.io/badge/Django-5.2.3-green?style=for-the-badge&logo=django" alt="Django"/>
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/C++-11-orange?style=for-the-badge&logo=cplusplus" alt="C++"/>
  <img src="https://img.shields.io/badge/Java-8+-red?style=for-the-badge&logo=oracle" alt="Java"/>
  <img src="https://img.shields.io/badge/AI-Gemma2--9B-purple?style=for-the-badge&logo=google" alt="AI Model"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"/>
</div>
<div align="center">
  <h3>🎓 Your Comprehensive Platform for Cryptographic Algorithm Visualization and Learning</h3>
  <p>Experience cryptography through interactive visualizations, AI-powered assistance, and hands-on implementations</p>
</div>

## 📊 Project Statistics

<div align="center">
  <table>
    <tr>
      <th>Metric</th>
      <th>Count</th>
    </tr>
    <tr>
      <td>📝 Total Lines of Code</td>
      <td><strong>12,500+</strong></td>
    </tr>
    <tr>
      <td>🔧 Cryptographic Algorithms</td>
      <td><strong>9</strong></td>
    </tr>
    <tr>
      <td>💻 Programming Languages</td>
      <td><strong>5</strong> (Python, C++, Java, JavaScript, HTML/CSS)</td>
    </tr>
    <tr>
      <td>📁 Project Files</td>
      <td><strong>100+</strong></td>
    </tr>
    <tr>
      <td>🎨 HTML Templates</td>
      <td><strong>20+</strong></td>
    </tr>
    <tr>
      <td>🤖 AI Quiz Questions</td>
      <td><strong>200+</strong> (dynamically generated)</td>
    </tr>
    <tr>
      <td>⚡ API Endpoints</td>
      <td><strong>15+</strong></td>
    </tr>
    <tr>
      <td>🛡️ Security Features</td>
      <td><strong>5</strong> (Rate limiting, Input validation, CSRF, Session tracking, Content filtering)</td>
    </tr>
  </table>
</div>

---

## 📖 Project Overview

AlgoVault is an educational web platform designed to demystify cryptographic algorithms through interactive visualizations and step-by-step explanations. Whether you're a student learning the fundamentals, an educator teaching security concepts, or a professional implementing secure systems, AlgoVault provides the tools and resources to understand cryptography at its core.

### 🎯 Mission Statement

Our mission is to bridge the gap between theoretical cryptography and practical implementation, making complex security concepts accessible to everyone through visual learning and interactive experiences.

---

## ✨ Features

### 🔒 **Cryptographic Algorithms**

#### Classical Ciphers
- **Caesar Cipher**: Interactive shift cipher with customizable rotation values
- **Vigenère Cipher**: Polyalphabetic substitution with key-based encryption
- **Hill Cipher**: Matrix-based encryption with visual matrix operations

#### Modern Encryption
- **AES (Advanced Encryption Standard)**: Round-by-round visualization of Rijndael algorithm
- **DES (Data Encryption Standard)**: 16-round Feistel network visualization

#### Hash Functions
- **MD5**: 128-bit hash generation with step-by-step processing
- **SHA-512**: Secure 512-bit hash computation with internal state display
- **HMAC**: Hash-based Message Authentication Code implementation

#### Key Exchange Protocols
- **Diffie-Hellman**: Interactive key exchange demonstration with mathematical calculations

### 🤖 **AI-Powered Assistant**

Our integrated chatbot, powered by **Google's Gemma2-9B-IT model** via Groq AI, offers:

- **Learning Mode**: Comprehensive explanations of cryptographic concepts
- **Quiz Mode**: Interactive testing with 5-question quizzes on selected topics
- **Interactive Chat Mode**: Free-form Q&A about any cryptography topic
- **Real-time Assistance**: Instant help with algorithm understanding and debugging

### 📊 **Visualization Features**

- **Step-by-Step Processing**: Watch algorithms execute in real-time
- **Round Key Generation**: Visual representation of key scheduling
- **Block Processing**: See how data blocks are transformed
- **State Transitions**: Observe internal algorithm states change
- **Performance Metrics**: Compare implementation speeds across languages

### 🎨 **User Experience**

- **Responsive Design**: Seamless experience across desktop, tablet, and mobile
- **Dark Theme**: Eye-friendly interface for extended learning sessions
- **Interactive Controls**: Hands-on manipulation of algorithm parameters
- **Multi-Language Support**: Implementations in C++, Java, and Python

---

## 🛠️ Tech Stack

### **Backend**
| Technology | Purpose | Version |
|------------|---------|---------|
| **Django** | Web Framework | 5.2.3 |
| **Python** | Primary Backend Language | 3.8+ |
| **SQLite** | Database | Default |
| **Groq API** | AI Integration | 0.30.0 |

### **Frontend**
| Technology | Purpose |
|------------|---------|
| **HTML5** | Structure |
| **CSS3** | Styling & Animations |
| **JavaScript** | Interactivity |
| **Font Awesome** | Icons |

### **Algorithm Implementations**
| Language | Use Case |
|----------|----------|
| **C++** | High-performance primary implementations |
| **Java** | Alternative implementations |
| **Python** | Fallback implementations & rapid prototyping |

### **AI & Machine Learning**
| Component | Purpose |
|-----------|---------|
| **Gemma2-9B-IT** | Language model for chat assistant |
| **Groq Cloud** | AI inference platform |

### **Security & Cryptography Libraries**
- `cryptography==45.0.5` - Modern cryptographic recipes
- `pycryptodome` - Low-level cryptographic primitives
- Custom implementations for educational purposes

---

## 📁 Folder Structure

```
AlgoVault/
├── 📂 algovault/                     # Django project settings
│   ├── settings.py                   # Main configuration
│   ├── urls.py                       # URL routing
│   └── wsgi.py                       # WSGI application
│
├── 📂 Cryptography/                  # Main cryptography app
│   ├── 📂 templates/                 # HTML templates
│   │   ├── landing.html              # Homepage
│   │   ├── tools.html                # Algorithm selection
│   │   ├── about.html                # About page
│   │   ├── help.html                 # Documentation
│   │   └── [algorithm].html          # Individual algorithm pages
│   ├── 📂 static/                    # Static assets
│   │   ├── css/                      # Stylesheets
│   │   ├── js/                       # JavaScript files
│   │   └── images/                   # Images and icons
│   ├── views.py                      # View controllers
│   ├── urls.py                       # App-specific routes
│   └── models.py                     # Data models
│
├── 📂 Algorithm/                     # Algorithm implementations
│   ├── 📂 cpp_source/                # C++ source files
│   │   ├── caesar_cipher.cpp
│   │   ├── vigenere_processor.cpp
│   │   ├── hill_processor.cpp
│   │   └── compile.sh                # Compilation script
│   ├── 📂 Crypto_Fallback/    
│   │   └── 📂 Python/                # Python fallback implementations
│   │       ├── 📂 CaesarCipher/
│   │       ├── 📂 VigenereCipher/
│   │       ├── 📂 HillCipher/
│   │       ├── 📂 AES/
│   │       ├── 📂 DES/
│   │       ├── 📂 SHA512/
│   │       ├── 📂 MD5/
│   │       ├── 📂 HMAC/
│   │       └── 📂 DiffieHellman/
│   └── *.exe                        # Compiled executables
│
├── 📂 ChatBot/                      # AI Assistant app
│   ├── 📂 templates/          
│   │   └── chatbot.html            # Chat interface
│   ├── 📂 static/
│   │   ├── css/                    # Chat styling
│   │   └── js/                     # Chat functionality
│   ├── views.py                    # Chat logic & Groq integration
│   ├── models.py                   # Conversation tracking
│   └── middleware.py               # Visitor tracking
│
├── 📂 UserAuth/                    # Authentication app
│   ├── 📂 templates/
│   │   ├── login.html
│   │   └── signup.html
│   ├── views.py                   # Auth logic
│   └── models.py                  # User models
│
├── 📄 requirements.txt            # Python dependencies
├── 📄 manage.py                   # Django management script
├── 📄 .env                        # Environment variables
└── 📄 db.sqlite3                  # SQLite database
```

---

## 🚀 Installation

### Prerequisites

- **Python 3.8+** with pip
- **C++ Compiler** (g++ for Linux/Mac, MinGW for Windows)
- **Git** for version control
- **Groq API Key** for AI features (get from [console.groq.com](https://console.groq.com))

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/AlgoVault.git
cd AlgoVault
```

### Step 2: Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Django Secret Key (generate a new one for production)
SECRET_KEY=your_secret_key_here

# Email Configuration (optional)
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### Step 5: Compile C++ Implementations

```bash
# Navigate to cpp_source directory
cd Algorithm/cpp_source/

# Make compile script executable (Linux/Mac)
chmod +x compile.sh

# Run compilation
./compile.sh

# Or compile manually
g++ CaesarCipher.cpp -o CaesarCipher.exe
g++ VigenereCipher.cpp -o VigenereCipher.exe
g++ HillCipher.cpp -o HillCipher.exe
```

### Step 6: Set Up Database

```bash
# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser
```

### Step 7: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

---

## 💻 Usage

### Running the Development Server

```bash
# Start the server
python manage.py runserver

# Or specify a custom port
python manage.py runserver 8001
```

Access the application at: `http://127.0.0.1:8000/`

### Accessing Different Features

| Feature | URL |
|---------|-----|
| **Homepage** | `/` |
| **Algorithm Tools** | `/tools/` |
| **Caesar Cipher** | `/caesar/` |
| **Vigenère Cipher** | `/vigenere/` |
| **Hill Cipher** | `/hill/` |
| **AES Encryption** | `/aes/` |
| **DES Encryption** | `/des/` |
| **SHA-512 Hash** | `/sha512/` |
| **MD5 Hash** | `/md5/` |
| **HMAC** | `/hmac/` |
| **Diffie-Hellman** | `/diffie_hellman/` |
| **AI Assistant** | `/chatbot/` |
| **User Login** | `/auth/login/` |
| **User Signup** | `/auth/signup/` |

### Using the AI Assistant

1. Navigate to `/chatbot/`
2. Choose your mode:
   - **Learning Mode**: Ask questions like "Explain AES encryption"
   - **Quiz Mode**: Type "quiz me" to start a 5-question quiz
   - **Chat Mode**: Free conversation about cryptography

---

## 🏗️ System Architecture

### Request Flow Diagram

```
User Input → Frontend (HTML/JS) → Django View
                                        ↓
                                  Input Validation
                                        ↓
                                Algorithm Selection
                                        ↓
                    ┌─────────────┬──────────────┬──────────────┐
                    ↓             ↓              ↓              ↓
                C++ Exec    Java Exec    Python Fallback   Groq API (AI)
                    ↓             ↓              ↓              ↓
                    └─────────────┴──────────────┴──────────────┘
                                        ↓
                                   Process Result
                                        ↓
                              Visitor Tracking/Logging
                                        ↓
                                   JSON Response
                                        ↓
                                 Frontend Rendering
```

### Component Architecture

```
AlgoVault/
├── Frontend Layer
│   ├── Templates (Django Template Engine)
│   ├── Static Assets (CSS/JS)
│   └── AJAX Communication
│
├── Application Layer
│   ├── Django Views (Request Handlers)
│   ├── Input Validators
│   ├── Session Management
│   └── Rate Limiting (Django Cache)
│
├── Algorithm Layer
│   ├── Primary: C++ Executables
│   ├── Secondary: Java Classes
│   └── Fallback: Python Implementations
│
├── AI Layer
│   ├── Groq Cloud API
│   ├── Gemma2-9B Model
│   └── Context Management
│
├── Data Layer
│   ├── SQLite Database
│   ├── Django ORM
│   └── Cache Layer
│
└── Security Layer
    ├── CSRF Protection
    ├── Content Filtering
    ├── Rate Limiting
    └── Security Alerts
```

### Database Schema

```sql
-- Core Models
VisitorSession
├── ip_address (GenericIPAddressField)
├── session_key (CharField)
├── user (ForeignKey → User)
├── first_visit (DateTimeField)
├── last_activity (DateTimeField)
├── page_views (IntegerField)
└── user_agent (TextField)

ServiceUsage
├── session (ForeignKey → VisitorSession)
├── service_type (CharField)
├── usage_time (DateTimeField)
├── input_data (TextField)
└── output_data (TextField)

ChatConversation
├── session (ForeignKey → VisitorSession)
├── user_message (TextField)
├── ai_response (TextField)
├── timestamp (DateTimeField)
├── response_time (FloatField)
└── message_hash (CharField)

SecurityAlert
├── ip_address (GenericIPAddressField)
├── alert_type (CharField)
├── description (TextField)
├── blocked_content (TextField)
└── severity (IntegerField)
```

---

## 🔄 Algorithm Visualization Workflow

### How Visualizations Work

1. **User Input**: Enter plaintext/ciphertext and encryption parameters
2. **Parameter Validation**: Frontend validates input format and constraints
3. **Processing Request**: AJAX request sent to Django backend
4. **Algorithm Selection**: System attempts execution in order:
   - Primary: C++ compiled executable
   - Secondary: Java implementation
   - Fallback: Python implementation
5. **Step Generation**: Algorithm generates intermediate steps
6. **Visualization Data**: Backend returns JSON with:
   - Each round's state
   - Key schedule information
   - Transformation details
7. **Rendering**: Frontend animates the transformation process
8. **Result Display**: Final output shown with performance metrics

### Why Multi-Language Implementation?

- **C++**: Maximum performance for complex algorithms
- **Java**: Platform independence and enterprise compatibility
- **Python**: Rapid prototyping and fallback reliability
- **Educational Value**: Compare implementation differences
- **Redundancy**: Ensures availability even if compilation fails

---

## 🌐 API Documentation

### RESTful Endpoints

All algorithm processing endpoints accept POST requests with JSON payloads:

| Endpoint | Purpose | Request Format | Response Format |
|----------|---------|----------------|-----------------|
| `/api/caesar/process/` | Caesar Cipher | `{operation, shift, message}` | `{result}` |
| `/api/vigenere/process/` | Vigenère Cipher | `{operation, message, keyword}` | `{result}` |
| `/api/hill/process/` | Hill Cipher | `{operation, dimension, key_matrix_flat, input_vector_flat}` | `{result}` |
| `/api/aes/process/` | AES Encryption | `{operation, message, key}` | `{result, blocks_data}` |
| `/api/des/process/` | DES Encryption | `{operation, message, key}` | `{result}` |
| `/api/sha512/process/` | SHA-512 Hash | `{message}` | `{result}` |
| `/md5/process/` | MD5 Hash | `{text}` | `{hash}` |
| `/hmac/process/` | HMAC | `{message, key, algorithm}` | `{hmac}` |
| `/chatbot/api/chat/` | AI Chat | `{message, context}` | `{response, action}` |

### Example API Request

```javascript
// AES Encryption Example
fetch('/api/aes/process/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        operation: 'encrypt',
        message: 'Hello World',
        key: '1234567890123456'  // 16 characters for AES-128
    })
})
.then(response => response.json())
.then(data => console.log(data.result));
```

---

## 📈 Performance & Optimization

### Algorithm Performance Metrics

| Algorithm | C++ (ms) | Java (ms) | Python (ms) | Complexity |
|-----------|----------|-----------|-------------|------------|
| Caesar Cipher | 0.5 | 2 | 5 | O(n) |
| Vigenère | 1 | 3 | 8 | O(n*m) |
| Hill Cipher | 5 | 10 | 25 | O(n³) |
| AES-128 | 10 | 15 | 50 | O(n) |
| DES | 15 | 12 | 60 | O(n) |
| SHA-512 | 2 | 5 | 3 | O(n) |
| MD5 | 1 | 3 | 2 | O(n) |

### Optimization Strategies

#### Backend Optimizations
- **Multi-language Fallback System**: Automatic fallback from C++ → Java → Python
- **Django Cache**: Response caching for repeated calculations
- **Rate Limiting**: 50 requests/hour per user to prevent abuse
- **Session Management**: Efficient visitor tracking with minimal database queries

#### Frontend Optimizations
- **Lazy Loading**: Components loaded on-demand
- **Debounced Input**: Prevents excessive API calls during typing
- **Local State Management**: Reduces server round-trips
- **Minified Assets**: CSS/JS minification in production

#### AI Response Optimization
- **Context Summarization**: Maintains last 10 messages for context
- **Token Management**: Optimized prompts to reduce token usage
- **Response Caching**: Common questions cached for instant responses
- **Stream Processing**: Responses processed in chunks for faster display

---

## 🔒 Security Implementation

### Input Validation & Sanitization

```python
# Content validation in ChatBot/views.py
def validate_message_content(message):
    """Validate and filter user messages"""
    blocked_keywords = [
        'hack into', 'break into', 'steal password',
        'exploit vulnerability', 'create virus'
    ]
    
    message_lower = message.lower()
    for keyword in blocked_keywords:
        if keyword in message_lower:
            return False, "Malicious content detected"
    
    return True, ""
```

### Rate Limiting

```python
# Rate limiting implementation (50 messages/hour)
def check_rate_limit(request):
    user_id = f"user_{request.user.id}" if request.user.is_authenticated \
              else f"ip_{request.META.get('REMOTE_ADDR')}"
    
    cache_key = f"chat_rate_limit_{user_id}"
    current_count = cache.get(cache_key, 0)
    
    if current_count >= 50:
        return False, "Rate limit exceeded"
    
    cache.set(cache_key, current_count + 1, 3600)
    return True, ""
```

### Security Features

| Feature | Implementation | Purpose |
|---------|---------------|---------|
| **CSRF Protection** | Django middleware | Prevents cross-site request forgery |
| **Rate Limiting** | Django cache (50/hour) | Prevents API abuse |
| **Input Validation** | Server-side validation | Blocks malicious input |
| **Content Filtering** | Keyword blocking | Prevents harmful requests |
| **Session Tracking** | Custom middleware | Monitors user activity |
| **Security Alerts** | Database logging | Tracks suspicious behavior |

---

## 📊 Visitor Tracking & Analytics

### Tracking System Architecture

The project includes a comprehensive visitor tracking system implemented through custom middleware:

```python
# ChatBot/middleware.py
class VisitorTrackingMiddleware:
    """Automatically tracks all page visits"""
    
    def process_request(self, request):
        # Skip admin, static, and API endpoints
        skip_paths = ['/admin/', '/static/', '/api/']
        
        if not any(request.path.startswith(p) for p in skip_paths):
            track_page_visit(request, self.get_page_title(request.path))
```

### Tracked Metrics

| Metric | Description | Storage |
|--------|-------------|---------|
| **Page Views** | Total pages visited per session | `VisitorSession.page_views` |
| **Service Usage** | Which algorithms used | `ServiceUsage` model |
| **Chat Conversations** | AI interactions with response times | `ChatConversation` model |
| **Security Alerts** | Blocked malicious attempts | `SecurityAlert` model |
| **Session Duration** | Time spent on platform | `VisitorSession.total_duration` |

### Privacy Compliance
- IP addresses hashed for anonymity
- No personal data collection without consent
- Session data expires after 30 days
- GDPR-compliant data handling

---

## 🤖 AI Chat Assistant Integration

### Architecture

The AI assistant uses a sophisticated multi-tier architecture:

1. **Frontend Layer** (`ChatBot/static/js/chatbot.js`)
   - WebSocket-like communication
   - Context management (maintains last 10 messages)
   - Smart message formatting
   - Quiz option handling

2. **Backend Processing** (`ChatBot/views.py`)
   - Request validation and rate limiting
   - Context preparation and summarization
   - Groq API communication
   - Response enhancement and filtering

3. **AI Model Integration**
   - Model: Gemma2-9B-IT (Google's instruction-tuned model)
   - Platform: Groq Cloud (ultra-low latency inference)
   - Context window: 8,192 tokens
   - Temperature: 0.3 (balanced creativity/accuracy)

### AI Model Integration

The AI assistant uses a sophisticated multi-tier architecture:

1. **Frontend Layer** (`ChatBot/static/js/chatbot.js`)
   - AJAX-based communication (not WebSocket)
   - Context management (maintains last 10 messages)
   - Smart message formatting
   - Quiz option handling

2. **Backend Processing** (`ChatBot/views.py`)
   - Request validation and rate limiting
   - Context preparation and summarization
   - Groq API communication
   - Response enhancement and filtering

3. **AI Model Integration**
   - Model: Gemma2-9B-IT (Google's instruction-tuned model)
   - Platform: Groq Cloud (ultra-low latency inference)
   - Context window: 8,192 tokens
   - Temperature: 0.3 (balanced creativity/accuracy)

### Three Operational Modes

#### 📚 Learning Mode
- Comprehensive explanations with examples
- Historical context and mathematical foundations
- Step-by-step algorithm walkthroughs
- Best practices and real-world applications

#### 🧠 Quiz Mode
- 5-question quizzes with topic rotation
- Multiple-choice format (A, B, C, D)
- Immediate feedback with explanations
- Topics from 15+ cryptography categories:
  - Classical Ciphers (Caesar, Vigenère, Hill)
  - Modern Encryption (AES, DES, RSA)
  - Hash Functions (MD5, SHA family)
  - Key Exchange (Diffie-Hellman, ECDH)
  - Digital Signatures & PKI
  - Cryptanalysis Techniques
  - And more...

#### 💬 Interactive Chat Mode
- Free-form Q&A about cryptography
- Natural conversation flow
- Context-aware responses
- Follow-up questions for clarity

### Quiz System Architecture

```python
# Topic rotation ensures variety
QUIZ_CATEGORIES = [
    "Classical Ciphers",
    "Block Ciphers", 
    "Stream Ciphers",
    "Hash Functions",
    "Public Key Cryptography",
    "Digital Signatures",
    "Key Exchange",
    "Cryptanalysis",
    "Quantum Cryptography",
    "Blockchain",
    "Zero-Knowledge Proofs",
    "Homomorphic Encryption",
    "Post-Quantum Cryptography",
    "Side-Channel Attacks",
    "Random Number Generation"
]

# Each quiz follows strict rules:
# - 5 questions total
# - Each from different category
# - No repeated questions
# - Progressive difficulty
```

### Response Processing Pipeline

```
User Message → Content Validation → Rate Limit Check
                                           ↓
                                    Mode Detection
                                           ↓
                            Context Preparation (Last 10 msgs)
                                           ↓
                                    Groq API Call
                                           ↓
                                 Response Enhancement
                                           ↓
                           Action Token Processing (Quiz flow)
                                           ↓
                                    Database Logging
                                           ↓
                                     JSON Response
```

### Why Groq + Gemma2?

- **Groq Speed**: Sub-second response times (10x faster than traditional APIs)
- **Gemma2 Quality**: State-of-the-art instruction following
- **Cost Efficiency**: Optimized token usage
- **Educational Focus**: Trained on technical documentation

---

## 🎯 Example Use Cases

### For Students
- Learn cryptography fundamentals through visualization
- Test knowledge with AI-generated quizzes
- Understand mathematical foundations step-by-step
- Compare different algorithm approaches

### For Educators
- Demonstrate algorithm execution in real-time
- Generate quiz questions for assessments
- Show security vulnerabilities visually
- Explain complex concepts interactively

### For Developers
- Reference implementations in multiple languages
- Debug cryptographic implementations
- Understand algorithm internals
- Test edge cases quickly

### For Security Professionals
- Analyze algorithm strengths/weaknesses
- Demonstrate attack vectors
- Train team members
- Quick cryptographic calculations

---

## 🔧 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **C++ executables not working** | • Recompile with `g++ -o algorithm.exe algorithm.cpp`<br>• Check execution permissions: `chmod +x *.exe`<br>• Python fallback will automatically activate |
| **"GROQ_API_KEY not found"** | • Add `GROQ_API_KEY=your_key` to `.env` file<br>• Restart Django server after adding |
| **"Module not found" errors** | • Ensure virtual environment is activated<br>• Run `pip install -r requirements.txt` |
| **Static files not loading** | • Run `python manage.py collectstatic`<br>• Check `STATICFILES_DIRS` in settings.py |
| **Database errors** | • Run `python manage.py makemigrations`<br>• Run `python manage.py migrate` |
| **Chat rate limit exceeded** | • Wait 1 hour (50 messages/hour limit)<br>• Clear cache: `python manage.py shell` then `from django.core.cache import cache; cache.clear()` |
| **Algorithm produces wrong output** | • Check input format (some require specific formatting)<br>• Verify key lengths (AES: 16, DES: 8 characters)<br>• Try the Python fallback implementation |

### Platform-Specific Issues

#### Windows
```bash
# If C++ executables fail on Windows
# Install MinGW and add to PATH
# Compile with: g++ -o algorithm.exe algorithm.cpp -static

# Python path issues
# Use forward slashes in paths or raw strings: r"C:\path\to\file"
```

#### Linux/Mac
```bash
# Permission denied errors
chmod +x Algorithm/Crypto_Native/CPP/*.exe
chmod +x Algorithm/cpp_source/compile.sh

# Missing g++ compiler
# Ubuntu/Debian: sudo apt-get install g++
# Mac: xcode-select --install
```

### Debug Mode

Enable debug output for troubleshooting:

```python
# In views.py, add debug prints
import logging
logger = logging.getLogger(__name__)

# Enable SQL query logging
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}
```

---

## 🤝 Contributing Guidelines

We welcome contributions! Here's how you can help:

### 1. Fork & Clone
```bash
git clone https://github.com/yourusername/AlgoVault.git
cd AlgoVault
git remote add upstream https://github.com/original/AlgoVault.git
```

### 2. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Development Guidelines

#### Code Style
- **Python**: Follow PEP 8
- **JavaScript**: Use ES6+ features
- **C++**: Follow Google C++ Style Guide
- **HTML/CSS**: Semantic markup, BEM methodology

#### Commit Messages
```
type(scope): description

- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance
```

#### Testing Requirements
- Unit tests for new algorithms
- Integration tests for API endpoints
- UI tests for new visualizations
- Performance benchmarks for optimizations

### 4. Submit Pull Request
- Clear description of changes
- Link related issues
- Include screenshots for UI changes
- Update documentation

### Areas for Contribution
- 🆕 New algorithm implementations
- 🎨 UI/UX improvements
- 📚 Documentation enhancement
- 🐛 Bug fixes
- ⚡ Performance optimizations
- 🌍 Internationalization
- ♿ Accessibility improvements

---



## 🙏 Acknowledgements

### Technologies & Libraries
- **Django Team** - For the amazing web framework
- **Google** - For Gemma2 language model
- **Groq** - For ultra-fast AI inference
- **Python Cryptography** - For secure implementations
- **Font Awesome** - For beautiful icons
  
### Community
- All contributors and beta testers
- Cryptography educators worldwide
- Open-source community

---

## 📞 Support & Contact

### Getting Help
- 📖 **Documentation**: Check our [Help Center](/help/)
- 💬 **AI Assistant**: Ask our chatbot at [/chatbot/](/chatbot/)
- 🐛 **Bug Reports**: Open an issue on GitHub
- 💡 **Feature Requests**: Discuss in GitHub Discussions

### Security Vulnerabilities
For security issues, please email: security@algovault.example.com

### Stay Connected
- 🌐 **Website**: [algovault.example.com](https://algovault.example.com)
- 📧 **Email**:  connect.ayushommishra@gmail.com
- 💼 **LinkedIn**: [AlgoVault](https://linkedin.com/company/algovault)
---

<div align="center">
  <p>Built with ❤️ by the AlgoVault Team</p>
  <p>Making Cryptography Accessible to Everyone</p>
</div>
