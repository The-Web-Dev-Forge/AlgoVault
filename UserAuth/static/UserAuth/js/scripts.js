document.addEventListener('DOMContentLoaded', function() {
    // Theme toggle functionality
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const themeToggleIcon = document.getElementById('theme-toggle-icon');
    
    // Check if user has previously set a theme preference
    const currentTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', currentTheme);
    
    // Update icon based on current theme
    if (currentTheme === 'light') {
        themeToggleIcon.classList.remove('fa-moon');
        themeToggleIcon.classList.add('fa-sun');
    }
    
    // Handle theme toggle click
    themeToggleBtn.addEventListener('click', function() {
        // Add transition class for smoother theme change
        document.body.classList.add('theme-transition');
        
        // Toggle theme
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Update icon
        if (newTheme === 'light') {
            themeToggleIcon.classList.remove('fa-moon');
            themeToggleIcon.classList.add('fa-sun');
        } else {
            themeToggleIcon.classList.remove('fa-sun');
            themeToggleIcon.classList.add('fa-moon');
        }
        
        // Remove transition class after theme change
        setTimeout(() => {
            document.body.classList.remove('theme-transition');
        }, 500);
    });
    
    // Password visibility toggle
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const passwordInput = this.previousElementSibling;
            const icon = this.querySelector('i');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });
    
    // Password strength meter
    const passwordInputs = document.querySelectorAll('input[type="password"]#password');
    
    passwordInputs.forEach(input => {
        input.addEventListener('input', function() {
            const password = this.value;
            const strengthValue = document.getElementById('strength-value');
            const strengthSegments = document.querySelectorAll('.strength-segment');
            
            if (!strengthValue || !strengthSegments.length) return;
            
            let strength = calculatePasswordStrength(password);
            
            // Update strength segments
            strengthSegments.forEach((segment, index) => {
                if (index < strength) {
                    segment.classList.add('active');
                } else {
                    segment.classList.remove('active');
                }
            });
            
            // Update strength text
            let strengthText;
            if (strength === 0) {
                strengthText = 'Very Weak';
            } else if (strength === 1) {
                strengthText = 'Weak';
            } else if (strength === 2) {
                strengthText = 'Medium';
            } else if (strength === 3) {
                strengthText = 'Strong';
            } else {
                strengthText = 'Very Strong';
            }
            
            strengthValue.textContent = strengthText;
        });
    });
    
    function calculatePasswordStrength(password) {
        if (!password) return 0;
        
        let strength = 0;
        
        // Length
        if (password.length >= 8) {
            strength += 1;
        }
        
        // Contains uppercase and lowercase
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) {
            strength += 1;
        }
        
        // Contains numbers
        if (/\d/.test(password)) {
            strength += 1;
        }
        
        // Contains special characters
        if (/[^a-zA-Z0-9]/.test(password)) {
            strength += 1;
        }
        
        return strength;
    }
    
    // Login form handling
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Validate inputs
            if (!email || !password) {
                showNotification('Please fill in all fields', 'error');
                e.preventDefault();
                return;
            }
            
            // Let the form submit naturally to Django backend
        });
    }
    
    // Signup form handling
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            const firstName = document.getElementById('first-name').value;
            const lastName = document.getElementById('last-name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm-password').value;
            const terms = document.getElementById('terms').checked;
            
            // Validate inputs
            if (!firstName || !lastName || !email || !password || !confirmPassword) {
                showNotification('Please fill in all fields', 'error');
                e.preventDefault();
                return;
            }
            
            if (password !== confirmPassword) {
                showNotification('Passwords do not match', 'error');
                e.preventDefault();
                return;
            }
            
            if (!terms) {
                showNotification('Please agree to the Terms of Service and Privacy Policy', 'error');
                e.preventDefault();
                return;
            }
            
            // Check password strength
            const strength = calculatePasswordStrength(password);
            if (strength < 2) {
                showNotification('Please choose a stronger password', 'error');
                e.preventDefault();
                return;
            }
            
            // Let the form submit naturally to Django backend
        });
    }
    
    // Forgot password form handling
    const requestResetBtn = document.getElementById('request-reset-btn');
    if (requestResetBtn) {
        requestResetBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            
            // Validate email
            if (!email) {
                showNotification('Please enter your email address', 'error');
                return;
            }
            
            // Submit the form to Django backend
            const form = document.getElementById('reset-request-form');
            if (form) {
                form.submit();
            }
        });
        
        // Resend button handling
        const resendBtn = document.getElementById('resend-btn');
        if (resendBtn) {
            resendBtn.addEventListener('click', function() {
                showNotification('Reset link has been resent to your email', 'success');
                const form = document.getElementById('reset-request-form');
                if (form) {
                    form.submit();
                }
            });
        }
    }
    
    // Reset password form handling
    const resetPasswordBtn = document.getElementById('reset-password-btn');
    if (resetPasswordBtn) {
        resetPasswordBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm-password').value;
            
            // Validate inputs
            if (!password || !confirmPassword) {
                showNotification('Please fill in all fields', 'error');
                return;
            }
            
            if (password !== confirmPassword) {
                showNotification('Passwords do not match', 'error');
                return;
            }
            
            // Check password strength
            const strength = calculatePasswordStrength(password);
            if (strength < 2) {
                showNotification('Please choose a stronger password', 'error');
                return;
            }
            
            // Submit the form to Django backend
            const form = document.getElementById('reset-password-form');
            if (form) {
                form.submit();
            }
        });
    }
    
    // Google Authentication Button
    const googleAuthBtns = document.querySelectorAll('.btn-google');
    googleAuthBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // In a real implementation, this would redirect to the Google OAuth flow
            // For this demo, we'll just show a notification
            showNotification('Redirecting to Google for authentication...', 'success');
            
            // Simulate the process
            setTimeout(() => {
                showNotification('Google authentication successful! Redirecting...', 'success');
                
                // Simulate redirect
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1500);
            }, 1500);
        });
    });
    
    // GitHub Authentication Button
    const githubAuthBtns = document.querySelectorAll('.btn-github');
    githubAuthBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // In a real implementation, this would redirect to the GitHub OAuth flow
            // For this demo, we'll just show a notification
            showNotification('Redirecting to GitHub for authentication...', 'success');
            
            // Simulate the process
            setTimeout(() => {
                showNotification('GitHub authentication successful! Redirecting...', 'success');
                
                // Simulate redirect
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1500);
            }, 1500);
        });
    });
    
    // Utility function to show notifications
    function showNotification(message, type) {
        const notification = document.getElementById('notification');
        notification.textContent = message;
        notification.className = 'notification ' + type;
        notification.style.display = 'block';
        
        // Hide notification after 5 seconds
        setTimeout(() => {
            notification.style.display = 'none';
        }, 5000);
    }
});
