// Reset Password JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    const resetPasswordForm = document.getElementById('resetPasswordForm');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');

    // Password strength checker
    function checkPasswordStrength(password) {
        let strength = 0;
        const checks = {
            length: password.length >= 8,
            lowercase: /[a-z]/.test(password),
            uppercase: /[A-Z]/.test(password),
            numbers: /\d/.test(password),
            special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
        };

        Object.values(checks).forEach(check => {
            if (check) strength++;
        });

        let level = 'weak';
        if (strength >= 5) level = 'strong';
        else if (strength >= 4) level = 'good';
        else if (strength >= 3) level = 'fair';

        return { level, checks, score: strength };
    }

    // Update password strength display
    function updatePasswordStrength() {
        const password = passwordInput.value;
        const strengthResult = checkPasswordStrength(password);
        const strengthFill = document.querySelector('.strength-fill');
        const strengthLevel = document.getElementById('strengthLevel');

        // Update strength bar
        strengthFill.className = `strength-fill ${strengthResult.level}`;
        strengthLevel.textContent = strengthResult.level.charAt(0).toUpperCase() + strengthResult.level.slice(1);
        strengthLevel.className = strengthResult.level;
    }

    // Update password match indicator
    function updatePasswordMatch() {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        
        let matchIndicator = document.querySelector('.password-match');
        
        if (confirmPassword && password) {
            if (!matchIndicator) {
                matchIndicator = document.createElement('div');
                matchIndicator.className = 'password-match';
                confirmPasswordInput.closest('.input-group').appendChild(matchIndicator);
            }
            
            if (password === confirmPassword) {
                matchIndicator.className = 'password-match match';
                matchIndicator.textContent = 'Passwords match';
            } else {
                matchIndicator.className = 'password-match no-match';
                matchIndicator.textContent = 'Passwords do not match';
            }
        } else if (matchIndicator) {
            matchIndicator.remove();
        }
    }

    // Show error message
    function showError(input, message) {
        const inputGroup = input.closest('.input-group');
        inputGroup.classList.remove('success');
        inputGroup.classList.add('error');
        
        const existingMessage = inputGroup.querySelector('.validation-feedback');
        if (existingMessage) {
            existingMessage.remove();
        }
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'validation-feedback invalid';
        errorDiv.textContent = message;
        inputGroup.appendChild(errorDiv);
    }

    // Show success message
    function showSuccess(input, message) {
        const inputGroup = input.closest('.input-group');
        inputGroup.classList.remove('error');
        inputGroup.classList.add('success');
        
        const existingMessage = inputGroup.querySelector('.validation-feedback');
        if (existingMessage) {
            existingMessage.remove();
        }
        
        const successDiv = document.createElement('div');
        successDiv.className = 'validation-feedback valid';
        successDiv.textContent = message;
        inputGroup.appendChild(successDiv);
    }

    // Clear validation state
    function clearValidation(input) {
        const inputGroup = input.closest('.input-group');
        inputGroup.classList.remove('error', 'success');
        const messages = inputGroup.querySelectorAll('.validation-feedback');
        messages.forEach(msg => msg.remove());
    }

    // Show success state after password reset
    function showSuccessState() {
        const authCard = document.querySelector('.auth-card');
        authCard.innerHTML = `
            <div class="form-success">
                <div class="icon">🎉</div>
                <h3>Password Reset Successful!</h3>
                <p>Your password has been successfully reset. You can now log in with your new password.</p>
                <a href="/auth/login/" class="btn btn-primary btn-full">Go to Login</a>
            </div>
        `;
    }

    // Form validation
    function validateForm() {
        let isValid = true;
        
        // Clear previous validations
        clearValidation(passwordInput);
        clearValidation(confirmPasswordInput);
        
        // Validate password strength
        const passwordStrength = checkPasswordStrength(passwordInput.value);
        if (!passwordInput.value) {
            showError(passwordInput, 'Password is required');
            isValid = false;
        } else if (passwordStrength.score < 3) {
            showError(passwordInput, 'Password is too weak. Please choose a stronger password.');
            isValid = false;
        } else {
            showSuccess(passwordInput, 'Password strength is good');
        }
        
        // Validate confirm password
        if (!confirmPasswordInput.value) {
            showError(confirmPasswordInput, 'Please confirm your password');
            isValid = false;
        } else if (passwordInput.value !== confirmPasswordInput.value) {
            showError(confirmPasswordInput, 'Passwords do not match');
            isValid = false;
        } else {
            showSuccess(confirmPasswordInput, 'Passwords match');
        }
        
        return isValid;
    }

    // Event listeners
    passwordInput.addEventListener('input', function() {
        updatePasswordStrength();
        updatePasswordMatch();
        
        if (this.value) {
            clearValidation(this);
        }
    });

    confirmPasswordInput.addEventListener('input', function() {
        updatePasswordMatch();
        
        if (this.value) {
            clearValidation(this);
        }
    });

    // Form submission
    resetPasswordForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }
        
        const submitButton = resetPasswordForm.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.innerHTML = '🔒 Resetting Password...';
        submitButton.disabled = true;
        
        try {
            const formData = new FormData(resetPasswordForm);
            const response = await fetch(resetPasswordForm.action || window.location.href, {
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
                        showSuccessState();
                    } else {
                        showMessage(data.message || 'Password reset failed', 'error');
                    }
                } else {
                    showSuccessState();
                }
            } else {
                showMessage('Password reset failed. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Reset password error:', error);
            showMessage('An error occurred. Please try again.', 'error');
        } finally {
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }
    });

    // Show message to user
    function showMessage(message, type) {
        const existingMessages = document.querySelectorAll('.temp-message');
        existingMessages.forEach(msg => msg.remove());
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `alert alert-${type} temp-message`;
        messageDiv.textContent = message;
        messageDiv.style.position = 'fixed';
        messageDiv.style.top = '20px';
        messageDiv.style.right = '20px';
        messageDiv.style.zIndex = '1000';
        messageDiv.style.maxWidth = '300px';
        
        document.body.appendChild(messageDiv);
        
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }

    // Add token expiry warning
    const tokenWarning = document.createElement('div');
    tokenWarning.className = 'token-warning';
    tokenWarning.innerHTML = `
        <span class="icon">⏰</span>
        <div>
            <strong>Security Notice:</strong> This password reset link will expire in 1 hour.
            Please reset your password promptly.
        </div>
    `;
    
    const authForm = document.querySelector('.auth-form');
    authForm.insertBefore(tokenWarning, authForm.firstChild);

    // Add security tips
    const securityTips = document.createElement('div');
    securityTips.className = 'security-tips';
    securityTips.innerHTML = `
        <h4><span>🔒</span> Security Tips</h4>
        <ul>
            <li>Use a unique password you haven't used elsewhere</li>
            <li>Include a mix of letters, numbers, and special characters</li>
            <li>Make it at least 8 characters long</li>
            <li>Avoid personal information like names or dates</li>
        </ul>
    `;
    
    authForm.appendChild(securityTips);

    // Auto-focus password input
    passwordInput.focus();

    // Enhanced class for JavaScript functionality
    document.body.classList.add('js-enhanced');
});

// Password toggle functionality
function togglePassword(inputId) {
    const passwordInput = document.getElementById(inputId);
    const toggleButton = passwordInput.nextElementSibling;
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleButton.textContent = '🙈';
    } else {
        passwordInput.type = 'password';
        toggleButton.textContent = '👁️';
    }
}
