import pytest
from app.services.role_management_service import RoleManagementService
from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.utils.exceptions import ValidationError, NotFoundError

def test_get_roles_list(test_db):
    """Test getting roles list"""
    # Create test roles
    admin_role = Role(name="admin", description="Administrator")
    user_role = Role(name="user", description="Regular user")
    
    test_db.add(admin_role)
    test_db.add(user_role)
    test_db.commit()
    
    # Test getting roles list
    result = RoleManagementService.get_roles_list(test_db)
    
    assert result is not None
    assert len(result) == 2
    
    role_names = [role["displayName"] for role in result]
    assert "admin" in role_names
    assert "user" in role_names

def test_get_role_detail(test_db):
    """Test getting role detail"""
    # Create a test role
    role = Role(name="admin", description="Administrator")
    test_db.add(role)
    test_db.commit()
    
    # Test getting role detail
    result = RoleManagementService.get_role_detail(test_db, f"ROLE-{role.id}")
    
    assert result is not None
    assert result["id"] == f"ROLE-{role.id}"
    assert result["displayName"] == "admin"
    assert result["description"] == "Administrator"

def test_get_role_detail_not_found(test_db):
    """Test getting non-existent role detail"""
    with pytest.raises(NotFoundError):
        RoleManagementService.get_role_detail(test_db, "ROLE-99999")

def test_update_role(test_db):
    """Test updating role"""
    # Create a test role
    role = Role(name="user", description="Regular user")
    test_db.add(role)
    test_db.commit()
    
    # Create test permissions
    perm1 = Permission(name="read", resource="data", action="read", description="Read permission")
    perm2 = Permission(name="write", resource="data", action="write", description="Write permission")
    test_db.add(perm1)
    test_db.add(perm2)
    test_db.commit()
    
    # Update role
    update_data = {
        "displayName": "admin",
        "description": "Administrator",
        "permissions": ["read", "write"]
    }
    
    result = RoleManagementService.update_role(test_db, f"ROLE-{role.id}", update_data)
    
    assert result is not None
    assert result["displayName"] == "admin"
    assert result["description"] == "Administrator"
    assert len(result["permissions"]) == 2

def test_update_role_not_found(test_db):
    """Test updating non-existent role"""
    with pytest.raises(NotFoundError):
        RoleManagementService.update_role(test_db, "ROLE-99999", {"displayName": "admin"})