import pytest
from fastapi import HTTPException, status
from app.utils.exceptions import (
    ServiceError, 
    ValidationError, 
    NotFoundError, 
    ConflictError, 
    DatabaseError,
    service_exception_handler
)

def test_service_error():
    """Test ServiceError creation"""
    error = ServiceError("Test error message")
    assert error.message == "Test error message"
    assert error.error_code == "SERVICE_ERROR"
    assert error.details == {}

def test_service_error_with_details():
    """Test ServiceError creation with details"""
    error = ServiceError("Test error message", "TEST_ERROR", {"field": "value"})
    assert error.message == "Test error message"
    assert error.error_code == "TEST_ERROR"
    assert error.details == {"field": "value"}

def test_validation_error():
    """Test ValidationError creation"""
    error = ValidationError("Validation failed", "test_field")
    assert error.message == "Validation failed"
    assert error.error_code == "VALIDATION_ERROR"
    assert error.field == "test_field"

def test_not_found_error():
    """Test NotFoundError creation"""
    error = NotFoundError("User")
    assert error.message == "User未找到"
    assert error.error_code == "NOT_FOUND"
    assert error.resource == "User"

def test_not_found_error_with_id():
    """Test NotFoundError creation with resource ID"""
    error = NotFoundError("User", "123")
    assert error.message == "User未找到: 123"
    assert error.error_code == "NOT_FOUND"
    assert error.resource == "User"
    assert error.resource_id == "123"

def test_conflict_error():
    """Test ConflictError creation"""
    error = ConflictError("Resource conflict")
    assert error.message == "Resource conflict"
    assert error.error_code == "CONFLICT"

def test_database_error():
    """Test DatabaseError creation"""
    error = DatabaseError("Database error")
    assert error.message == "Database error"
    assert error.error_code == "DATABASE_ERROR"

def test_service_exception_handler_validation_error():
    """Test service exception handler with ValidationError"""
    error = ValidationError("Validation failed", "test_field")
    http_exception = service_exception_handler(error)
    
    assert isinstance(http_exception, HTTPException)
    assert http_exception.status_code == status.HTTP_400_BAD_REQUEST
    assert http_exception.detail["message"] == "Validation failed"
    assert http_exception.detail["error_code"] == "VALIDATION_ERROR"

def test_service_exception_handler_not_found_error():
    """Test service exception handler with NotFoundError"""
    error = NotFoundError("User", "123")
    http_exception = service_exception_handler(error)
    
    assert isinstance(http_exception, HTTPException)
    assert http_exception.status_code == status.HTTP_404_NOT_FOUND
    assert http_exception.detail["message"] == "User未找到: 123"
    assert http_exception.detail["error_code"] == "NOT_FOUND"

def test_service_exception_handler_conflict_error():
    """Test service exception handler with ConflictError"""
    error = ConflictError("Resource conflict")
    http_exception = service_exception_handler(error)
    
    assert isinstance(http_exception, HTTPException)
    assert http_exception.status_code == status.HTTP_409_CONFLICT
    assert http_exception.detail["message"] == "Resource conflict"
    assert http_exception.detail["error_code"] == "CONFLICT"

def test_service_exception_handler_database_error():
    """Test service exception handler with DatabaseError"""
    error = DatabaseError("Database error")
    http_exception = service_exception_handler(error)
    
    assert isinstance(http_exception, HTTPException)
    assert http_exception.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert http_exception.detail["message"] == "Database error"
    assert http_exception.detail["error_code"] == "DATABASE_ERROR"

def test_service_exception_handler_service_error():
    """Test service exception handler with generic ServiceError"""
    error = ServiceError("Generic error")
    http_exception = service_exception_handler(error)
    
    assert isinstance(http_exception, HTTPException)
    assert http_exception.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert http_exception.detail["message"] == "Generic error"
    assert http_exception.detail["error_code"] == "SERVICE_ERROR"