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

    // Format bot message with proper HTML
    function formatBotMessage(content) {
        // Convert markdown-like formatting to HTML
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Convert line breaks to paragraphs
        const paragraphs = content.split('\n\n').filter(p => p.trim());
        let formatted = '';
        
        for (let paragraph of paragraphs) {
            if (paragraph.trim().startsWith('- ')) {
                // Handle bullet points
                const items = paragraph.split('\n').filter(item => item.trim());
                formatted += '<ul>';
                for (let item of items) {
                    if (item.trim().startsWith('- ')) {
                        formatted += `<li>${item.substring(2).trim()}</li>`;
                    }
                }
                formatted += '</ul>';
            } else {
                formatted += `<p>${paragraph.trim()}</p>`;
            }
        }
        
        return formatted || `<p>${content}</p>`;
    }

    // Escape HTML
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Send message to API
    async function sendMessage(message) {
        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Failed to get response');
            }

            return data.response;
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
            
            // Add bot response
            const botMessage = createMessageElement(response, false);
            chatMessages.appendChild(botMessage);
            
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

    // Initialize
    updateCharCount();
    messageInput.focus();
    scrollToBottom();

    // Add some visual feedback
    messageInput.addEventListener('focus', function() {
        this.parentElement.style.transform = 'translateY(-2px)';
    });

    messageInput.addEventListener('blur', function() {
        this.parentElement.style.transform = 'translateY(0)';
    });
});
