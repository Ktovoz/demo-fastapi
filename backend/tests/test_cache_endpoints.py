import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.cache import cache

@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)

def test_cache_endpoints(client):
    """Test cache API endpoints"""
    # Add some data to cache
    cache.set("test_key", "test_value")
    cache.set("another_key", {"data": "value"})
    
    # Test cache stats endpoint
    response = client.get("/api/system/cache/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "data" in data
    assert "size" in data["data"]
    assert "hits" in data["data"]
    assert "misses" in data["data"]
    
    # Test cache clear endpoint
    response = client.delete("/api/system/cache/clear")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "data" in data
    assert "deleted" in data["data"]
    
    # Check that cache is cleared
    stats = cache.stats()
    assert stats["size"] == 0

def test_cache_operations(client):
    """Test cache operations through API"""
    # Clear cache first
    response = client.delete("/api/system/cache/clear")
    assert response.status_code == 200
    
    # Add some data directly to cache
    cache.set("api_test_key", "api_test_value", ttl=60)
    
    # Check stats
    response = client.get("/api/system/cache/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["size"] == 1
    
    # Clear cache through API
    response = client.delete("/api/system/cache/clear")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["deleted"] >= 1
    
    # Check that cache is cleared
    response = client.get("/api/system/cache/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["size"] == 0