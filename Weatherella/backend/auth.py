"""MongoDB authentication module with user registration and login."""
import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from pymongo import MongoClient
from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI')
if not MONGODB_URI:
    raise ValueError("MONGODB_URI not found in environment variables")

client = MongoClient(MONGODB_URI)
db = client.get_database()  # Uses the database specified in the URI
users_collection = db['users']

# JWT secret key
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def generate_token(user_id: str, email: str) -> str:
    """Generate a JWT token for a user."""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and verify a JWT token."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


def register_user(email: str, password: str, name: str = None) -> dict:
    """Register a new user."""
    # Check if user already exists
    if users_collection.find_one({'email': email}):
        raise ValueError("User with this email already exists")
    
    # Validate password length
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters long")
    
    # Create user document
    user_doc = {
        'email': email,
        'password': hash_password(password),
        'name': name or email.split('@')[0],
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    
    # Insert user
    result = users_collection.insert_one(user_doc)
    
    # Generate token
    token = generate_token(str(result.inserted_id), email)
    
    return {
        'user_id': str(result.inserted_id),
        'email': email,
        'name': user_doc['name'],
        'token': token
    }


def login_user(email: str, password: str) -> dict:
    """Login a user and return a token."""
    # Find user
    user = users_collection.find_one({'email': email})
    if not user:
        raise ValueError("Invalid email or password")
    
    # Verify password
    if not verify_password(password, user['password']):
        raise ValueError("Invalid email or password")
    
    # Generate token
    token = generate_token(str(user['_id']), email)
    
    return {
        'user_id': str(user['_id']),
        'email': user['email'],
        'name': user.get('name', email.split('@')[0]),
        'token': token
    }


def token_required(f):
    """Decorator to protect routes with JWT authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Decode token
            payload = decode_token(token)
            # Add user info to request context
            request.user = payload
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        
        return f(*args, **kwargs)
    
    return decorated


def get_user_by_id(user_id: str) -> dict:
    """Get user information by ID."""
    from bson.objectid import ObjectId
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    if not user:
        return None
    
    return {
        'user_id': str(user['_id']),
        'email': user['email'],
        'name': user.get('name', user['email'].split('@')[0]),
        'created_at': user.get('created_at')
    }
