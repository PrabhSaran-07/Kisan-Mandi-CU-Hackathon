// =========================
// Common utility functions
// =========================
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

// =========================
// API helper
// =========================
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include'
    };

    if (data) options.body = JSON.stringify(data);

    const response = await fetch(`http://localhost:5000/api${endpoint}`, options);
    return response.json();
}

// =========================
// Alert helper
// =========================
function showAlert(message, type = 'info', duration = 5000) {
    const alertDiv = document.getElementById('alertContainer');
    if (!alertDiv) return;

    alertDiv.innerHTML = `<div class="alert alert-${type} show">${message}</div>`;
    if (duration > 0) {
        setTimeout(() => alertDiv.innerHTML = '', duration);
    }
}

// =========================
// Validators
// =========================
function validatePassword(password) {
    const minLength = 8;
    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);

    return {
        isValid: password.length >= minLength && hasUppercase && hasLowercase && hasNumbers,
        strength: [
            password.length >= minLength,
            hasUppercase,
            hasLowercase,
            hasNumbers
        ].filter(Boolean).length
    };
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isValidPhone(phone) {
    return /^[0-9]{10}$/.test(phone.replace(/[^\d]/g, ''));
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// =========================
// Local storage helpers
// =========================
function saveToLocalStorage(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}

function getFromLocalStorage(key) {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : null;
}

// =========================
// Modal helpers
// =========================
function closeModal(modalId) {
    document.getElementById(modalId)?.classList.remove('show');
}

function openModal(modalId) {
    document.getElementById(modalId)?.classList.add('show');
}

document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('show');
    }
});

// ==================================================
//  CHATBOT LOGIC (THIS FIXES YOUR ISSUE)
// ==================================================

//  DEMO MARKET PRICE DATA (Hackathon-safe)
const marketPrices = {
    wheat: { price: 2350, unit: 'quintal', mandi: 'Punjab' },
    rice: { price: 3200, unit: 'quintal', mandi: 'Haryana' },
    maize: { price: 2100, unit: 'quintal', mandi: 'UP' },
    potato: { price: 1200, unit: 'quintal', mandi: 'West Bengal' }
};

// 🎯 Main chatbot handler
function getBotReply(message) {
    const text = message.toLowerCase();

    // Greetings
    if (["hi", "hello", "hey"].some(w => text.includes(w))) {
        return "Hello  I can help you with crop prices, farming advice, and selling crops.";
    }

    // Price queries
    if (text.includes("price")) {
        for (const crop in marketPrices) {
            if (text.includes(crop)) {
                const data = marketPrices[crop];
                return ` **${capitalize(crop)} Price**\n\n` +
                       ` Price: ₹${data.price}/${data.unit}\n` +
                       ` Mandi: ${data.mandi}\n` +
                       ` Updated: ${formatDate(new Date())}`;
            }
        }
        return " Please mention a crop name like *wheat*, *rice*, *maize*.";
    }

    // Harvest season
    if (text.includes("season") || text.includes("harvest")) {
        if (text.includes("wheat")) {
            return "🌾 **Wheat Harvest Season**\n\nBest time: **March – April** (Rabi crop)";
        }
        if (text.includes("rice")) {
            return "🌾 **Rice Harvest Season**\n\nBest time: **October – November** (Kharif crop)";
        }
        return "🌱 Tell me the crop name to suggest the best season.";
    }

    // Selling crops
    if (text.includes("sell")) {
        return " **How to Sell Crops on Kisan Mandi**\n\n1️⃣ List crop\n2️⃣ Set price\n3️⃣ Connect buyers\n4️⃣ Get paid securely";
    }

    // Fallback
    return " I didn't understand that. Try:\n• current wheat price\n• best season to harvest wheat";
}

// =========================
// Chat UI hook
// =========================
function handleChatMessage(userMessage) {
    const reply = getBotReply(userMessage);
    return reply;
}

console.log(' Utilities + Chatbot loaded');