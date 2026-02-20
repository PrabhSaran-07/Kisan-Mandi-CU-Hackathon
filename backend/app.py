from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from models import db, User, Crop, Transaction, Price, ChatMessage
from config import Config
import os
import sys
import openai

# Get the frontend directory path
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')

# Initialize Flask app
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
app.config.from_object(Config)

# Initialize OpenAI API
openai.api_key = app.config['OPENAI_API_KEY']

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'  # type: ignore
CORS(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== DATABASE INITIALIZATION ====================
@app.cli.command()
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        print("Database initialized!")
        # Add default prices
        init_default_prices()

def init_default_prices():
    """Initialize demo prices"""
    demo_prices = [
        Price(crop_name='Wheat', location='Punjab', price=2200, source='demo'),
        Price(crop_name='Rice', location='Karnataka', price=3500, source='demo'),
        Price(crop_name='Cotton', location='Gujarat', price=5500, source='demo'),
        Price(crop_name='Sugarcane', location='Maharashtra', price=1800, source='demo'),
        Price(crop_name='Tomato', location='Himachal', price=4000, source='demo'),
    ]
    for price in demo_prices:
        if not Price.query.filter_by(crop_name=price.crop_name).first():
            db.session.add(price)
    db.session.commit()

# ==================== AUTHENTICATION ROUTES ====================
@app.route('/api/signup', methods=['POST'])
def signup():
    """User signup endpoint"""
    data = request.get_json()
    
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    user = User(  # type: ignore
        username=data.get('username'),  # type: ignore
        email=data.get('email'),  # type: ignore
        role=data.get('role', 'farmer'),  # type: ignore
        phone=data.get('phone'),  # type: ignore
        location=data.get('location')  # type: ignore
    )
    user.set_password(data.get('password'))
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully', 'user_id': user.id}), 201

@app.route('/api/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    
    if user and user.check_password(data.get('password')):
        login_user(user)
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    """User logout endpoint"""
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/user', methods=['GET'])
@login_required
def get_user():
    """Get current user info"""
    return jsonify(current_user.to_dict()), 200

# ==================== MARKETPLACE ROUTES ====================
@app.route('/api/crops', methods=['GET'])
def get_crops():
    """Get all available crops"""
    category = request.args.get('category')
    location = request.args.get('location')
    
    query = Crop.query.filter_by(status='available')
    
    if category:
        query = query.filter_by(category=category)
    if location:
        query = query.filter_by(location=location)
    
    crops = query.all()
    return jsonify([crop.to_dict() for crop in crops]), 200

@app.route('/api/crops/<int:crop_id>', methods=['GET'])
def get_crop(crop_id):
    """Get single crop details"""
    crop = Crop.query.get(crop_id)
    if not crop:
        return jsonify({'error': 'Crop not found'}), 404
    return jsonify(crop.to_dict()), 200

@app.route('/api/crops', methods=['POST'])
@login_required
def create_crop():
    """Farmer creates crop listing"""
    if current_user.role != 'farmer':
        return jsonify({'error': 'Only farmers can create listings'}), 403
    
    data = request.get_json()
    crop = Crop(
        farmer_id=current_user.id,
        crop_name=data.get('crop_name'),
        category=data.get('category'),
        quantity=data.get('quantity'),
        unit=data.get('unit', 'kg'),
        price_per_unit=data.get('price_per_unit'),
        description=data.get('description'),
        location=current_user.location
    )
    
    db.session.add(crop)
    db.session.commit()
    
    return jsonify({'message': 'Crop listed successfully', 'crop_id': crop.id}), 201

@app.route('/api/crops/<int:crop_id>', methods=['PUT'])
@login_required
def update_crop(crop_id):
    """Update crop listing"""
    crop = Crop.query.get(crop_id)
    if not crop or crop.farmer_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    crop.crop_name = data.get('crop_name', crop.crop_name)
    crop.quantity = data.get('quantity', crop.quantity)
    crop.price_per_unit = data.get('price_per_unit', crop.price_per_unit)
    crop.status = data.get('status', crop.status)
    
    db.session.commit()
    return jsonify({'message': 'Crop updated successfully'}), 200

@app.route('/api/crops/<int:crop_id>', methods=['DELETE'])
@login_required
def delete_crop(crop_id):
    """Delete crop listing"""
    crop = Crop.query.get(crop_id)
    if not crop or crop.farmer_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(crop)
    db.session.commit()
    return jsonify({'message': 'Crop deleted successfully'}), 200

# ==================== PRICING ROUTES ====================
@app.route('/api/prices', methods=['GET'])
def get_prices():
    """Get current crop prices"""
    prices = Price.query.order_by(Price.date.desc()).all()
    return jsonify([price.to_dict() for price in prices]), 200

# ==================== PAYMENT ROUTES ====================
@app.route('/api/transactions', methods=['POST'])
@login_required
def create_transaction():
    """Create new transaction/order"""
    data = request.get_json()
    
    crop = Crop.query.get(data.get('crop_id'))
    if not crop:
        return jsonify({'error': 'Crop not found'}), 404
    
    transaction = Transaction(
        buyer_id=current_user.id,
        crop_id=data.get('crop_id'),
        quantity=data.get('quantity'),
        total_price=data.get('quantity') * crop.price_per_unit,
        agreement_accepted=data.get('agreement_accepted', False)
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({
        'message': 'Transaction created',
        'transaction_id': transaction.id,
        'total_price': transaction.total_price
    }), 201

@app.route('/api/transactions/<int:transaction_id>', methods=['GET'])
@login_required
def get_transaction(transaction_id):
    """Get transaction details"""
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404
    return jsonify(transaction.to_dict()), 200

@app.route('/api/transactions/<int:transaction_id>/payment', methods=['POST'])
@login_required
def update_payment(transaction_id):
    """Update payment status"""
    data = request.get_json()
    transaction = Transaction.query.get(transaction_id)
    
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404
    
    transaction.payment_status = data.get('status', 'completed')
    transaction.payment_method = data.get('method', 'razorpay')
    transaction.razorpay_order_id = data.get('razorpay_order_id')
    
    if transaction.payment_status == 'completed':
        transaction.crop.quantity -= transaction.quantity
        if transaction.crop.quantity <= 0:
            transaction.crop.status = 'sold'
    
    db.session.commit()
    return jsonify({'message': 'Payment updated'}), 200

# ==================== AI & CHATBOT ROUTES ====================
@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    """AI Chatbot endpoint with OpenAI integration and fallback"""
    data = request.get_json()
    user_message = data.get('message')
    message_type = data.get('type', 'general')  # 'agronomy', 'marketplace', 'general'
    
    bot_response = None
    use_fallback = False
    
    # Try OpenAI API if configured
    if app.config['OPENAI_API_KEY']:
        try:
            # Create context-aware system prompt based on message type
            system_prompts = {
                'agronomy': 'You are an expert agricultural advisor for Indian farmers. Provide practical farming advice considering Indian climate and crops. Keep responses concise and actionable.',
                'marketplace': 'You are a helpful guide for an agricultural marketplace platform. Help users understand how to buy and sell crops, pricing, and platform features.',
                'general': 'You are a helpful agricultural assistant for farmers in India. You can answer questions about farming practices, crop prices, market trends, and our Kisan Mandi platform. Keep responses concise and practical.'
            }
            
            system_prompt = system_prompts.get(message_type, system_prompts['general'])
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Extract bot response from OpenAI response
            try:
                # Response should be a dict when using openai library
                response_dict = dict(response)  # type: ignore
                bot_response = response_dict['choices'][0]['message']['content'].strip()  # type: ignore
            except (KeyError, IndexError, TypeError, ValueError):
                try:
                    # Fallback: try direct access
                    bot_response = response['choices'][0]['message']['content'].strip()  # type: ignore
                except:
                    use_fallback = True
            
        except Exception as e:
            error_str = str(e)
            
            # Check if it's an authentication or quota error
            if 'quota' in error_str.lower() or 'exceeded' in error_str.lower() or 'rate' in error_str.lower():
                # Use intelligent fallback for quota/rate limit issues
                use_fallback = True
            elif 'Authentication' in error_str or 'unauthorized' in error_str or 'api_key' in error_str:
                bot_response = " Authentication error: Invalid OpenAI API key. Please check your configuration."
                return jsonify({
                    'user_message': user_message,
                    'bot_response': bot_response,
                    'error': True
                }), 401
            else:
                # Other errors
                use_fallback = True
    else:
        # No API key configured, use fallback
        use_fallback = True
    
    # Use intelligent fallback if OpenAI didn't work
    if bot_response is None or use_fallback:
        bot_response = get_intelligent_fallback_response(user_message, message_type)
    
    # Store chat message in database
    chat_msg = ChatMessage(
        user_id=current_user.id,
        user_message=user_message,
        bot_response=bot_response,
        message_type=message_type
    )
    db.session.add(chat_msg)
    db.session.commit()
    
    return jsonify({
        'user_message': user_message,
        'bot_response': bot_response
    }), 200

def get_intelligent_fallback_response(message, msg_type):
    """Intelligent fallback responses based on keywords"""
    message_lower = message.lower()
    
    # Keywords for selling crops
    if any(word in message_lower for word in ['sell', 'price', 'market', 'best time', 'when', 'weather']):
        weather_keywords = ['weather', 'rain', 'season', 'monsoon', 'summer', 'winter']
        price_keywords = ['price', 'rate', 'market', 'profit']
        
        if any(word in message_lower for word in weather_keywords) and any(word in message_lower for word in price_keywords):
            return " To decide when to sell your crop:\n\n1. **Monitor Weather**: Check monsoon timings, rainfall patterns, and temperature forecasts. Good harvest weather = better quality = higher prices.\n\n2. **Check Market Prices**: Use our Prices section to track commodity rates. Sell when prices are high.\n\n3. **Timing Strategy**: \n   - Wheat: Sell March-April for best prices\n   - Rice: Peak prices June-July\n   - Cotton: October-November highest demand\n   - Vegetables: Post-harvest season (high demand, seasonal gluts)\n\n4. **Use Kisan Mandi**: List your crops when prices are favorable and weather is stable.\n\nWould you like specific advice for a particular crop?"
        elif any(word in message_lower for word in weather_keywords):
            return " **Weather & Crop Selling**:\n\nGood weather conditions = Better crop quality = Higher market value\n\nCheck our Prices page to see current market rates and list your crops when conditions are optimal. Use the Marketplace to connect directly with buyers!"
        elif any(word in message_lower for word in price_keywords):
            return " **Getting Best Prices**:\n\n1. Visit our Prices page to check current market rates\n2. Harvest crops when market demand is high\n3. List on our marketplace with your best price\n4. Direct buyer connection = No middlemen cost\n\nWhat crop are you planning to sell?"
    
    # Keywords for farming/crops advice
    if any(word in message_lower for word in ['plant', 'grow', 'farm', 'crop', 'seed', 'soil', 'fertilizer']):
        return " **Farming & Crop Advice**:\n\nFor best results:\n\n1. **Soil Preparation**: Test soil pH before planting\n2. **Organic Methods**: Use natural fertilizers (compost, vermicompost)\n3. **Water Management**: Proper irrigation based on weather and crop type\n4. **Pest Control**: Use integrated pest management techniques\n5. **Timing**: Plant according to your region's crop season\n\nWhich crop would you like guidance on? (Wheat, Rice, Cotton, etc.)"
    
    # Keywords for marketplace/selling
    if any(word in message_lower for word in ['sell', 'list', 'buyer', 'marketplace', 'trade']):
        return " **Selling on Kisan Mandi Marketplace**:\n\n1. **Create Listing**: Add crop details, quantity, quality grade\n2. **Upload Photos**: Show your produce clearly\n3. **Set Your Price**: You control pricing - no middlemen\n4. **Connect with Buyers**: Buyers browse and contact directly\n5. **Payment**: Secure payment through our platform\n\nReady to list your crops? Go to Marketplace → Add New Listing!"
    
    # Keywords for prices
    if any(word in message_lower for word in ['price', 'rate', 'cost', 'expensive', 'cheap', 'rate']):
        return " **Current Market Prices**:\n\nVisit our Prices page to see live commodity rates for:\n- Wheat\n- Rice\n- Cotton\n- Sugarcane\n- Tomato\n- And more!\n\nPrices vary by location and season. Check regularly to time your sales optimally!"
    
    # General greeting
    return " I'm your Kisan Mandi Agricultural Advisor! I can help you with:\n\n **Selling Tips**: When & how to sell crops for best prices\n🌾 **Farming Advice**: Crop growing, soil care, pest management\n💰 **Market Prices**: Current rates for all crops\n🏪 **Marketplace Guide**: How to use our platform\n🌤️ **Weather Impact**: How weather affects crop price & quality\n\nWhat would you like to know?"

# ==================== STATIC ROUTES ====================
@app.route('/')
def index():
    """Serve login page"""
    return send_from_directory(FRONTEND_DIR, 'login.html')


@app.route('/dashboard.html')
@login_required
def dashboard():
    """Serve dashboard page"""
    return send_from_directory(FRONTEND_DIR, 'dashboard.html')

@app.route('/marketplace.html')
@login_required
def marketplace():
    """Serve marketplace page"""
    return send_from_directory(FRONTEND_DIR, 'marketplace.html')

@app.route('/advisor.html')
def advisor():
    """Serve advisor page"""
    return send_from_directory(FRONTEND_DIR, 'advisor.html')

@app.route('/chatbot.html')
def chatbot():
    """Serve chatbot page"""
    return send_from_directory(FRONTEND_DIR, 'chatbot.html')

@app.route('/prices.html')
def prices():
    """Serve prices page"""
    return send_from_directory(FRONTEND_DIR, 'prices.html')

@app.route('/payment.html')
def payment():
    """Serve payment page"""
    return send_from_directory(FRONTEND_DIR, 'payment.html')

# Serve static files (CSS, JS, etc)
@app.route('/css/<path:filename>')
def serve_css(filename):
    """Serve CSS files"""
    return send_from_directory(os.path.join(FRONTEND_DIR, 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    """Serve JavaScript files"""
    return send_from_directory(os.path.join(FRONTEND_DIR, 'js'), filename)

# Catch-all for any other static files (must be last route)
@app.route('/<path:filename>')
def serve_static(filename):
    """Serve any other static file"""
    filepath = os.path.join(FRONTEND_DIR, filename)
    if os.path.isfile(filepath):
        return send_from_directory(FRONTEND_DIR, filename)
    return jsonify({'error': 'File not found'}), 404

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Page not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Ensure demo price data exists on startup for local development
        try:
            init_default_prices()
        except Exception:
            # If DB already has data or migrations are not ready, ignore
            pass
    app.run(debug=True, host='0.0.0.0', port=5000)
