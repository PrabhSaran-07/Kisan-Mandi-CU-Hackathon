# Kisan Mandi - Digital Agricultural Marketplace

**3-4 Day Development Roadmap**

## Project Overview
A digital platform connecting farmers, buyers, and logistics providers with:
- AI-powered agronomy advisor
- Real-time crop prices
- Digital marketplace
- UPI/Razorpay payments
- Multilingual support

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **Database**: SQLite
- **Hosting**: PythonAnywhere
- **APIs**: OpenAI (Chatbot), Razorpay (Payments), data.gov.in (Prices)

## Project Structure
```
kisan-mandi/
├── frontend/
│   ├── index.html          (Landing/Dashboard)
│   ├── login.html          (Login/Signup)
│   ├── marketplace.html    (Buy/Sell crops)
│   ├── payment.html        (Payment flow)
│   ├── chatbot.html        (AI Chatbot)
│   ├── advisor.html        (Agronomy Advisor)
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── app.js
│       ├── chatbot.js
│       └── payment.js
├── backend/
│   ├── app.py              (Flask main)
│   ├── models.py           (Database models)
│   ├── routes.py           (API endpoints)
│   ├── config.py           (Configuration)
│   └── requirements.txt
├── database/
│   └── kisan_mandi.db      (SQLite database)
└── README.md
```


## API Integrations
1. **OpenAI API** - For AI Chatbot and Agronomy Advisor
2. **Razorpay** - For payments (test mode)
3. **data.gov.in** - For real-time crop prices (optional, can use mock data)

## Getting Started
1. Install backend dependencies: `pip install -r backend/requirements.txt`
2. Initialize database: `python backend/app.py init-db`
3. Run Flask server: `python backend/app.py`
4. Open `frontend/login.html` in browser

or run the following commands
 .\setup.ps1

open the website on your browser:- http://localhost:5000
