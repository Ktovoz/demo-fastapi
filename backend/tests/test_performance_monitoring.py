import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.performance import performance_monitor

@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)

def test_performance_monitoring_basic(client):
    """Test basic performance monitoring functionality"""
    # Make a few requests to generate performance data
    response = client.get("/health")
    assert response.status_code == 200
    
    response = client.get("/docs")
    assert response.status_code == 200
    
    # Check performance stats
    stats = performance_monitor.get_summary()
    assert stats is not None
    assert "total_requests" in stats
    assert "success_rate" in stats
    assert "avg_response_time" in stats
    
    # Check request stats
    request_stats = performance_monitor.get_request_stats()
    assert request_stats is not None
    
    # Check slow requests (should be empty since our requests are fast)
    slow_requests = performance_monitor.get_slow_requests(0.1)  # 100ms threshold
    assert isinstance(slow_requests, list)

def test_performance_monitoring_endpoints(client):
    """Test performance monitoring API endpoints"""
    # Make a request to generate some data
    response = client.get("/health")
    assert response.status_code == 200
    
    # Test performance stats endpoint
    response = client.get("/api/system/performance")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "data" in data
    assert "total_requests" in data["data"]
    
    # Test request stats endpoint
    response = client.get("/api/system/performance/requests")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "data" in data
    
    # Test slow requests endpoint
    response = client.get("/api/system/performance/slow")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "data" in data
    
    # Test reset endpoint
    response = client.delete("/api/system/performance/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True

def test_performance_monitoring_reset(client):
    """Test performance monitoring reset functionality"""
    # Make a request to generate some data
    response = client.get("/health")
    assert response.status_code == 200
    
    # Check that we have some data
    stats_before = performance_monitor.get_summary()
    assert stats_before["total_requests"] > 0
    
    # Reset stats
    performance_monitor.reset_stats()
    
    # Check that stats are reset
    stats_after = performance_monitor.get_summary()
    assert stats_after["total_requests"] == 0