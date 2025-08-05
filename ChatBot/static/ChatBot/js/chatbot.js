// Chatbot JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const chatMessages = document.getElementById('chatMessages');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const typingIndicator = document.getElementById('typingIndicator');
    const charCount = document.getElementById('charCount');
    const questionCards = document.querySelectorAll('.question-card');
    const welcomeTime = document.getElementById('welcomeTime');

    // Conversation history for context
    let conversationHistory = [];
    let conversationSummary = "";
    
    // Smart context management configuration
    const RECENT_MESSAGES_LIMIT = 20; // Keep last 20 messages as full context
    const SUMMARY_THRESHOLD = 30; // Start summarizing when we have more than 30 messages

    // Set welcome message time
    if (welcomeTime) {
        welcomeTime.textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    }

    // Auto-resize textarea
    function autoResizeTextarea() {
        messageInput.style.height = 'auto';
        messageInput.style.height = messageInput.scrollHeight + 'px';
    }

    // Update character count
    function updateCharCount() {
        const count = messageInput.value.length;
        charCount.textContent = count;
        
        if (count > 900) {
            charCount.style.color = '#ff4444';
        } else if (count > 800) {
            charCount.style.color = '#ff8800';
        } else {
            charCount.style.color = 'var(--text-muted)';
        }
    }

    // Scroll to bottom of chat
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Show typing indicator
    function showTyping() {
        typingIndicator.style.display = 'flex';
        scrollToBottom();
    }

    // Hide typing indicator
    function hideTyping() {
        typingIndicator.style.display = 'none';
    }

    // Add quiz option click handlers
    function addQuizOptionHandlers(messageElement) {
        const quizOptions = messageElement.querySelectorAll('.quiz-option-item');
        quizOptions.forEach(option => {
            option.addEventListener('click', async function() {
                const optionText = this.getAttribute('data-option');
                
                // Visual feedback
                this.style.background = 'rgba(255, 0, 0, 0.1)';
                this.style.borderColor = 'var(--primary-color)';
                
                // Disable all quiz options to prevent multiple clicks
                quizOptions.forEach(opt => {
                    opt.style.pointerEvents = 'none';
                    opt.style.opacity = '0.6';
                });
                
                // Directly submit the selected option
                if (!messageInput.disabled && !sendButton.disabled) {
                    // Set the message and submit directly
                    messageInput.value = optionText;
                    await handleSubmit();
                }
                
                // Re-enable quiz options after a delay
                setTimeout(() => {
                    quizOptions.forEach(opt => {
                        opt.style.pointerEvents = '';
                        opt.style.opacity = '';
                    });
                    this.style.background = '';
                    this.style.borderColor = '';
                }, 1000);
            });
        });
    }

    // Add mode selection handlers
    function addModeSelectionHandlers(messageElement) {
        const modeOptions = messageElement.querySelectorAll('.mode-option');
        modeOptions.forEach(option => {
            option.addEventListener('click', async function() {
                const mode = this.getAttribute('data-mode');
                
                // Visual feedback
                this.style.background = 'rgba(255, 0, 0, 0.1)';
                this.style.borderColor = 'var(--primary-color)';
                
                // Disable to prevent multiple clicks
                modeOptions.forEach(opt => {
                    opt.style.pointerEvents = 'none';
                    opt.style.opacity = '0.6';
                });
                
                // Set appropriate message for each mode
                if (mode === 'learning') {
                    // Show topic selection for learning
                    showTopicSelection('learning');
                } else if (mode === 'quiz') {
                    // Show topic selection for quiz
                    showTopicSelection('quiz');
                } else if (mode === 'chat') {
                    // Show free chat welcome message
                    showFreeChatWelcome();
                }
                
                // Reset visual feedback after a delay
                setTimeout(() => {
                    modeOptions.forEach(opt => {
                        opt.style.pointerEvents = '';
                        opt.style.opacity = '';
                    });
                    this.style.background = '';
                    this.style.borderColor = '';
                }, 1000);
            });
        });
    }

    // Show free chat welcome message
    function showFreeChatWelcome() {
        // Create interactive chat welcome message
        let chatHtml = `
            <div class="interactive-chat-welcome">
                <h3 style="margin-bottom: 20px; color: var(--primary-color); text-align: center; font-weight: 600; font-size: 1.2rem;">
                    <i class="fas fa-comments" style="margin-right: 10px;"></i>
                    Interactive Chat Mode
                </h3>
                <div style="background: var(--secondary-color); border-radius: 15px; padding: 20px; margin-bottom: 20px; border: 1px solid rgba(255, 0, 0, 0.1);">
                    <p style="margin: 0 0 15px 0; color: var(--text-color); line-height: 1.6; font-size: 1rem;">
                         <strong>You're now in Interactive Chat mode!</strong> Ask me anything about cryptography - no structured topics needed.
                    </p>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-top: 15px;">
                        <div style="background: var(--card-bg); padding: 12px; border-radius: 10px; border: 1px solid rgba(255, 0, 0, 0.1);">
                            <strong style="color: var(--primary-color);">💡 Example Questions:</strong>
                            <ul style="margin: 8px 0 0 0; font-size: 0.9rem; color: var(--text-muted);">
                                <li>How secure is RSA-2048?</li>
                                <li>What are timing attacks?</li>
                                <li>Best practices for password hashing?</li>
                            </ul>
                        </div>
                        <div style="background: var(--card-bg); padding: 12px; border-radius: 10px; border: 1px solid rgba(255, 0, 0, 0.1);">
                            <strong style="color: var(--primary-color);">🔍 Deep Dives:</strong>
                            <ul style="margin: 8px 0 0 0; font-size: 0.9rem; color: var(--text-muted);">
                                <li>Compare algorithms</li>
                                <li>Implementation details</li>
                                <li>Real-world vulnerabilities</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <p style="text-align: center; font-size: 0.95rem; color: var(--text-muted); font-style: italic; margin: 15px 0;">
                    ✨ Go ahead, type your question below and let's explore cryptography together!
                </p>
                <div style="text-align: center; margin-top: 20px;">
                    <button class="back-to-modes-btn" style="
                        background: var(--secondary-color);
                        color: var(--text-color);
                        border: 1px solid rgba(255, 0, 0, 0.2);
                        padding: 10px 20px;
                        border-radius: 25px;
                        cursor: pointer;
                        font-size: 0.9rem;
                        transition: all 0.3s ease;
                    ">← Back to Mode Selection</button>
                </div>
            </div>
        `;
        
        // Add the free chat welcome message to chat
        const chatMessage = createMessageElement('', false);
        chatMessage.querySelector('.message-bubble').innerHTML = chatHtml;
        chatMessages.appendChild(chatMessage);
        
        // Add handler for back button
        addFreeChatHandlers(chatMessage);
        
        scrollToBottom();
    }

    // Add free chat handlers
    function addFreeChatHandlers(messageElement) {
        const backButton = messageElement.querySelector('.back-to-modes-btn');
        
        if (backButton) {
            backButton.addEventListener('click', function() {
                // Visual feedback
                this.style.background = 'var(--primary-color)';
                this.style.color = 'white';
                this.textContent = 'Loading...';
                
                // Reload the page to show mode selection again
                setTimeout(() => {
                    location.reload();
                }, 300);
            });
            
            // Add hover effect for back button
            backButton.addEventListener('mouseenter', function() {
                this.style.background = 'var(--primary-color)';
                this.style.color = 'white';
                this.style.transform = 'translateX(-2px)';
            });
            
            backButton.addEventListener('mouseleave', function() {
                this.style.background = 'var(--secondary-color)';
                this.style.color = 'var(--text-color)';
                this.style.transform = 'translateX(0)';
            });
        }
    }

    // Show topic selection interface
    function showTopicSelection(mode) {
        const topics = {
            learning: [
                { 
                    id: 'overview', 
                    title: 'Cryptography Overview', 
                    description: 'History, fundamentals, and main types',
                    subtopics: [
                        { id: 'history', title: 'History of Cryptography', description: 'Ancient ciphers to modern cryptography' },
                        { id: 'fundamentals', title: 'Fundamental Concepts', description: 'Basic principles and terminology' },
                        { id: 'types', title: 'Types of Cryptography', description: 'Overview of symmetric, asymmetric, and hashing' },
                        { id: 'applications', title: 'Real-world Applications', description: 'How cryptography is used today' }
                    ]
                },
                { 
                    id: 'symmetric', 
                    title: 'Symmetric Encryption', 
                    description: 'AES, DES, block/stream ciphers',
                    subtopics: [
                        { id: 'aes', title: 'AES (Advanced Encryption Standard)', description: 'Modern symmetric encryption standard' },
                        { id: 'des', title: 'DES (Data Encryption Standard)', description: 'Legacy symmetric encryption algorithm' },
                        { id: 'block-ciphers', title: 'Block Ciphers', description: 'Fixed-size block encryption methods' },
                        { id: 'stream-ciphers', title: 'Stream Ciphers', description: 'Bit-by-bit encryption methods' },
                        { id: 'cipher-modes', title: 'Cipher Modes', description: 'ECB, CBC, CTR, GCM modes' }
                    ]
                },
                { 
                    id: 'asymmetric', 
                    title: 'Asymmetric Encryption', 
                    description: 'RSA, ECC, public-key cryptography',
                    subtopics: [
                        { id: 'rsa', title: 'RSA Algorithm', description: 'Public-key cryptosystem based on factoring' },
                        { id: 'ecc', title: 'Elliptic Curve Cryptography', description: 'Modern public-key based on elliptic curves' },
                        { id: 'key-exchange', title: 'Key Exchange Protocols', description: 'Diffie-Hellman and variants' },
                        { id: 'digital-signatures', title: 'Digital Signatures', description: 'Authentication and non-repudiation' },
                        { id: 'pki-concepts', title: 'Public Key Infrastructure', description: 'Certificate authorities and trust models' }
                    ]
                },
                { 
                    id: 'hashing', 
                    title: 'Hash Functions', 
                    description: 'SHA, MD5, digital signatures',
                    subtopics: [
                        { id: 'sha', title: 'SHA Family', description: 'SHA-1, SHA-256, SHA-512 algorithms' },
                        { id: 'md5', title: 'MD5 Algorithm', description: 'Legacy hash function and vulnerabilities' },
                        { id: 'hash-properties', title: 'Hash Function Properties', description: 'Collision resistance, avalanche effect' },
                        { id: 'hmac', title: 'HMAC', description: 'Hash-based message authentication codes' },
                        { id: 'applications', title: 'Hash Applications', description: 'Password storage, integrity checking' }
                    ]
                },
                { 
                    id: 'protocols', 
                    title: 'Cryptographic Protocols', 
                    description: 'TLS, PKI, certificates',
                    subtopics: [
                        { id: 'tls-ssl', title: 'TLS/SSL Protocols', description: 'Secure communication protocols' },
                        { id: 'pki', title: 'Public Key Infrastructure', description: 'Certificate management systems' },
                        { id: 'certificates', title: 'Digital Certificates', description: 'X.509 certificates and validation' },
                        { id: 'authentication', title: 'Authentication Protocols', description: 'OAuth, SAML, Kerberos' },
                        { id: 'secure-messaging', title: 'Secure Messaging', description: 'Signal, WhatsApp encryption' }
                    ]
                },
                { 
                    id: 'advanced', 
                    title: 'Advanced Topics', 
                    description: 'Quantum, post-quantum, blockchain',
                    subtopics: [
                        { id: 'quantum', title: 'Quantum Cryptography', description: 'Quantum key distribution and protocols' },
                        { id: 'post-quantum', title: 'Post-Quantum Cryptography', description: 'Quantum-resistant algorithms' },
                        { id: 'blockchain', title: 'Blockchain Cryptography', description: 'Hash chains, Merkle trees, consensus' },
                        { id: 'zero-knowledge', title: 'Zero-Knowledge Proofs', description: 'Privacy-preserving verification' },
                        { id: 'homomorphic', title: 'Homomorphic Encryption', description: 'Computing on encrypted data' }
                    ]
                }
            ],
            quiz: [
                { 
                    id: 'mixed', 
                    title: 'Mixed Topics Quiz', 
                    description: '5 questions across all categories',
                    subtopics: [
                        { id: 'general', title: 'General Mixed Quiz', description: 'Random questions from all topics' },
                        { id: 'beginner', title: 'Beginner Level', description: 'Basic concepts across all areas' },
                        { id: 'intermediate', title: 'Intermediate Level', description: 'Moderate difficulty mixed questions' },
                        { id: 'advanced', title: 'Advanced Level', description: 'Challenging questions across topics' }
                    ]
                },
                { 
                    id: 'symmetric', 
                    title: 'Symmetric Encryption Quiz', 
                    description: 'AES, DES, block ciphers',
                    subtopics: [
                        { id: 'aes-quiz', title: 'AES Quiz', description: 'Questions about AES algorithm' },
                        { id: 'des-quiz', title: 'DES Quiz', description: 'Questions about DES algorithm' },
                        { id: 'block-ciphers-quiz', title: 'Block Ciphers Quiz', description: 'Block cipher concepts and modes' },
                        { id: 'stream-ciphers-quiz', title: 'Stream Ciphers Quiz', description: 'Stream cipher principles' }
                    ]
                },
                { 
                    id: 'asymmetric', 
                    title: 'Asymmetric Encryption Quiz', 
                    description: 'RSA, ECC, key exchange',
                    subtopics: [
                        { id: 'rsa-quiz', title: 'RSA Quiz', description: 'RSA algorithm and applications' },
                        { id: 'ecc-quiz', title: 'ECC Quiz', description: 'Elliptic curve cryptography' },
                        { id: 'key-exchange-quiz', title: 'Key Exchange Quiz', description: 'Diffie-Hellman and protocols' },
                        { id: 'signatures-quiz', title: 'Digital Signatures Quiz', description: 'Signature schemes and verification' }
                    ]
                },
                { 
                    id: 'hashing', 
                    title: 'Hash Functions Quiz', 
                    description: 'SHA, MD5, digital signatures',
                    subtopics: [
                        { id: 'sha-quiz', title: 'SHA Quiz', description: 'SHA family algorithms' },
                        { id: 'md5-quiz', title: 'MD5 Quiz', description: 'MD5 and its vulnerabilities' },
                        { id: 'hash-properties-quiz', title: 'Hash Properties Quiz', description: 'Hash function characteristics' },
                        { id: 'hmac-quiz', title: 'HMAC Quiz', description: 'Message authentication codes' }
                    ]
                },
                { 
                    id: 'protocols', 
                    title: 'Protocols Quiz', 
                    description: 'TLS, PKI, security protocols',
                    subtopics: [
                        { id: 'tls-quiz', title: 'TLS/SSL Quiz', description: 'Transport layer security' },
                        { id: 'pki-quiz', title: 'PKI Quiz', description: 'Public key infrastructure' },
                        { id: 'certificates-quiz', title: 'Certificates Quiz', description: 'Digital certificates and validation' },
                        { id: 'auth-quiz', title: 'Authentication Quiz', description: 'Authentication protocols' }
                    ]
                },
                { 
                    id: 'advanced', 
                    title: 'Advanced Topics Quiz', 
                    description: 'Quantum, modern cryptography',
                    subtopics: [
                        { id: 'quantum-quiz', title: 'Quantum Cryptography Quiz', description: 'Quantum concepts and protocols' },
                        { id: 'post-quantum-quiz', title: 'Post-Quantum Quiz', description: 'Quantum-resistant cryptography' },
                        { id: 'blockchain-quiz', title: 'Blockchain Quiz', description: 'Blockchain cryptographic concepts' },
                        { id: 'modern-quiz', title: 'Modern Crypto Quiz', description: 'Latest cryptographic developments' }
                    ]
                }
            ]
        };

        const topicOptions = topics[mode];
        const modeTitle = mode === 'learning' ? 'Learning Mode' : 'Quiz Mode';
        
        // Create topic selection message
        let topicHtml = `
            <div class="topic-selection">
                <h3 style="margin-bottom: 20px; color: var(--primary-color); text-align: center; font-weight: 600; font-size: 1.2rem;">${modeTitle} - Choose a Topic</h3>
                <div class="topic-grid">
        `;
        
        topicOptions.forEach(topic => {
            topicHtml += `
                <div class="topic-option" data-mode="${mode}" data-topic="${topic.id}" style="
                    border: 2px solid rgba(255, 0, 0, 0.2);
                    border-radius: 12px;
                    padding: 16px;
                    margin: 10px 0;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    background: var(--card-bg);
                    box-shadow: var(--shadow);
                    backdrop-filter: blur(10px);
                ">
                    <div class="topic-title" style="font-weight: 600; color: var(--text-color); margin-bottom: 6px; font-size: 1rem;">${topic.title}</div>
                    <div class="topic-description" style="font-size: 0.875rem; color: var(--text-muted); line-height: 1.4;">${topic.description}</div>
                </div>
            `;
        });
        
        topicHtml += `
                </div>
                <p style="margin-top: 20px; font-size: 0.875rem; color: var(--text-muted); text-align: center; font-style: italic;">
                    💡 Or type your own specific question about any cryptography topic!
                </p>
            </div>
        `;
        
        // Add the topic selection message to chat
        const topicMessage = createMessageElement('', false);
        topicMessage.querySelector('.message-bubble').innerHTML = topicHtml;
        chatMessages.appendChild(topicMessage);
        
        // Add handlers for topic selection
        addTopicSelectionHandlers(topicMessage);
        
        scrollToBottom();
    }

    // Show subtopic selection interface
    function showSubtopicSelection(mode, mainTopic) {
        const topics = getTopicsData();
        const selectedTopic = topics[mode].find(topic => topic.id === mainTopic);
        
        if (!selectedTopic || !selectedTopic.subtopics) {
            // Fallback to direct message if no subtopics
            handleDirectTopicSelection(mode, mainTopic);
            return;
        }

        const modeTitle = mode === 'learning' ? 'Learning Mode' : 'Quiz Mode';
        
        // Create subtopic selection message
        let subtopicHtml = `
            <div class="subtopic-selection">
                <h3 style="margin-bottom: 15px; color: var(--primary-color); text-align: center; font-weight: 600; font-size: 1.1rem;">${selectedTopic.title} - Choose a Subtopic</h3>
                <div class="subtopic-grid">
        `;
        
        selectedTopic.subtopics.forEach(subtopic => {
            subtopicHtml += `
                <div class="subtopic-option" data-mode="${mode}" data-main-topic="${mainTopic}" data-subtopic="${subtopic.id}" style="
                    border: 1.5px solid rgba(255, 0, 0, 0.15);
                    border-radius: 10px;
                    padding: 12px;
                    margin: 8px 0;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    background: var(--card-bg);
                    box-shadow: var(--shadow);
                    backdrop-filter: blur(10px);
                ">
                    <div class="subtopic-title" style="font-weight: 600; color: var(--text-color); margin-bottom: 4px; font-size: 0.95rem;">${subtopic.title}</div>
                    <div class="subtopic-description" style="font-size: 0.8rem; color: var(--text-muted); line-height: 1.3;">${subtopic.description}</div>
                </div>
            `;
        });
        
        subtopicHtml += `
                </div>
                <div style="margin-top: 15px; text-align: center;">
                    <button class="back-to-topics-btn" data-mode="${mode}" style="
                        background: var(--secondary-color);
                        color: var(--text-color);
                        border: 1px solid rgba(255, 0, 0, 0.2);
                        padding: 8px 16px;
                        border-radius: 20px;
                        cursor: pointer;
                        font-size: 0.85rem;
                        transition: all 0.3s ease;
                        margin-right: 10px;
                    ">← Back to Categories</button>
                    <span style="font-size: 0.8rem; color: var(--text-muted); font-style: italic;">
                        💡 Or type your own specific question!
                    </span>
                </div>
            </div>
        `;
        
        // Add the subtopic selection message to chat
        const subtopicMessage = createMessageElement('', false);
        subtopicMessage.querySelector('.message-bubble').innerHTML = subtopicHtml;
        chatMessages.appendChild(subtopicMessage);
        
        // Add handlers for subtopic selection
        addSubtopicSelectionHandlers(subtopicMessage);
        
        scrollToBottom();
    }

    // Add subtopic selection handlers
    function addSubtopicSelectionHandlers(messageElement) {
        const subtopicOptions = messageElement.querySelectorAll('.subtopic-option');
        const backButton = messageElement.querySelector('.back-to-topics-btn');
        
        // Add hover effects for subtopics
        subtopicOptions.forEach(option => {
            option.addEventListener('mouseenter', function() {
                this.style.borderColor = 'var(--primary-color)';
                this.style.background = 'var(--secondary-color)';
                this.style.transform = 'translateY(-1px)';
                this.style.boxShadow = '0 4px 12px rgba(255, 0, 0, 0.15)';
            });
            
            option.addEventListener('mouseleave', function() {
                if (!this.classList.contains('selected')) {
                    this.style.borderColor = 'rgba(255, 0, 0, 0.15)';
                    this.style.background = 'var(--card-bg)';
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = 'var(--shadow)';
                }
            });
        });
        
        // Handle subtopic selection
        subtopicOptions.forEach(option => {
            option.addEventListener('click', async function() {
                const mode = this.getAttribute('data-mode');
                const mainTopic = this.getAttribute('data-main-topic');
                const subtopicId = this.getAttribute('data-subtopic');
                
                // Visual feedback
                this.style.background = 'var(--secondary-color)';
                this.style.borderColor = 'var(--primary-color)';
                this.style.boxShadow = '0 4px 16px rgba(255, 0, 0, 0.25)';
                this.style.transform = 'scale(0.98)';
                this.classList.add('selected');
                
                // Disable all subtopic options
                subtopicOptions.forEach(opt => {
                    opt.style.pointerEvents = 'none';
                    if (opt !== this) {
                        opt.style.opacity = '0.5';
                        opt.style.transform = 'scale(0.95)';
                    }
                });
                
                // Generate detailed message based on subtopic
                const message = generateSubtopicMessage(mode, mainTopic, subtopicId);
                
                // Set message and submit
                messageInput.value = message;
                updateCharCount();
                autoResizeTextarea();
                
                await handleSubmit();
            });
        });
        
        // Handle back button
        if (backButton) {
            backButton.addEventListener('click', function() {
                const mode = this.getAttribute('data-mode');
                
                // Visual feedback
                this.style.background = 'var(--primary-color)';
                this.style.color = 'white';
                
                // Show main topic selection again
                setTimeout(() => {
                    showTopicSelection(mode);
                }, 200);
            });
            
            // Add hover effect for back button
            backButton.addEventListener('mouseenter', function() {
                this.style.background = 'var(--primary-color)';
                this.style.color = 'white';
                this.style.transform = 'translateX(-2px)';
            });
            
            backButton.addEventListener('mouseleave', function() {
                this.style.background = 'var(--secondary-color)';
                this.style.color = 'var(--text-color)';
                this.style.transform = 'translateX(0)';
            });
        }
    }

    // Get topics data (extracted for reusability)
    function getTopicsData() {
        return {
            learning: [
                { 
                    id: 'overview', 
                    title: 'Cryptography Overview', 
                    description: 'History, fundamentals, and main types',
                    subtopics: [
                        { id: 'history', title: 'History of Cryptography', description: 'Ancient ciphers to modern cryptography' },
                        { id: 'fundamentals', title: 'Fundamental Concepts', description: 'Basic principles and terminology' },
                        { id: 'types', title: 'Types of Cryptography', description: 'Overview of symmetric, asymmetric, and hashing' },
                        { id: 'applications', title: 'Real-world Applications', description: 'How cryptography is used today' }
                    ]
                },
                { 
                    id: 'symmetric', 
                    title: 'Symmetric Encryption', 
                    description: 'AES, DES, block/stream ciphers',
                    subtopics: [
                        { id: 'aes', title: 'AES (Advanced Encryption Standard)', description: 'Modern symmetric encryption standard' },
                        { id: 'des', title: 'DES (Data Encryption Standard)', description: 'Legacy symmetric encryption algorithm' },
                        { id: 'block-ciphers', title: 'Block Ciphers', description: 'Fixed-size block encryption methods' },
                        { id: 'stream-ciphers', title: 'Stream Ciphers', description: 'Bit-by-bit encryption methods' },
                        { id: 'cipher-modes', title: 'Cipher Modes', description: 'ECB, CBC, CTR, GCM modes' }
                    ]
                },
                { 
                    id: 'asymmetric', 
                    title: 'Asymmetric Encryption', 
                    description: 'RSA, ECC, public-key cryptography',
                    subtopics: [
                        { id: 'rsa', title: 'RSA Algorithm', description: 'Public-key cryptosystem based on factoring' },
                        { id: 'ecc', title: 'Elliptic Curve Cryptography', description: 'Modern public-key based on elliptic curves' },
                        { id: 'key-exchange', title: 'Key Exchange Protocols', description: 'Diffie-Hellman and variants' },
                        { id: 'digital-signatures', title: 'Digital Signatures', description: 'Authentication and non-repudiation' },
                        { id: 'pki-concepts', title: 'Public Key Infrastructure', description: 'Certificate authorities and trust models' }
                    ]
                },
                { 
                    id: 'hashing', 
                    title: 'Hash Functions', 
                    description: 'SHA, MD5, digital signatures',
                    subtopics: [
                        { id: 'sha', title: 'SHA Family', description: 'SHA-1, SHA-256, SHA-512 algorithms' },
                        { id: 'md5', title: 'MD5 Algorithm', description: 'Legacy hash function and vulnerabilities' },
                        { id: 'hash-properties', title: 'Hash Function Properties', description: 'Collision resistance, avalanche effect' },
                        { id: 'hmac', title: 'HMAC', description: 'Hash-based message authentication codes' },
                        { id: 'applications', title: 'Hash Applications', description: 'Password storage, integrity checking' }
                    ]
                },
                { 
                    id: 'protocols', 
                    title: 'Cryptographic Protocols', 
                    description: 'TLS, PKI, certificates',
                    subtopics: [
                        { id: 'tls-ssl', title: 'TLS/SSL Protocols', description: 'Secure communication protocols' },
                        { id: 'pki', title: 'Public Key Infrastructure', description: 'Certificate management systems' },
                        { id: 'certificates', title: 'Digital Certificates', description: 'X.509 certificates and validation' },
                        { id: 'authentication', title: 'Authentication Protocols', description: 'OAuth, SAML, Kerberos' },
                        { id: 'secure-messaging', title: 'Secure Messaging', description: 'Signal, WhatsApp encryption' }
                    ]
                },
                { 
                    id: 'advanced', 
                    title: 'Advanced Topics', 
                    description: 'Quantum, post-quantum, blockchain',
                    subtopics: [
                        { id: 'quantum', title: 'Quantum Cryptography', description: 'Quantum key distribution and protocols' },
                        { id: 'post-quantum', title: 'Post-Quantum Cryptography', description: 'Quantum-resistant algorithms' },
                        { id: 'blockchain', title: 'Blockchain Cryptography', description: 'Hash chains, Merkle trees, consensus' },
                        { id: 'zero-knowledge', title: 'Zero-Knowledge Proofs', description: 'Privacy-preserving verification' },
                        { id: 'homomorphic', title: 'Homomorphic Encryption', description: 'Computing on encrypted data' }
                    ]
                }
            ],
            quiz: [
                { 
                    id: 'mixed', 
                    title: 'Mixed Topics Quiz', 
                    description: '5 questions across all categories',
                    subtopics: [
                        { id: 'general', title: 'General Mixed Quiz', description: 'Random questions from all topics' },
                        { id: 'beginner', title: 'Beginner Level', description: 'Basic concepts across all areas' },
                        { id: 'intermediate', title: 'Intermediate Level', description: 'Moderate difficulty mixed questions' },
                        { id: 'advanced', title: 'Advanced Level', description: 'Challenging questions across topics' }
                    ]
                },
                { 
                    id: 'symmetric', 
                    title: 'Symmetric Encryption Quiz', 
                    description: 'AES, DES, block ciphers',
                    subtopics: [
                        { id: 'aes-quiz', title: 'AES Quiz', description: 'Questions about AES algorithm' },
                        { id: 'des-quiz', title: 'DES Quiz', description: 'Questions about DES algorithm' },
                        { id: 'block-ciphers-quiz', title: 'Block Ciphers Quiz', description: 'Block cipher concepts and modes' },
                        { id: 'stream-ciphers-quiz', title: 'Stream Ciphers Quiz', description: 'Stream cipher principles' }
                    ]
                },
                { 
                    id: 'asymmetric', 
                    title: 'Asymmetric Encryption Quiz', 
                    description: 'RSA, ECC, key exchange',
                    subtopics: [
                        { id: 'rsa-quiz', title: 'RSA Quiz', description: 'RSA algorithm and applications' },
                        { id: 'ecc-quiz', title: 'ECC Quiz', description: 'Elliptic curve cryptography' },
                        { id: 'key-exchange-quiz', title: 'Key Exchange Quiz', description: 'Diffie-Hellman and protocols' },
                        { id: 'signatures-quiz', title: 'Digital Signatures Quiz', description: 'Signature schemes and verification' }
                    ]
                },
                { 
                    id: 'hashing', 
                    title: 'Hash Functions Quiz', 
                    description: 'SHA, MD5, digital signatures',
                    subtopics: [
                        { id: 'sha-quiz', title: 'SHA Quiz', description: 'SHA family algorithms' },
                        { id: 'md5-quiz', title: 'MD5 Quiz', description: 'MD5 and its vulnerabilities' },
                        { id: 'hash-properties-quiz', title: 'Hash Properties Quiz', description: 'Hash function characteristics' },
                        { id: 'hmac-quiz', title: 'HMAC Quiz', description: 'Message authentication codes' }
                    ]
                },
                { 
                    id: 'protocols', 
                    title: 'Protocols Quiz', 
                    description: 'TLS, PKI, security protocols',
                    subtopics: [
                        { id: 'tls-quiz', title: 'TLS/SSL Quiz', description: 'Transport layer security' },
                        { id: 'pki-quiz', title: 'PKI Quiz', description: 'Public key infrastructure' },
                        { id: 'certificates-quiz', title: 'Certificates Quiz', description: 'Digital certificates and validation' },
                        { id: 'auth-quiz', title: 'Authentication Quiz', description: 'Authentication protocols' }
                    ]
                },
                { 
                    id: 'advanced', 
                    title: 'Advanced Topics Quiz', 
                    description: 'Quantum, modern cryptography',
                    subtopics: [
                        { id: 'quantum-quiz', title: 'Quantum Cryptography Quiz', description: 'Quantum concepts and protocols' },
                        { id: 'post-quantum-quiz', title: 'Post-Quantum Quiz', description: 'Quantum-resistant cryptography' },
                        { id: 'blockchain-quiz', title: 'Blockchain Quiz', description: 'Blockchain cryptographic concepts' },
                        { id: 'modern-quiz', title: 'Modern Crypto Quiz', description: 'Latest cryptographic developments' }
                    ]
                }
            ]
        };
    }

    // Generate detailed messages for subtopics
    function generateSubtopicMessage(mode, mainTopic, subtopicId) {
        const messages = {
            learning: {
                overview: {
                    history: "Explain the detailed history of cryptography from ancient times to modern era, including Caesar cipher, Enigma machine, DES development, and the advent of public-key cryptography. Include key historical figures and milestones.",
                    fundamentals: "Explain the fundamental concepts of cryptography including confidentiality, integrity, authentication, non-repudiation, key management, and the difference between encoding, encryption, and hashing.",
                    types: "Provide a comprehensive overview of the three main types of cryptography: symmetric encryption (shared secret), asymmetric encryption (public-key), and hash functions, with their use cases and relationships.",
                    applications: "Explain real-world applications of cryptography including HTTPS/TLS, digital signatures, cryptocurrency, messaging apps, VPNs, password storage, and blockchain technology."
                },
                symmetric: {
                    aes: "Explain AES (Advanced Encryption Standard) in detail including its development history, key sizes (128, 192, 256 bits), rounds, SubBytes, ShiftRows, MixColumns operations, and why it replaced DES.",
                    des: "Explain DES (Data Encryption Standard) including its 56-bit key structure, 16 rounds, Feistel network, why it became vulnerable, and the development of 3DES as a temporary solution.",
                    'block-ciphers': "Explain block ciphers in detail including fixed block sizes, padding schemes, and the most important cipher modes: ECB, CBC, CFB, OFB, CTR, and GCM with their security properties.",
                    'stream-ciphers': "Explain stream ciphers including their bit-by-bit operation, pseudorandom keystreams, advantages over block ciphers for real-time applications, and examples like RC4 and ChaCha20.",
                    'cipher-modes': "Explain cipher modes of operation in detail: ECB (insecure), CBC (requires IV), CFB, OFB, CTR (parallelizable), and authenticated modes like GCM and CCM."
                },
                asymmetric: {
                    rsa: "Explain RSA algorithm in detail including key generation using prime numbers, modular arithmetic, public/private key relationship, encryption/decryption process, digital signatures, and current security considerations.",
                    ecc: "Explain Elliptic Curve Cryptography including the mathematical foundation, advantages over RSA (smaller key sizes), ECDSA for signatures, ECDH for key exchange, and common curves like P-256.",
                    'key-exchange': "Explain key exchange protocols including Diffie-Hellman key exchange, the discrete logarithm problem, man-in-the-middle attacks, and authenticated key exchange protocols.",
                    'digital-signatures': "Explain digital signatures in detail including RSA signatures, ECDSA, DSA, the signing and verification process, hash-then-sign paradigm, and non-repudiation properties.",
                    'pki-concepts': "Explain Public Key Infrastructure including certificate authorities, certificate chains, root certificates, certificate validation, revocation (CRL/OCSP), and trust models."
                },
                hashing: {
                    sha: "Explain the SHA (Secure Hash Algorithm) family including SHA-1 (deprecated), SHA-2 family (SHA-224, SHA-256, SHA-384, SHA-512), SHA-3, their construction, and security properties.",
                    md5: "Explain MD5 hash function including its 128-bit output, collision vulnerabilities discovered by Xiaoyun Wang, why it's no longer secure, and its remaining uses for checksums.",
                    'hash-properties': "Explain essential hash function properties: deterministic output, fixed output size, avalanche effect, pre-image resistance, second pre-image resistance, and collision resistance.",
                    hmac: "Explain HMAC (Hash-based Message Authentication Code) including its construction with nested hashing, key derivation, resistance to length extension attacks, and use in protocols like TLS.",
                    applications: "Explain hash function applications including password storage with salts, file integrity checking, digital signatures, blockchain proof-of-work, and Merkle trees."
                },
                protocols: {
                    'tls-ssl': "Explain TLS/SSL protocols including the handshake process, certificate validation, cipher suite negotiation, perfect forward secrecy, and the evolution from SSL to TLS 1.3.",
                    pki: "Explain Public Key Infrastructure in detail including certificate authorities, registration authorities, certificate lifecycle management, cross-certification, and trust models.",
                    certificates: "Explain X.509 digital certificates including their structure, fields, certificate chains, path validation, revocation checking, and certificate transparency.",
                    authentication: "Explain authentication protocols including OAuth 2.0, SAML, Kerberos, multi-factor authentication, and the difference between authentication and authorization.",
                    'secure-messaging': "Explain secure messaging protocols including Signal Protocol, end-to-end encryption, forward secrecy, deniability, and how apps like WhatsApp implement these concepts."
                },
                advanced: {
                    quantum: "Explain quantum cryptography including quantum key distribution (QKD), BB84 protocol, quantum entanglement, the no-cloning theorem, and practical quantum communication systems.",
                    'post-quantum': "Explain post-quantum cryptography including the threat from quantum computers to current crypto, lattice-based, code-based, and multivariate cryptographic approaches being standardized.",
                    blockchain: "Explain blockchain cryptography including hash chains, Merkle trees, digital signatures for transactions, consensus mechanisms, and cryptographic primitives in Bitcoin and Ethereum.",
                    'zero-knowledge': "Explain zero-knowledge proofs including the concept of proving knowledge without revealing information, zk-SNARKs, zk-STARKs, and applications in privacy-preserving systems.",
                    homomorphic: "Explain homomorphic encryption including the ability to compute on encrypted data, fully homomorphic encryption (FHE), partially homomorphic schemes, and practical applications."
                }
            },
            quiz: {
                mixed: {
                    general: "Start a comprehensive cryptography quiz with 5 questions randomly selected from all topics including symmetric encryption, asymmetric encryption, hash functions, protocols, and advanced concepts.",
                    beginner: "Start a beginner-level mixed cryptography quiz focusing on basic concepts, terminology, and fundamental principles across symmetric encryption, asymmetric encryption, and hash functions.",
                    intermediate: "Start an intermediate-level mixed cryptography quiz with moderate difficulty questions covering practical applications, algorithm details, and protocol understanding.",
                    advanced: "Start an advanced mixed cryptography quiz with challenging questions about algorithm internals, security proofs, advanced protocols, and cutting-edge research topics."
                },
                symmetric: {
                    'aes-quiz': "Start a focused quiz on AES (Advanced Encryption Standard) covering its key sizes, round structure, operations (SubBytes, ShiftRows, MixColumns), security properties, and practical implementations.",
                    'des-quiz': "Start a quiz on DES (Data Encryption Standard) covering its history, 56-bit keys, Feistel structure, vulnerabilities, 3DES, and the transition to AES.",
                    'block-ciphers-quiz': "Start a quiz on block ciphers covering cipher modes (ECB, CBC, CTR, GCM), padding schemes, block sizes, and security considerations for different modes.",
                    'stream-ciphers-quiz': "Start a quiz on stream ciphers covering keystream generation, synchronous vs self-synchronizing, advantages for real-time applications, and examples like RC4 and ChaCha20."
                },
                asymmetric: {
                    'rsa-quiz': "Start a quiz on RSA covering key generation, modular arithmetic, encryption/decryption process, digital signatures, key sizes, and current security recommendations.",
                    'ecc-quiz': "Start a quiz on Elliptic Curve Cryptography covering curve mathematics, key advantages, ECDSA signatures, ECDH key exchange, and standard curves.",
                    'key-exchange-quiz': "Start a quiz on key exchange protocols covering Diffie-Hellman, discrete logarithm problem, authenticated key exchange, and man-in-the-middle prevention.",
                    'signatures-quiz': "Start a quiz on digital signatures covering RSA signatures, ECDSA, DSA, signature verification, non-repudiation, and hash-then-sign paradigm."
                },
                hashing: {
                    'sha-quiz': "Start a quiz on SHA hash functions covering SHA-1, SHA-2 family, SHA-3, their security properties, output sizes, and appropriate use cases.",
                    'md5-quiz': "Start a quiz on MD5 covering its structure, collision vulnerabilities, why it's deprecated for security uses, and remaining appropriate applications.",
                    'hash-properties-quiz': "Start a quiz on hash function properties covering collision resistance, pre-image resistance, avalanche effect, and deterministic behavior.",
                    'hmac-quiz': "Start a quiz on HMAC covering its construction, key usage, protection against length extension attacks, and applications in authentication protocols."
                },
                protocols: {
                    'tls-quiz': "Start a quiz on TLS/SSL protocols covering handshake process, certificate validation, cipher suites, perfect forward secrecy, and protocol evolution.",
                    'pki-quiz': "Start a quiz on Public Key Infrastructure covering certificate authorities, trust models, certificate validation, revocation, and cross-certification.",
                    'certificates-quiz': "Start a quiz on digital certificates covering X.509 format, certificate chains, validation process, revocation checking, and certificate transparency.",
                    'auth-quiz': "Start a quiz on authentication protocols covering OAuth, SAML, Kerberos, multi-factor authentication, and authentication vs authorization."
                },
                advanced: {
                    'quantum-quiz': "Start a quiz on quantum cryptography covering quantum key distribution, BB84 protocol, quantum entanglement, no-cloning theorem, and practical QKD systems.",
                    'post-quantum-quiz': "Start a quiz on post-quantum cryptography covering quantum computing threats, lattice-based crypto, code-based systems, and NIST standardization efforts.",
                    'blockchain-quiz': "Start a quiz on blockchain cryptography covering hash chains, Merkle trees, digital signatures in transactions, consensus mechanisms, and cryptocurrency security.",
                    'modern-quiz': "Start a quiz on modern cryptographic developments covering zero-knowledge proofs, homomorphic encryption, secure multi-party computation, and privacy-preserving technologies."
                }
            }
        };
        
        return messages[mode]?.[mainTopic]?.[subtopicId] || `Explore ${subtopicId} in ${mainTopic} for ${mode === 'learning' ? 'learning' : 'quiz'} mode.`;
    }

    // Add topic selection handlers
    function addTopicSelectionHandlers(messageElement) {
        const topicOptions = messageElement.querySelectorAll('.topic-option');
        
        // Add hover effects
        topicOptions.forEach(option => {
            option.addEventListener('mouseenter', function() {
                this.style.borderColor = 'var(--primary-color)';
                this.style.background = 'var(--secondary-color)';
                this.style.transform = 'translateY(-2px)';
                this.style.boxShadow = '0 8px 25px rgba(255, 0, 0, 0.15)';
            });
            
            option.addEventListener('mouseleave', function() {
                if (!this.classList.contains('selected')) {
                    this.style.borderColor = 'rgba(255, 0, 0, 0.2)';
                    this.style.background = 'var(--card-bg)';
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = 'var(--shadow)';
                }
            });
        });
        
        topicOptions.forEach(option => {
            option.addEventListener('click', async function() {
                const mode = this.getAttribute('data-mode');
                const topicId = this.getAttribute('data-topic');
                
                // Visual feedback - enhanced selection state
                this.style.background = 'var(--secondary-color)';
                this.style.borderColor = 'var(--primary-color)';
                this.style.boxShadow = '0 6px 20px rgba(255, 0, 0, 0.25)';
                this.style.transform = 'scale(0.98)';
                this.classList.add('selected');
                
                // Disable all topic options
                topicOptions.forEach(opt => {
                    opt.style.pointerEvents = 'none';
                    if (opt !== this) {
                        opt.style.opacity = '0.5';
                        opt.style.transform = 'scale(0.95)';
                    }
                });
                
                // Show subtopic selection instead of direct message
                setTimeout(() => {
                    showSubtopicSelection(mode, topicId);
                }, 300);
            });
        });
    }

    // Add next question button handlers (only handle existing buttons, don't create new ones)
    function addNextQuestionHandlers(messageElement) {
        // Handle existing Next Question buttons (created by backend action flags)
        const nextButtons = messageElement.querySelectorAll('.next-question-btn');
        nextButtons.forEach(button => {
            button.addEventListener('click', async function() {
                // Visual feedback
                this.style.background = 'var(--primary-color)';
                this.style.color = 'white';
                this.textContent = 'Loading...';
                
                // Send "Next Question" request
                messageInput.value = "Next Question";
                await handleSubmit();
                
                // Remove the button after clicking
                this.remove();
            });
        });
        
        // Handle existing New Quiz buttons (created by backend action flags)
        const newQuizButtons = messageElement.querySelectorAll('.new-quiz-btn');
        newQuizButtons.forEach(button => {
            button.addEventListener('click', async function() {
                // Visual feedback
                this.style.background = 'var(--primary-color)';
                this.style.color = 'white';
                this.textContent = 'Starting...';
                
                // Show topic selection for new quiz
                showTopicSelection('quiz');
                
                // Remove the button after clicking
                this.remove();
            });
        });
    }

    // Create message element
    function createMessageElement(content, isUser = false, timestamp = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        const time = timestamp || new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas ${isUser ? 'fa-user' : 'fa-robot'}"></i>
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    ${isUser ? `<p>${escapeHtml(content)}</p>` : formatBotMessage(content)}
                </div>
                <div class="message-time">
                    <span>${time}</span>
                </div>
            </div>
        `;
        
        return messageDiv;
    }

    // Enhanced bot message formatting function
    function formatBotMessage(content) {
        // Remove excessive emojis at the start of lines
        content = content.replace(/^[🎯🔧✅❌⚡🚀📊🎨🔍💡🎉🎪⭐🔥📝🎭🎵🌟💫⭐️🔍📚🎓💻🔐🎯🎪🎨🎊🎈🎁🌈💎🎀🎊]+\s*/gm, '');
        
        // Clean up excessive bold formatting
        content = content.replace(/\*\*[\-\s]*\*\*/g, '');
        
        // Convert markdown-like formatting to HTML
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Split content into lines for processing
        const lines = content.split('\n');
        let formatted = '';
        let inList = false;
        let inOrderedList = false;
        let currentParagraph = '';
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();
            
            if (!line) {
                // Empty line - end current paragraph/list
                if (inList) {
                    formatted += '</ul>';
                    inList = false;
                } else if (inOrderedList) {
                    formatted += '</ol>';
                    inOrderedList = false;
                } else if (currentParagraph) {
                    formatted += `<p>${currentParagraph.trim()}</p>`;
                    currentParagraph = '';
                }
                continue;
            }
            
            // Check for quiz options (A) B) C) D) format
            if (/^[A-D]\)\s/.test(line)) {
                if (!inList) {
                    if (currentParagraph) {
                        formatted += `<p>${currentParagraph.trim()}</p>`;
                        currentParagraph = '';
                    }
                    formatted += '<ul class="quiz-options">';
                    inList = true;
                }
                const optionText = line.substring(2).trim();
                const optionLetter = line.charAt(0);
                formatted += `<li class="quiz-option-item" data-option="${optionLetter}) ${optionText}"><strong>${optionLetter})</strong> ${optionText}</li>`;
                continue;
            }
            
            // Check for numbered lists (1. 2. 3.)
            if (/^\d+\.\s/.test(line)) {
                if (!inOrderedList) {
                    if (currentParagraph) {
                        formatted += `<p>${currentParagraph.trim()}</p>`;
                        currentParagraph = '';
                    }
                    if (inList) {
                        formatted += '</ul>';
                        inList = false;
                    }
                    formatted += '<ol>';
                    inOrderedList = true;
                }
                const listText = line.replace(/^\d+\.\s/, '');
                formatted += `<li>${listText}</li>`;
                continue;
            }
            
            // Check for bullet points (- or • or *)
            if (/^[-•*]\s/.test(line)) {
                if (!inList) {
                    if (currentParagraph) {
                        formatted += `<p>${currentParagraph.trim()}</p>`;
                        currentParagraph = '';
                    }
                    if (inOrderedList) {
                        formatted += '</ol>';
                        inOrderedList = false;
                    }
                    formatted += '<ul>';
                    inList = true;
                }
                const listText = line.replace(/^[-•*]\s/, '');
                formatted += `<li>${listText}</li>`;
                continue;
            }
            
            // Check for headers
            if (line.startsWith('#')) {
                if (inList) {
                    formatted += '</ul>';
                    inList = false;
                } else if (inOrderedList) {
                    formatted += '</ol>';
                    inOrderedList = false;
                } else if (currentParagraph) {
                    formatted += `<p>${currentParagraph.trim()}</p>`;
                    currentParagraph = '';
                }
                
                const level = line.match(/^#+/)[0].length;
                const text = line.replace(/^#+\s*/, '');
                formatted += `<h${Math.min(level, 6)}>${text}</h${Math.min(level, 6)}>`;
                continue;
            }
            
            // Regular text - add to current paragraph
            if (inList || inOrderedList) {
                // If we're in a list but this isn't a list item, close the list
                if (inList) {
                    formatted += '</ul>';
                    inList = false;
                } else if (inOrderedList) {
                    formatted += '</ol>';
                    inOrderedList = false;
                }
            }
            
            if (currentParagraph) {
                currentParagraph += ' ' + line;
            } else {
                currentParagraph = line;
            }
        }
        
        // Close any remaining open elements
        if (inList) {
            formatted += '</ul>';
        } else if (inOrderedList) {
            formatted += '</ol>';
        } else if (currentParagraph) {
            formatted += `<p>${currentParagraph.trim()}</p>`;
        }
        
        // Post-process to catch any missed quiz options in paragraph format
        formatted = postProcessQuizOptions(formatted);
        
        // Note: Next Question buttons are now handled via action flags in sendMessage()
        // No longer adding buttons here to prevent duplicates
        
        return formatted || `<p>${content}</p>`;
    }

    // Add Next Question button for quiz feedback
    function addNextQuestionButton(html) {
        // Detect quiz feedback patterns (Correct! or Incorrect.)
        if (html.match(/(Correct!|Incorrect\.)/)) {
            // Check if this is quiz feedback (not a question with options)
            if (!html.includes('quiz-options')) {
                html += '<div style="margin-top: 15px;"><button class="next-question-btn" style="background: var(--primary-color); color: white; border: none; padding: 10px 20px; border-radius: 25px; cursor: pointer; font-size: 14px; font-weight: 500; transition: all 0.3s ease;">Next Question</button></div>';
            }
        }
        return html;
    }

    // Post-process function to catch quiz options that were missed
    function postProcessQuizOptions(html) {
        // Look for patterns like "A) text B) text C) text D) text" within paragraphs
        return html.replace(/<p>([^<]*?[A-D]\)\s*[^<]+?\s+[A-D]\)[^<]*?)<\/p>/g, function(match, content) {
            // Check if this looks like quiz options
            const optionMatches = content.match(/[A-D]\)\s*[^A-D)]+?(?=\s*[A-D]\)|$)/g);
            if (optionMatches && optionMatches.length >= 2) {
                let quizHtml = '<ul class="quiz-options">';
                optionMatches.forEach(option => {
                    const optionMatch = option.match(/([A-D])\)\s*(.+)/);
                    if (optionMatch) {
                        const letter = optionMatch[1];
                        const text = optionMatch[2].trim();
                        quizHtml += `<li class="quiz-option-item" data-option="${letter}) ${text}"><strong>${letter})</strong> ${text}</li>`;
                    }
                });
                quizHtml += '</ul>';
                return quizHtml;
            }
            return match;
        });
    }

    // Escape HTML
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Smart context management - create summary of older messages
    function createConversationSummary(messages) {
        if (messages.length === 0) return "";
        
        const topics = [];
        const keyPhrases = [];
        // Expanded keyword map for synonyms and related terms
        const keywordMap = [
            { topic: 'AES encryption', keywords: ['aes', 'advanced encryption', 'rijndael', 'block cipher', 'symmetric encryption'] },
            { topic: 'DES encryption', keywords: ['des', 'data encryption standard', 'feistel', '56-bit key'] },
            { topic: 'RSA encryption', keywords: ['rsa', 'rivest', 'shamir', 'adlemann', 'public key', 'asymmetric encryption', 'modulus', 'private key'] },
            { topic: 'Caesar cipher', keywords: ['caesar', 'shift cipher', 'julius', 'monoalphabetic'] },
            { topic: 'Vigenère cipher', keywords: ['vigenere', 'vigenère', 'polyalphabetic', 'repeating key'] },
            { topic: 'Hill cipher', keywords: ['hill', 'matrix cipher', 'linear algebra', 'matrix multiplication'] },
            { topic: 'HMAC authentication', keywords: ['hmac', 'hash-based message', 'mac', 'message authentication code'] },
            { topic: 'SHA hashing', keywords: ['sha', 'secure hash', 'sha-1', 'sha-256', 'sha-512', 'digest'] },
            { topic: 'MD5 hashing', keywords: ['md5', 'message digest 5', 'digest', 'collision'] },
            { topic: 'Diffie-Hellman key exchange', keywords: ['diffie', 'hellman', 'key exchange', 'shared secret', 'modular exponentiation'] },
            { topic: 'Hashing algorithms', keywords: ['hash', 'digest', 'checksum', 'hash function'] },
            { topic: 'Encryption/Decryption', keywords: ['encrypt', 'decryption', 'cipher', 'plaintext', 'ciphertext', 'cryptanalysis', 'cryptography'] },
        ];
        
        // Simple phrase extraction: extract quoted text and code blocks
        function extractPhrases(text) {
            const phrases = [];
            // Extract quoted phrases
            const quoteRegex = /"([^"]+)"|'([^']+)'/g;
            let match;
            while ((match = quoteRegex.exec(text)) !== null) {
                phrases.push(match[1] || match[2]);
            }
            // Extract code blocks (backticks)
            const codeRegex = /`([^`]+)`/g;
            while ((match = codeRegex.exec(text)) !== null) {
                phrases.push(match[1]);
            }
            return phrases;
        }
        
        for (let i = 0; i < messages.length; i += 2) {
            const userMessage = messages[i];
            const assistantMessage = messages[i + 1];
            
            if (userMessage) {
                const userContent = userMessage.content.toLowerCase();
                // Expanded topic detection
                for (const entry of keywordMap) {
                    for (const kw of entry.keywords) {
                        if (userContent.includes(kw) && !topics.includes(entry.topic)) {
                            topics.push(entry.topic);
                        }
                    }
                }
                // Extract key phrases from user message
                keyPhrases.push(...extractPhrases(userMessage.content));
            }
            // Optionally, include bot response key points
            if (assistantMessage) {
                // Extract key phrases from bot response
                keyPhrases.push(...extractPhrases(assistantMessage.content));
            }
        }
        
        let summary = "";
        if (topics.length > 0) {
            summary += `Previous conversation covered: ${topics.join(', ')}.`;
        }
        if (keyPhrases.length > 0) {
            summary += ` Key phrases: ${keyPhrases.slice(0, 5).join('; ')}.`;
        }
        if (!summary) {
            summary = `Previous conversation about cryptography concepts.`;
        }
        
        // Placeholder: For advanced use, send older messages to backend for AI summarization
        // Example: if (messages.length > 50) { fetch('/api/summarize/', { ... }) }
        
        return summary;
    }

    // Prepare optimized conversation context
    function prepareConversationContext() {
        if (conversationHistory.length <= RECENT_MESSAGES_LIMIT) {
            // If we have few messages, send all
            return conversationHistory;
        }
        
        // Split into old messages (for summary) and recent messages (full context)
        const recentMessages = conversationHistory.slice(-RECENT_MESSAGES_LIMIT);
        const olderMessages = conversationHistory.slice(0, -RECENT_MESSAGES_LIMIT);
        
        // Create or update summary
        if (olderMessages.length > 0 && conversationSummary === "") {
            conversationSummary = createConversationSummary(olderMessages);
        }
        
        // Prepare context array
        const context = [];
        
        // Add summary as context if we have one
        if (conversationSummary) {
            context.push({
                role: "system",
                content: conversationSummary
            });
        }
        
        // Add recent full messages
        context.push(...recentMessages);
        
        return context;
    }

    // Send message to API with smart conversation context
    async function sendMessage(message) {
        try {
            // Prepare optimized conversation context
            const contextToSend = prepareConversationContext();
            
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ 
                    message: message,
                    history: contextToSend
                })
            });

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Failed to get response');
            }

            // Check for special actions in response
            if (data.action) {
                // Handle mode switching actions
                if (data.action === 'show_topic_selection') {
                    showTopicSelection(data.mode);
                    return { message: data.message, hasAction: true };
                } else if (data.action === 'show_free_chat') {
                    showFreeChatWelcome();
                    return { message: data.message, hasAction: true };
                } else if (data.action === 'next_question') {
                    // For quiz responses that should show next question button
                    return { message: data.response, hasAction: false, showNextButton: true };
                } else if (data.action === 'new_quiz') {
                    // For final quiz response that should show new quiz option
                    return { message: data.response, hasAction: false, showNewQuiz: true };
                }
            }

            // Add user message and AI response to conversation history
            conversationHistory.push({role: "user", content: message});
            conversationHistory.push({role: "assistant", content: data.response || data.message});

            // Smart conversation management
            if (conversationHistory.length > SUMMARY_THRESHOLD) {
                // Update summary when we have too many messages
                const messagesToSummarize = conversationHistory.slice(0, -RECENT_MESSAGES_LIMIT);
                if (messagesToSummarize.length > 0) {
                    conversationSummary = createConversationSummary(messagesToSummarize);
                }
            }

            return data.response || data.message;
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    }

    // Get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Handle message submission
    async function handleSubmit() {
        const message = messageInput.value.trim();
        
        if (!message) return;
        
        // Disable input and button
        messageInput.disabled = true;
        sendButton.disabled = true;
        
        // Add user message
        const userMessage = createMessageElement(message, true);
        chatMessages.appendChild(userMessage);
        
        // Clear input
        messageInput.value = '';
        updateCharCount();
        autoResizeTextarea();
        
        // Show typing indicator
        showTyping();
        
        try {
            // Send message to API
            const response = await sendMessage(message);
            
            // Hide typing indicator
            hideTyping();
            
            // Check if response has action (mode switching)
            if (response && typeof response === 'object' && response.hasAction) {
                // For mode switching, just show the action message briefly
                const actionMessage = createMessageElement(response.message, false);
                chatMessages.appendChild(actionMessage);
                scrollToBottom();
                return; // Don't add handlers for mode switching messages
            }
            
            // Check if response is a quiz response that needs special handling
            if (response && typeof response === 'object' && (response.showNextButton || response.showNewQuiz)) {
                // Add bot response with quiz handling
                const botMessage = createMessageElement(response.message, false);
                
                // Add Next Question button if needed
                if (response.showNextButton) {
                    const messageContent = botMessage.querySelector('.message-bubble');
                    messageContent.innerHTML += '<div style="margin-top: 15px;"><button class="next-question-btn" style="background: var(--primary-color); color: white; border: none; padding: 10px 20px; border-radius: 25px; cursor: pointer; font-size: 14px; font-weight: 500; transition: all 0.3s ease;">Next Question</button></div>';
                }
                
                // Add New Quiz button if needed
                if (response.showNewQuiz) {
                    const messageContent = botMessage.querySelector('.message-bubble');
                    messageContent.innerHTML += '<div style="margin-top: 15px;"><button class="new-quiz-btn" style="background: var(--primary-color); color: white; border: none; padding: 10px 20px; border-radius: 25px; cursor: pointer; font-size: 14px; font-weight: 500; transition: all 0.3s ease; margin-right: 10px;">New Quiz</button></div>';
                }
                
                chatMessages.appendChild(botMessage);
                
                // Add quiz option handlers to the new message
                addQuizOptionHandlers(botMessage);
                
                // Add next question handlers to the new message
                addNextQuestionHandlers(botMessage);
                
                scrollToBottom();
                return;
            }
            
            // Add bot response (normal chat response)
            const botMessage = createMessageElement(response, false);
            chatMessages.appendChild(botMessage);
            
            // Add quiz option handlers to the new message
            addQuizOptionHandlers(botMessage);
            
            // Add mode selection handlers to the new message
            addModeSelectionHandlers(botMessage);
            
            // Add next question handlers to the new message
            addNextQuestionHandlers(botMessage);
            
        } catch (error) {
            hideTyping();
            
            // Show error message
            const errorMessage = createMessageElement(
                `Sorry, I encountered an error: ${error.message}. Please try again or check if the API key is configured correctly.`,
                false
            );
            errorMessage.querySelector('.message-bubble').style.background = '#fee';
            errorMessage.querySelector('.message-bubble').style.border = '1px solid #fcc';
            errorMessage.querySelector('.message-bubble').style.color = '#d00';
            chatMessages.appendChild(errorMessage);
        } finally {
            // Re-enable input and button
            messageInput.disabled = false;
            sendButton.disabled = false;
            messageInput.focus();
            scrollToBottom();
        }
    }

    // Event listeners
    messageInput.addEventListener('input', function() {
        updateCharCount();
        autoResizeTextarea();
    });

    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    });

    sendButton.addEventListener('click', handleSubmit);

    // Quick question cards
    questionCards.forEach(card => {
        card.addEventListener('click', function() {
            const question = this.getAttribute('data-question');
            messageInput.value = question;
            updateCharCount();
            autoResizeTextarea();
            messageInput.focus();
        });
    });

    // Clear conversation functionality
    const clearButton = document.getElementById('clearConversation');
    if (clearButton) {
        clearButton.addEventListener('click', function() {
            if (confirm('Start a new conversation? This will clear the current chat history.')) {
                // Clear conversation history and summary
                conversationHistory = [];
                conversationSummary = "";
                
                // Clear chat messages (keep only welcome message)
                const welcomeMessage = chatMessages.querySelector('.bot-message');
                chatMessages.innerHTML = '';
                if (welcomeMessage) {
                    chatMessages.appendChild(welcomeMessage);
                }
                
                // Reset input
                messageInput.value = '';
                updateCharCount();
                autoResizeTextarea();
                
                // Show success message briefly
                const originalText = clearButton.innerHTML;
                clearButton.innerHTML = '<i class="fas fa-check"></i> Cleared!';
                clearButton.style.color = 'var(--primary-color)';
                
                setTimeout(() => {
                    clearButton.innerHTML = originalText;
                    clearButton.style.color = '';
                }, 2000);
            }
        });
    }

    // Initialize
    updateCharCount();
    messageInput.focus();
    scrollToBottom();
    
    // Add mode selection handlers to the initial welcome message
    addModeSelectionHandlers(document);

    // Add some visual feedback
    messageInput.addEventListener('focus', function() {
        this.parentElement.style.transform = 'translateY(-2px)';
    });

    messageInput.addEventListener('blur', function() {
        this.parentElement.style.transform = 'translateY(0)';
    });
});
