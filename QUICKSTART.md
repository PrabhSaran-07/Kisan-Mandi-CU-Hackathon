#  Kisan Mandi - Quick Start Guide


Your complete Kisan Mandi project is ready. Here's how to get started:

---

##  Installation & Setup

### Step 1: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Setup Environment Variables

Edit `backend/.env` and add your API keys:

```
OPENAI_API_KEY=sk-your-actual-key-from-openai
RAZORPAY_KEY_ID=rzp_test_your_test_key
RAZORPAY_KEY_SECRET=your_test_secret_key
```

**Get your keys from:**
-  OpenAI: https://platform.openai.com/api-keys
-  Razorpay Test: https://dashboard.razorpay.com (Create test account)

### Step 3: Initialize Database

```bash
cd backend
python app.py init-db
```

### Step 4: Run Flask Backend (This Serves Everything!)

```bash
cd backend
python app.py
```

 Flask server will run at: **http://localhost:5000**

### Step 5: Open Website in Browser

Open your browser and go to:

```
http://localhost:5000
```

That's it! The Flask backend automatically serves:
- ✅ Frontend HTML files (login, dashboard, marketplace, etc.)
- ✅ Static assets (CSS, JavaScript)
- ✅ API endpoints for database operations

**No need for separate frontend server!**

---

##  Test Accounts

### Farmer Account
- **Username**: farmer1
- **Password**: Farmer@123
- **Role**: Farmer
- **Location**: Punjab

### Buyer Account
- **Username**: buyer1
- **Password**: Buyer@123
- **Role**: Buyer
- **Location**: Delhi

### Admin Account
- **Username**: admin1
- **Password**: Admin@123
- **Role**: Admin

**To create these test accounts:** Make sign-up requests via the frontend.

---



##  Project Structure

```
kisan-mandi/
├── backend/
│   ├── app.py              ← Flask main app
│   ├── models.py           ← Database models
│   ├── config.py           ← Configuration
│   ├── requirements.txt     ← Python dependencies
│   ├── .env                ← API keys (keep secret!)
│   └── kisan_mandi.db      ← SQLite database (auto-created)
│
├── frontend/
│   ├── login.html          ← Login/Signup
│   ├── dashboard.html      ← Main dashboard
│   ├── marketplace.html    ← Buy/Sell crops
│   ├── payment.html        ← Payment (Razorpay test)
│   ├── chatbot.html        ← AI Chatbot
│   ├── advisor.html        ← AI Agronomy Advisor
│   ├── prices.html         ← Real-time prices
│   ├── css/style.css       ← Styling
│   └── js/app.js           ← Utilities
│
└── database/
    └── kisan_mandi.db      ← Auto-created SQLite DB
```

---

##  API Endpoints

**Backend Base URL**: `http://localhost:5000/api`

### Authentication
- `POST /api/signup` - Register user
- `POST /api/login` - Login user
- `POST /api/logout` - Logout
- `GET /api/user` - Get current user

### Marketplace
- `GET /api/crops` - Get all crops
- `GET /api/crops/<id>` - Get crop details
- `POST /api/crops` - Create crop (Farmer only)
- `PUT /api/crops/<id>` - Update crop
- `DELETE /api/crops/<id>` - Delete crop

### Prices
- `GET /api/prices` - Get all crop prices

### Transactions
- `POST /api/transactions` - Create order
- `GET /api/transactions/<id>` - Get order details
- `POST /api/transactions/<id>/payment` - Update payment status

### AI
- `POST /api/chat` - Chat with AI (OpenAI or mock)

---

##  API Key Setup (Important!)

### OpenAI API Integration
1. Go to https://platform.openai.com/api-keys
2. Create API key
3. Add to `.env` file
4. The chatbot will use GPT to answer farming questions

### Razorpay Test Mode
1. Create account at https://razorpay.com
2. Get test keys from Dashboard → Settings → Api Keys
3. Use test card: `4111 1111 1111 1111`
4. Any future expiry and CVV will work

---

##  User Flow

### Farmer Flow
1. **Signup** as Farmer (provide location, phone)
2. **Dashboard** → List a new crop
3. **Marketplace** → See your & other crops
4. **Prices** → Check market prices
5. **AI Advisor** → Get farming tips

### Buyer Flow
1. **Signup** as Buyer
2. **Marketplace** → Browse & search crops
3. **Select crop** → Agree to terms
4. **Payment** → Use test Razorpay
5. **Order confirmation**

### Admin Flow
1. **Signup** as Admin
2. **Dashboard** → Manage users & transactions
3. **Monitor** platform statistics
4. **Manage** prices & disputes

---

##  Troubleshooting

### Port 5000 already in use?
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :5000   # Windows
```

### Database error?
```bash
cd backend
rm kisan_mandi.db        # Delete old DB
python app.py init-db    # Recreate
```

### CORS errors?
Flask-CORS is already configured. Ensure `credentials: 'include'` in fetch calls.

### OpenAI errors?
- Verify API key in `.env`
- Check your OpenAI account balance
- Fall back to mock responses if key invalid

---

##  Next Steps for Production

1. **Deploy Backend** → PythonAnywhere
   - Upload backend folder
   - Install dependencies
   - Create web app
   - Configure WSGI file

2. **Deploy Frontend** → Netlify/Vercel
   - Update API_BASE URL in JavaScript
   - Deploy static files

3. **Real Data Integration**
   - Connect data.gov.in API for real prices
   - Implement real Aadhar verification
   - Setup actual email notifications

4. **Multilingual Support**
   - Add Hindi translations
   - Use i18n library
   - Translate API responses

5. **Security**
   - Add HTTPS
   - Implement rate limiting
   - Add input sanitization
   - Secure password reset

---

##  Resources Used

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python Flask, SQLAlchemy ORM
- **Database**: SQLite (lightweight, perfect for MVP)
- **APIs**: OpenAI, Razorpay, data.gov.in
- **Hosting**: PythonAnywhere (Backend), Netlify/Vercel (Frontend)

---

##  Important Notes

1. **Never commit API keys** - Use `.env` file (added to .gitignore)
2. **Use Razorpay Test Mode** - Don't test with real money
3. **CORS enabled** - Frontend and backend can communicate
4. **Mock AI responses** - If OpenAI key not set, mock responses will be used
5. **Database is SQLite** - Runs independently, no server needed

---

## Timeline

- **Day 1**: ✅ Setup + Auth (1-2 hours)
- **Day 2**: ✅ Marketplace CRUD (2-3 hours)
- **Day 3**: ✅ Payments + AI Integration (2-3 hours)
- **Day 4**: ✅ Testing + Deployment (2-3 hours)

**Total**: ~8-10 hours of implementation

---

##  Need Help?

1. Check Flask error logs for backend issues
2. Check browser console (F12) for frontend issues
3. Verify API endpoints are accessible
4. Ensure all dependencies are installed
5. Check `.env` file has correct API keys

---

**Happy farming!  Good luck with your Kisan Mandi project!**

Last Updated: February 13, 2026
