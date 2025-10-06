import pytest
from app.services.user_service import UserService, AuthService
from app.models.user import User
from app.core.security import get_password_hash
from app.utils.exceptions import ValidationError, NotFoundError

def test_get_user_by_username(test_db):
    """Test getting user by username"""
    # Create a test user
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash("password123"),
        full_name="Test User"
    )
    test_db.add(user)
    test_db.commit()
    
    # Test getting user by username
    result = UserService.get_user_by_username(test_db, "testuser")
    assert result is not None
    assert result.username == "testuser"
    assert result.email == "test@example.com"
    
    # Test getting non-existent user
    result = UserService.get_user_by_username(test_db, "nonexistent")
    assert result is None

def test_get_user_by_username_empty_username(test_db):
    """Test getting user with empty username"""
    with pytest.raises(ValidationError):
        UserService.get_user_by_username(test_db, "")

def test_get_user_by_email(test_db):
    """Test getting user by email"""
    # Create a test user
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash("password123"),
        full_name="Test User"
    )
    test_db.add(user)
    test_db.commit()
    
    # Test getting user by email
    result = UserService.get_user_by_email(test_db, "test@example.com")
    assert result is not None
    assert result.username == "testuser"
    assert result.email == "test@example.com"
    
    # Test getting non-existent user
    result = UserService.get_user_by_email(test_db, "nonexistent@example.com")
    assert result is None

def test_get_user_by_email_empty_email(test_db):
    """Test getting user with empty email"""
    with pytest.raises(ValidationError):
        UserService.get_user_by_email(test_db, "")

def test_get_user_by_email_invalid_email(test_db):
    """Test getting user with invalid email"""
    with pytest.raises(ValidationError):
        UserService.get_user_by_email(test_db, "invalid-email")

def test_create_user(test_db):
    """Test creating a user"""
    user = UserService.create_user(
        test_db, 
        "testuser", 
        "test@example.com", 
        "password123", 
        "Test User"
    )
    
    assert user is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"

def test_create_user_empty_fields(test_db):
    """Test creating a user with empty fields"""
    with pytest.raises(ValidationError):
        UserService.create_user(test_db, "", "test@example.com", "password123", "Test User")
    
    with pytest.raises(ValidationError):
        UserService.create_user(test_db, "testuser", "", "password123", "Test User")
    
    with pytest.raises(ValidationError):
        UserService.create_user(test_db, "testuser", "test@example.com", "", "Test User")

def test_create_user_invalid_email(test_db):
    """Test creating a user with invalid email"""
    with pytest.raises(ValidationError):
        UserService.create_user(test_db, "testuser", "invalid-email", "password123", "Test User")

def test_verify_user_credentials(test_db):
    """Test verifying user credentials"""
    # Create a test user
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash("password123"),
        full_name="Test User"
    )
    test_db.add(user)
    test_db.commit()
    
    # Test valid credentials
    result = AuthService.verify_user_credentials(test_db, "testuser", "password123")
    assert result is not None
    assert result.username == "testuser"
    
    # Test invalid password
    result = AuthService.verify_user_credentials(test_db, "testuser", "wrongpassword")
    assert result is None
    
    # Test non-existent user
    result = AuthService.verify_user_credentials(test_db, "nonexistent", "password123")
    assert result is None

def test_verify_user_credentials_empty_fields(test_db):
    """Test verifying user credentials with empty fields"""
    result = AuthService.verify_user_credentials(test_db, "", "password123")
    assert result is None
    
    result = AuthService.verify_user_credentials(test_db, "testuser", "")
    assert result is None

def test_verify_user_credentials_by_email(test_db):
    """Test verifying user credentials by email"""
    # Create a test user
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash("password123"),
        full_name="Test User"
    )
    test_db.add(user)
    test_db.commit()
    
    # Test valid credentials
    result = AuthService.verify_user_credentials_by_email(test_db, "test@example.com", "password123")
    assert result is not None
    assert result.email == "test@example.com"
    
    # Test invalid password
    result = AuthService.verify_user_credentials_by_email(test_db, "test@example.com", "wrongpassword")
    assert result is None
    
    # Test non-existent user
    result = AuthService.verify_user_credentials_by_email(test_db, "nonexistent@example.com", "password123")
    assert result is None

def test_verify_user_credentials_by_email_empty_fields(test_db):
    """Test verifying user credentials by email with empty fields"""
    result = AuthService.verify_user_credentials_by_email(test_db, "", "password123")
    assert result is None
    
    result = AuthService.verify_user_credentials_by_email(test_db, "test@example.com", "")
    assert result is None