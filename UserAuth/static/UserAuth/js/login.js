// Login JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const rememberCheckbox = document.getElementById('remember');

    // Form validation
    function validateForm() {
        let isValid = true;
        
        // Clear previous error states
        clearErrors();
        
        // Validate username
        if (!usernameInput.value.trim()) {
            showError(usernameInput, 'Username is required');
            isValid = false;
        }
        
        // Validate password
        if (!passwordInput.value.trim()) {
            showError(passwordInput, 'Password is required');
            isValid = false;
        }
        
        return isValid;
    }

    // Show error message
    function showError(input, message) {
        const inputGroup = input.closest('.input-group');
        inputGroup.classList.add('error');
        
        // Remove existing error message
        const existingError = inputGroup.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        // Add new error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `<span>⚠️</span> ${message}`;
        inputGroup.appendChild(errorDiv);
    }

    // Clear all errors
    function clearErrors() {
        const errorGroups = document.querySelectorAll('.input-group.error');
        errorGroups.forEach(group => {
            group.classList.remove('error');
            const errorMessage = group.querySelector('.error-message');
            if (errorMessage) {
                errorMessage.remove();
            }
        });
    }

    // Show loading state
    function showLoading(button) {
        button.classList.add('btn-loading');
        button.disabled = true;
    }

    // Hide loading state
    function hideLoading(button) {
        button.classList.remove('btn-loading');
        button.disabled = false;
    }

    // Handle form submission
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }
        
        const submitButton = loginForm.querySelector('button[type="submit"]');
        showLoading(submitButton);
        
        try {
            const formData = new FormData(loginForm);
            const response = await fetch(loginForm.action || window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            
            if (response.ok) {
                // Check if response is JSON (AJAX) or HTML (regular form)
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    const data = await response.json();
                    if (data.success) {
                        showMessage('Login successful! Redirecting...', 'success');
                        setTimeout(() => {
                            window.location.href = '/';
                        }, 1500);
                    } else {
                        showMessage(data.message || 'Login failed', 'error');
                    }
                } else {
                    // Regular form submission - let browser handle redirect
                    window.location.reload();
                }
            } else {
                showMessage('Login failed. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Login error:', error);
            showMessage('An error occurred. Please try again.', 'error');
        } finally {
            hideLoading(submitButton);
        }
    });

    // Show message to user
    function showMessage(message, type) {
        // Remove existing messages
        const existingMessages = document.querySelectorAll('.temp-message');
        existingMessages.forEach(msg => msg.remove());
        
        // Create new message
        const messageDiv = document.createElement('div');
        messageDiv.className = `alert alert-${type} temp-message`;
        messageDiv.textContent = message;
        messageDiv.style.position = 'fixed';
        messageDiv.style.top = '20px';
        messageDiv.style.right = '20px';
        messageDiv.style.zIndex = '1000';
        messageDiv.style.maxWidth = '300px';
        
        document.body.appendChild(messageDiv);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }

    // Remember me functionality
    if (rememberCheckbox) {
        // Load saved username if remember me was checked
        const savedUsername = localStorage.getItem('rememberedUsername');
        if (savedUsername) {
            usernameInput.value = savedUsername;
            rememberCheckbox.checked = true;
        }
        
        // Save/clear username based on remember me checkbox
        rememberCheckbox.addEventListener('change', function() {
            if (this.checked && usernameInput.value) {
                localStorage.setItem('rememberedUsername', usernameInput.value);
            } else {
                localStorage.removeItem('rememberedUsername');
            }
        });
        
        // Update saved username when input changes
        usernameInput.addEventListener('input', function() {
            if (rememberCheckbox.checked) {
                localStorage.setItem('rememberedUsername', this.value);
            }
        });
    }

    // Input validation on blur
    usernameInput.addEventListener('blur', function() {
        if (!this.value.trim()) {
            showError(this, 'Username is required');
        } else {
            const inputGroup = this.closest('.input-group');
            inputGroup.classList.remove('error');
            const errorMessage = inputGroup.querySelector('.error-message');
            if (errorMessage) {
                errorMessage.remove();
            }
        }
    });

    passwordInput.addEventListener('blur', function() {
        if (!this.value.trim()) {
            showError(this, 'Password is required');
        } else {
            const inputGroup = this.closest('.input-group');
            inputGroup.classList.remove('error');
            const errorMessage = inputGroup.querySelector('.error-message');
            if (errorMessage) {
                errorMessage.remove();
            }
        }
    });

    // Enter key handling
    usernameInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            passwordInput.focus();
        }
    });

    passwordInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            loginForm.dispatchEvent(new Event('submit'));
        }
    });
});

// Password toggle functionality
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleButton = passwordInput.nextElementSibling;
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleButton.textContent = '🙈';
    } else {
        passwordInput.type = 'password';
        toggleButton.textContent = '👁️';
    }
}

// Auto-focus first empty input
document.addEventListener('DOMContentLoaded', function() {
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    
    if (!usernameInput.value) {
        usernameInput.focus();
    } else if (!passwordInput.value) {
        passwordInput.focus();
    }
});
