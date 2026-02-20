// Common utility functions
function formatPrice(price) {
    return '₹' + parseFloat(price).toFixed(2);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-IN');
}

function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

// API helper functions
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include'
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(`http://localhost:5000/api${endpoint}`, options);
    return response.json();
}

// Alert helper
function showAlert(message, type = 'info', duration = 5000) {
    const alertDiv = document.getElementById('alertContainer');
    if (alertDiv) {
        alertDiv.innerHTML = `<div class="alert alert-${type} show">${message}</div>`;
        if (duration > 0) {
            setTimeout(() => {
                alertDiv.innerHTML = '';
            }, duration);
        }
    }
}

// Password strength validator
function validatePassword(password) {
    const minLength = 8;
    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecial = /[!@#$%^&*]/.test(password);

    return {
        isValid: password.length >= minLength && hasUppercase && hasLowercase && hasNumbers,
        strength: [
            password.length >= minLength ? 1 : 0,
            hasUppercase ? 1 : 0,
            hasLowercase ? 1 : 0,
            hasNumbers ? 1 : 0
        ].reduce((a, b) => a + b, 0)
    };
}

// Email validator
function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Phone validator
function isValidPhone(phone) {
    return /^[0-9]{10}$/.test(phone.replace(/[^\d]/g, ''));
}

// Capitalize string
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Local storage helpers
function saveToLocalStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
        console.error('localStorage error:', error);
    }
}

function getFromLocalStorage(key) {
    try {
        const value = localStorage.getItem(key);
        return value ? JSON.parse(value) : null;
    } catch (error) {
        console.error('localStorage error:', error);
        return null;
    }
}

// Modal helpers
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
    }
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
    }
}

// Close modal on background click
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('show');
    }
});

console.log('✅ Utilities loaded');  
