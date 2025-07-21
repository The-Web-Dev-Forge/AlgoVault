// Forgot Password JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    const forgotPasswordForm = document.getElementById('forgotPasswordForm');
    const emailInput = document.getElementById('email');

    // Email validation
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Show error message
    function showError(input, message) {
        const inputGroup = input.closest('.input-group');
        inputGroup.classList.remove('success');
        inputGroup.classList.add('error');
        
        const existingError = inputGroup.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `<span>⚠️</span> ${message}`;
        inputGroup.appendChild(errorDiv);
    }

    // Show success message
    function showSuccess(input, message) {
        const inputGroup = input.closest('.input-group');
        inputGroup.classList.remove('error');
        inputGroup.classList.add('success');
        
        const existingMessage = inputGroup.querySelector('.error-message, .success-message');
        if (existingMessage) {
            existingMessage.remove();
        }
        
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.innerHTML = `<span>✓</span> ${message}`;
        inputGroup.appendChild(successDiv);
    }

    // Clear validation state
    function clearValidation(input) {
        const inputGroup = input.closest('.input-group');
        inputGroup.classList.remove('error', 'success');
        const messages = inputGroup.querySelectorAll('.error-message, .success-message');
        messages.forEach(msg => msg.remove());
    }

    // Add email status indicator
    function addEmailStatusIndicator() {
        const inputGroup = emailInput.closest('.input-group');
        let statusIndicator = inputGroup.querySelector('.email-status');
        
        if (!statusIndicator) {
            statusIndicator = document.createElement('span');
            statusIndicator.className = 'email-status';
            inputGroup.appendChild(statusIndicator);
        }
        
        return statusIndicator;
    }

    // Show loading state
    function showLoading() {
        const authCard = document.querySelector('.auth-card');
        let loadingOverlay = authCard.querySelector('.loading-overlay');
        
        if (!loadingOverlay) {
            loadingOverlay = document.createElement('div');
            loadingOverlay.className = 'loading-overlay';
            loadingOverlay.innerHTML = '<div class="loading-spinner"></div>';
            authCard.appendChild(loadingOverlay);
        }
        
        loadingOverlay.classList.add('active');
    }

    // Hide loading state
    function hideLoading() {
        const loadingOverlay = document.querySelector('.loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.classList.remove('active');
        }
    }

    // Show success state
    function showSuccessState(resetUrl) {
        const authCard = document.querySelector('.auth-card');
        authCard.innerHTML = `
            <div class="success-state">
                <div class="icon">📧</div>
                <h3>Check Your Email</h3>
                <p>We've sent a password reset link to your email address. Please check your inbox and follow the instructions to reset your password.</p>
                <div class="form-info">
                    <span class="icon">💡</span>
                    <strong>Development Note:</strong> Since this is a development environment, here's your reset link: 
                    <a href="${resetUrl}" target="_blank">Reset Password</a>
                </div>
                <div class="security-note">
                    <span class="icon">🔒</span>
                    <strong>Security:</strong> This link will expire in 1 hour for your security.
                </div>
                <a href="/auth/login/" class="btn btn-primary btn-full">Back to Login</a>
            </div>
        `;
    }

    // Email validation on input
    emailInput.addEventListener('input', function() {
        clearValidation(this);
        const statusIndicator = addEmailStatusIndicator();
        
        if (this.value.trim()) {
            if (validateEmail(this.value)) {
                statusIndicator.className = 'email-status found';
                statusIndicator.textContent = '✓';
            } else {
                statusIndicator.className = 'email-status invalid';
                statusIndicator.textContent = '✗';
            }
        } else {
            statusIndicator.textContent = '';
            statusIndicator.className = 'email-status';
        }
    });

    // Email validation on blur
    emailInput.addEventListener('blur', function() {
        if (this.value.trim()) {
            if (validateEmail(this.value)) {
                showSuccess(this, 'Email format is valid');
            } else {
                showError(this, 'Please enter a valid email address');
            }
        }
    });

    // Form validation
    function validateForm() {
        let isValid = true;
        
        if (!emailInput.value.trim()) {
            showError(emailInput, 'Email address is required');
            isValid = false;
        } else if (!validateEmail(emailInput.value)) {
            showError(emailInput, 'Please enter a valid email address');
            isValid = false;
        }
        
        return isValid;
    }

    // Form submission
    forgotPasswordForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }
        
        showLoading();
        
        try {
            const formData = new FormData(forgotPasswordForm);
            const response = await fetch(forgotPasswordForm.action || window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            
            if (response.ok) {
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    const data = await response.json();
                    if (data.success) {
                        // Extract reset URL from message for development
                        const resetUrlMatch = data.message.match(/http[s]?:\/\/[^\s]+/);
                        const resetUrl = resetUrlMatch ? resetUrlMatch[0] : '#';
                        showSuccessState(resetUrl);
                    } else {
                        showError(emailInput, data.message || 'Failed to send reset email');
                    }
                } else {
                    window.location.reload();
                }
            } else {
                showError(emailInput, 'Failed to send reset email. Please try again.');
            }
        } catch (error) {
            console.error('Forgot password error:', error);
            showError(emailInput, 'An error occurred. Please try again.');
        } finally {
            hideLoading();
        }
    });

    // Auto-focus email input
    emailInput.focus();

    // Add info message
    const infoMessage = document.createElement('div');
    infoMessage.className = 'form-info';
    infoMessage.innerHTML = `
        <span class="icon">💡</span>
        Enter the email address associated with your account and we'll send you a link to reset your password.
    `;
    
    const authForm = document.querySelector('.auth-form');
    authForm.insertBefore(infoMessage, authForm.firstChild);
});
