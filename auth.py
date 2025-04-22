import hashlib
import secrets
from database import User, get_database_session

def hash_password(password):
    """Hash a password for storing."""
    salt = secrets.token_hex(8)
    hashed = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    return f"{salt}${hashed}"

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt, hashed = stored_password.split('$')
    return hashed == hashlib.sha256(salt.encode() + provided_password.encode()).hexdigest()

def register_user(username, password):
    """Register a new user"""
    session = get_database_session()
    
    # Check if username already exists
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        session.close()
        return False, "Username already exists"
    
    # Create new user
    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password)
    
    session.add(new_user)
    session.commit()
    session.close()
    
    return True, "User registered successfully"

def authenticate_user(username, password):
    """Authenticate a user"""
    session = get_database_session()
    
    user = session.query(User).filter_by(username=username).first()
    if not user or not verify_password(user.password, password):
        session.close()
        return False, None
    
    session.close()
    return True, user.id