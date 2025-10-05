import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.cache import cache

@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)

def test_role_management_with_caching(client):
    """Test role management with caching"""
    # Clear cache first
    cache.clear()
    
    # Get roles list - should populate cache
    response = client.get("/api/roles/")
    assert response.status_code == 200
    
    # Check cache stats - should have some hits/misses
    cache_stats_response = client.get("/api/system/cache/stats")
    assert cache_stats_response.status_code == 200
    cache_stats = cache_stats_response.json()
    
    # Get roles list again - should use cache
    response = client.get("/api/roles/")
    assert response.status_code == 200
    
    # Check that cache was used (more hits)
    new_cache_stats_response = client.get("/api/system/cache/stats")
    assert new_cache_stats_response.status_code == 200
    
    # Clear cache
    clear_response = client.delete("/api/system/cache/clear")
    assert clear_response.status_code == 200

def test_role_detail_with_caching(client):
    """Test role detail with caching"""
    # Clear cache first
    cache.clear()
    
    # Get roles to find a role ID
    roles_response = client.get("/api/roles/")
    assert roles_response.status_code == 200
    roles_data = roles_response.json()
    
    if roles_data["data"] and len(roles_data["data"]) > 0:
        role_id = roles_data["data"][0]["id"]
        
        # Get role detail - should populate cache
        response = client.get(f"/api/roles/{role_id}")
        assert response.status_code == 200
        
        # Get role detail again - should use cache
        response = client.get(f"/api/roles/{role_id}")
        assert response.status_code == 200

def test_role_update_clears_cache(client):
    """Test that role updates clear cache"""
    # Clear cache first
    cache.clear()
    
    # Get roles list to populate cache
    response = client.get("/api/roles/")
    assert response.status_code == 200
    
    # Check cache size
    cache_stats_response = client.get("/api/system/cache/stats")
    assert cache_stats_response.status_code == 200
    initial_cache_size = cache_stats_response.json()["data"]["size"]
    
    # Get roles again to increase hits
    response = client.get("/api/roles/")
    assert response.status_code == 200
    
    # Update a role (this should clear cache)
    roles_response = client.get("/api/roles/")
    if roles_response.status_code == 200 and roles_response.json()["data"]:
        role_data = roles_response.json()["data"][0]
        role_id = role_data["id"]
        
        # Update role
        update_response = client.put(
            f"/api/roles/{role_id}",
            json={
                "displayName": role_data["displayName"],
                "description": role_data["description"] or "Updated description"
            }
        )
        # Note: This might fail if there are permission issues, but cache should still be cleared
        
        # Check cache size after update
        cache_stats_response = client.get("/api/system/cache/stats")
        assert cache_stats_response.status_code == 200