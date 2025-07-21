// Signup JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signupForm');
    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const termsCheckbox = document.getElementById('terms');

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
        const strengthSegments = document.querySelectorAll('.strength-segment');
        const strengthValue = document.getElementById('strength-value');

        // Reset all segments
        strengthSegments.forEach(segment => {
            segment.classList.remove('active');
        });

        // Activate segments based on strength
        for (let i = 0; i < strengthResult.score && i < strengthSegments.length; i++) {
            strengthSegments[i].classList.add('active');
        }

        // Update strength text
        if (strengthValue) {
            strengthValue.textContent = strengthResult.level.charAt(0).toUpperCase() + strengthResult.level.slice(1);
            strengthValue.className = strengthResult.level;
        }

        // Show/hide password requirements
        updatePasswordRequirements(strengthResult.checks);
    }

    // Update password requirements display
    function updatePasswordRequirements(checks) {
        let requirementsDiv = document.querySelector('.password-requirements');
        
        if (!requirementsDiv && passwordInput.value) {
            requirementsDiv = document.createElement('div');
            requirementsDiv.className = 'password-requirements';
            requirementsDiv.innerHTML = `
                <h4>Password Requirements:</h4>
                <ul class="requirements-list">
                    <li id="req-length">At least 8 characters</li>
                    <li id="req-lowercase">One lowercase letter</li>
                    <li id="req-uppercase">One uppercase letter</li>
                    <li id="req-numbers">One number</li>
                    <li id="req-special">One special character</li>
                </ul>
            `;
            passwordInput.closest('.input-group').appendChild(requirementsDiv);
        }

        if (requirementsDiv) {
            document.getElementById('req-length').className = checks.length ? 'valid' : '';
            document.getElementById('req-lowercase').className = checks.lowercase ? 'valid' : '';
            document.getElementById('req-uppercase').className = checks.uppercase ? 'valid' : '';
            document.getElementById('req-numbers').className = checks.numbers ? 'valid' : '';
            document.getElementById('req-special').className = checks.special ? 'valid' : '';

            // Hide requirements if password is empty
            if (!passwordInput.value) {
                requirementsDiv.remove();
            }
        }
    }

    // Email validation
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Username validation
    function validateUsername(username) {
        return username.length >= 3 && /^[a-zA-Z0-9_]+$/.test(username);
    }

    // Show error message
    function showError(input, message) {
        const inputGroup = input.closest('.input-group');
        inputGroup.classList.remove('success');
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

    // Show success message
    function showSuccess(input, message = '') {
        const inputGroup = input.closest('.input-group');
        inputGroup.classList.remove('error');
        inputGroup.classList.add('success');
        
        // Remove existing messages
        const existingMessage = inputGroup.querySelector('.error-message, .success-message');
        if (existingMessage) {
            existingMessage.remove();
        }
        
        if (message) {
            const successDiv = document.createElement('div');
            successDiv.className = 'success-message';
            successDiv.innerHTML = `<span>✓</span> ${message}`;
            inputGroup.appendChild(successDiv);
        }
    }

    // Clear validation state
    function clearValidation(input) {
        const inputGroup = input.closest('.input-group');
        inputGroup.classList.remove('error', 'success');
        const messages = inputGroup.querySelectorAll('.error-message, .success-message');
        messages.forEach(msg => msg.remove());
    }

    // Form validation
    function validateForm() {
        let isValid = true;
        
        // Validate username
        if (!usernameInput.value.trim()) {
            showError(usernameInput, 'Username is required');
            isValid = false;
        } else if (!validateUsername(usernameInput.value)) {
            showError(usernameInput, 'Username must be at least 3 characters and contain only letters, numbers, and underscores');
            isValid = false;
        }
        
        // Validate email
        if (!emailInput.value.trim()) {
            showError(emailInput, 'Email is required');
            isValid = false;
        } else if (!validateEmail(emailInput.value)) {
            showError(emailInput, 'Please enter a valid email address');
            isValid = false;
        }
        
        // Validate password
        const passwordStrength = checkPasswordStrength(passwordInput.value);
        if (!passwordInput.value) {
            showError(passwordInput, 'Password is required');
            isValid = false;
        } else if (passwordStrength.score < 3) {
            showError(passwordInput, 'Password is too weak. Please choose a stronger password.');
            isValid = false;
        }
        
        // Validate confirm password
        if (!confirmPasswordInput.value) {
            showError(confirmPasswordInput, 'Please confirm your password');
            isValid = false;
        } else if (passwordInput.value !== confirmPasswordInput.value) {
            showError(confirmPasswordInput, 'Passwords do not match');
            isValid = false;
        }
        
        // Validate terms
        if (!termsCheckbox.checked) {
            showError(termsCheckbox, 'You must agree to the terms of service');
            isValid = false;
        }
        
        return isValid;
    }

    // Event listeners
    passwordInput.addEventListener('input', updatePasswordStrength);

    usernameInput.addEventListener('blur', function() {
        if (this.value.trim()) {
            if (validateUsername(this.value)) {
                showSuccess(this, 'Username looks good');
            } else {
                showError(this, 'Username must be at least 3 characters and contain only letters, numbers, and underscores');
            }
        }
    });

    emailInput.addEventListener('blur', function() {
        if (this.value.trim()) {
            if (validateEmail(this.value)) {
                showSuccess(this, 'Email format is valid');
            } else {
                showError(this, 'Please enter a valid email address');
            }
        }
    });

    confirmPasswordInput.addEventListener('input', function() {
        if (this.value && passwordInput.value) {
            if (this.value === passwordInput.value) {
                showSuccess(this, 'Passwords match');
            } else {
                showError(this, 'Passwords do not match');
            }
        }
    });

    // Form submission
    signupForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }
        
        const submitButton = signupForm.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Creating Account...';
        submitButton.disabled = true;
        
        try {
            const formData = new FormData(signupForm);
            const response = await fetch(signupForm.action || window.location.href, {
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
                        showMessage('Account created successfully! Redirecting to login...', 'success');
                        setTimeout(() => {
                            window.location.href = '/auth/login/';
                        }, 2000);
                    } else {
                        showMessage(data.message || 'Signup failed', 'error');
                    }
                } else {
                    window.location.reload();
                }
            } else {
                showMessage('Signup failed. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Signup error:', error);
            showMessage('An error occurred. Please try again.', 'error');
        } finally {
            submitButton.textContent = originalText;
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

    // Auto-focus first input
    usernameInput.focus();
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
