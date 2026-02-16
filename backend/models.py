from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for Farmer, Buyer, and Admin"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'farmer', 'buyer', 'admin'
    id_type = db.Column(db.String(50))  # 'aadhar', 'id_card'
    id_number = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    crops = db.relationship('Crop', backref='seller', lazy=True, foreign_keys='Crop.farmer_id')
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'phone': self.phone,
            'location': self.location
        }

class Crop(db.Model):
    """Crop/Product listing for marketplace"""
    __tablename__ = 'crops'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'cereal', 'spice', 'vegetable', etc
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), default='kg')
    price_per_unit = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    image_url = db.Column(db.String(255))
    status = db.Column(db.String(20), default='available')  # 'available', 'sold', 'pending'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    transactions = db.relationship('Transaction', backref='crop', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'crop_name': self.crop_name,
            'category': self.category,
            'quantity': self.quantity,
            'unit': self.unit,
            'price_per_unit': self.price_per_unit,
            'location': self.location,
            'status': self.status,
            'seller': self.seller.to_dict()
        }

class Transaction(db.Model):
    """Transaction/Purchase records"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), default='pending')  # 'pending', 'completed', 'failed'
    payment_method = db.Column(db.String(50))  # 'upi', 'razorpay', 'bank_transfer'
    razorpay_order_id = db.Column(db.String(100))
    delivery_status = db.Column(db.String(20), default='pending')  # 'pending', 'shipped', 'delivered'
    agreement_accepted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'crop': self.crop.to_dict(),
            'quantity': self.quantity,
            'total_price': self.total_price,
            'payment_status': self.payment_status,
            'delivery_status': self.delivery_status,
            'created_at': str(self.created_at)
        }

class Price(db.Model):
    """Real-time crop prices"""
    __tablename__ = 'prices'
    
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    price = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    source = db.Column(db.String(50))  # 'demo', 'agmarknet', 'data.gov'
    
    def to_dict(self):
        return {
            'crop_name': self.crop_name,
            'location': self.location,
            'price': self.price,
            'date': str(self.date)
        }

class ChatMessage(db.Model):
    """Store chat history with AI"""
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(50))  # 'agronomy', 'marketplace', 'general'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
