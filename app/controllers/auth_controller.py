import logging
import re
from flask import flash, redirect, url_for, session, request
from app.models.user import User
from app import db

# Regex patterns for validation
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'


logger = logging.getLogger(__name__)

def register_user(username, email, password):
    """Register a new user"""
    logger.info(f"Attempting to register user: {username}")
    
    # Validate email format
    if not re.match(EMAIL_REGEX, email):
        logger.warning(f"Invalid email format: {email}")
        flash('Please enter a valid email address')
        return False
        
    # Validate password complexity
    if not re.match(PASSWORD_REGEX, password):
        logger.warning(f"Password does not meet complexity requirements")
        flash('Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character')
        return False
        
    if User.query.filter_by(username=username).first():
        logger.warning(f"Registration failed - username already exists: {username}")
        flash('Username already exists')
        return False
    if User.query.filter_by(email=email).first():
        logger.warning(f"Registration failed - email already exists: {email}")
        flash('Email already exists')
        return False
        
    new_user = User(username=username, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()
    logger.info(f"User registered successfully: {username}")
    return True

def login_user(username, password):
    """Login a user"""
    logger.info(f"Login attempt for user: {username}")
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        logger.info(f"Login successful for user: {username}")
        return True
    logger.warning(f"Login failed for user: {username}")
    return False

def logout_user():
    """Logout the current user"""
    user_id = session.get('user_id')
    logger.info(f"Logging out user ID: {user_id}")
    session.pop('user_id', None)
    session.pop('username', None)

def get_current_user():
    """Get the current logged in user"""
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        logger.debug(f"Retrieved current user: {user.username if user else None}")
        return user
    logger.debug("No user currently logged in")
    return None
