import pytest
from app.services.system_management_service import SystemManagementService
from app.models.operation_log import OperationLog
from app.utils.exceptions import ValidationError

def test_get_system_logs(test_db):
    """Test getting system logs"""
    # Create test logs
    for i in range(5):
        log = OperationLog(
            action=f"Test action {i}",
            resource=f"/test/{i}",
            ip_address="127.0.0.1"
        )
        test_db.add(log)
    
    test_db.commit()
    
    # Test getting system logs
    result = SystemManagementService.get_system_logs(test_db, page=1, page_size=10)
    
    assert result is not None
    assert "items" in result
    assert "total" in result
    assert result["total"] == 5

def test_get_system_logs_pagination(test_db):
    """Test getting system logs with pagination"""
    # Create test logs
    for i in range(15):
        log = OperationLog(
            action=f"Test action {i}",
            resource=f"/test/{i}",
            ip_address="127.0.0.1"
        )
        test_db.add(log)
    
    test_db.commit()
    
    # Test pagination
    result = SystemManagementService.get_system_logs(test_db, page=1, page_size=10)
    assert len(result["items"]) == 10
    assert result["total"] == 15
    
    result = SystemManagementService.get_system_logs(test_db, page=2, page_size=10)
    assert len(result["items"]) == 5
    assert result["total"] == 15

def test_get_system_logs_invalid_params(test_db):
    """Test getting system logs with invalid parameters"""
    with pytest.raises(ValidationError):
        SystemManagementService.get_system_logs(test_db, page=0, page_size=10)
    
    with pytest.raises(ValidationError):
        SystemManagementService.get_system_logs(test_db, page=1, page_size=0)
    
    with pytest.raises(ValidationError):
        SystemManagementService.get_system_logs(test_db, page=1, page_size=101)

def test_get_logs_summary(test_db):
    """Test getting logs summary"""
    # Create test logs
    for i in range(5):
        log = OperationLog(
            action=f"Test action {i}",
            resource=f"/test/{i}",
            ip_address="127.0.0.1"
        )
        test_db.add(log)
    
    test_db.commit()
    
    # Test getting logs summary
    result = SystemManagementService.get_logs_summary(test_db)
    
    assert result is not None
    assert "severity" in result
    assert "recent" in result
    assert "topModules" in result
    assert "total" in result
    assert "errorRatio" in result

def test_get_system_settings(test_db):
    """Test getting system settings"""
    result = SystemManagementService.get_system_settings()
    
    assert result is not None
    assert "appName" in result
    assert "language" in result
    assert "timezone" in result
    assert "theme" in result

def test_update_system_settings(test_db):
    """Test updating system settings"""
    settings_data = {
        "appName": "Test App",
        "language": "en",
        "timezone": "UTC",
        "theme": "dark"
    }
    
    result = SystemManagementService.update_system_settings(settings_data)
    
    assert result is not None
    assert result["appName"] == "Test App"
    assert result["language"] == "en"
    assert result["timezone"] == "UTC"
    assert result["theme"] == "dark"

def test_update_system_settings_missing_fields(test_db):
    """Test updating system settings with missing fields"""
    with pytest.raises(ValidationError):
        SystemManagementService.update_system_settings({
            "language": "en",
            "timezone": "UTC",
            "theme": "dark"
        })