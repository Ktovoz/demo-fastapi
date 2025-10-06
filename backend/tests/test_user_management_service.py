import pytest
from app.services.user_management_service import UserManagementService
from app.models.user import User
from app.core.security import get_password_hash
from app.utils.exceptions import ValidationError, NotFoundError

def test_create_user_management(test_db):
    """Test creating a user through user management service"""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    }
    
    result = UserManagementService.create_user(test_db, user_data)
    
    assert result is not None
    assert result["name"] == "Test User"
    assert result["email"] == "test@example.com"

def test_create_user_management_missing_fields(test_db):
    """Test creating a user with missing fields"""
    # Missing name
    with pytest.raises(ValidationError):
        UserManagementService.create_user(test_db, {
            "email": "test@example.com",
            "password": "password123"
        })
    
    # Missing email
    with pytest.raises(ValidationError):
        UserManagementService.create_user(test_db, {
            "name": "Test User",
            "password": "password123"
        })
    
    # Missing password
    with pytest.raises(ValidationError):
        UserManagementService.create_user(test_db, {
            "name": "Test User",
            "email": "test@example.com"
        })

def test_create_user_management_invalid_email(test_db):
    """Test creating a user with invalid email"""
    with pytest.raises(ValidationError):
        UserManagementService.create_user(test_db, {
            "name": "Test User",
            "email": "invalid-email",
            "password": "password123"
        })

def test_get_users_list(test_db):
    """Test getting users list"""
    # Create test users
    for i in range(5):
        user = User(
            username=f"user{i}",
            email=f"user{i}@example.com",
            password_hash=get_password_hash("password123"),
            full_name=f"User {i}"
        )
        test_db.add(user)
    
    test_db.commit()
    
    # Test getting users list
    result = UserManagementService.get_users_list(test_db, page=1, page_size=10)
    
    assert result is not None
    assert "items" in result
    assert "total" in result
    assert result["total"] == 5

def test_get_users_list_pagination(test_db):
    """Test getting users list with pagination"""
    # Create test users
    for i in range(15):
        user = User(
            username=f"user{i}",
            email=f"user{i}@example.com",
            password_hash=get_password_hash("password123"),
            full_name=f"User {i}"
        )
        test_db.add(user)
    
    test_db.commit()
    
    # Test pagination
    result = UserManagementService.get_users_list(test_db, page=1, page_size=10)
    assert len(result["items"]) == 10
    assert result["total"] == 15
    
    result = UserManagementService.get_users_list(test_db, page=2, page_size=10)
    assert len(result["items"]) == 5
    assert result["total"] == 15

def test_get_user_detail(test_db):
    """Test getting user detail"""
    # Create a test user
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash("password123"),
        full_name="Test User"
    )
    test_db.add(user)
    test_db.commit()
    
    # Test getting user detail
    result = UserManagementService.get_user_detail(test_db, f"USR-{user.id}")
    
    assert result is not None
    assert result["id"] == f"USR-{user.id}"
    assert result["name"] == "Test User"
    assert result["email"] == "test@example.com"

def test_get_user_detail_not_found(test_db):
    """Test getting non-existent user detail"""
    with pytest.raises(NotFoundError):
        UserManagementService.get_user_detail(test_db, "USR-99999")

def test_update_user(test_db):
    """Test updating user"""
    # Create a test user
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash("password123"),
        full_name="Test User"
    )
    test_db.add(user)
    test_db.commit()
    
    # Update user
    update_data = {
        "name": "Updated User",
        "email": "updated@example.com"
    }
    
    result = UserManagementService.update_user(test_db, f"USR-{user.id}", update_data)
    
    assert result is not None
    assert result["name"] == "Updated User"
    assert result["email"] == "updated@example.com"

def test_update_user_not_found(test_db):
    """Test updating non-existent user"""
    with pytest.raises(NotFoundError):
        UserManagementService.update_user(test_db, "USR-99999", {"name": "Updated User"})

def test_update_user_invalid_email(test_db):
    """Test updating user with invalid email"""
    # Create a test user
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash("password123"),
        full_name="Test User"
    )
    test_db.add(user)
    test_db.commit()
    
    with pytest.raises(ValidationError):
        UserManagementService.update_user(test_db, f"USR-{user.id}", {"email": "invalid-email"})

def test_delete_user(test_db):
    """Test deleting user"""
    # Create a test user
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash("password123"),
        full_name="Test User"
    )
    test_db.add(user)
    test_db.commit()
    
    # Delete user
    result = UserManagementService.delete_user(test_db, f"USR-{user.id}")
    
    assert result is not None
    assert result["deleted"] is True
    
    # Verify user is deleted
    deleted_user = test_db.query(User).filter(User.id == user.id).first()
    assert deleted_user is None

def test_delete_user_not_found(test_db):
    """Test deleting non-existent user"""
    with pytest.raises(NotFoundError):
        UserManagementService.delete_user(test_db, "USR-99999")