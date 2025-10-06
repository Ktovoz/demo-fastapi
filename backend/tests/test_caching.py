import pytest
from app.utils.cache import cache, SimpleCache

def test_cache_basic_operations():
    """Test basic cache operations"""
    # Test set and get
    cache.set("test_key", "test_value")
    assert cache.get("test_key") == "test_value"
    
    # Test exists
    assert cache.exists("test_key") == True
    assert cache.exists("non_existent_key") == False
    
    # Test delete
    assert cache.delete("test_key") == True
    assert cache.get("test_key") is None
    assert cache.exists("test_key") == False

def test_cache_ttl():
    """Test cache TTL functionality"""
    # Set a value with TTL
    cache.set("ttl_key", "ttl_value", ttl=1)  # 1 second TTL
    
    # Check that it exists
    assert cache.exists("ttl_key") == True
    assert cache.get("ttl_key") == "ttl_value"
    
    # Check TTL remaining
    ttl_remaining = cache.ttl("ttl_key")
    assert ttl_remaining is not None
    assert ttl_remaining <= 1

def test_cache_expiration():
    """Test cache expiration"""
    # Set a value with very short TTL
    cache.set("exp_key", "exp_value", ttl=0.1)  # 100ms TTL
    
    # Wait for expiration
    import time
    time.sleep(0.11)
    
    # Check that it's expired
    assert cache.exists("exp_key") == False
    assert cache.get("exp_key") is None

def test_cache_stats():
    """Test cache statistics"""
    # Clear cache to start fresh
    cache.clear()
    
    # Get initial stats
    initial_stats = cache.stats()
    initial_hits = initial_stats["hits"]
    initial_misses = initial_stats["misses"]
    
    # Make some cache operations
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.get("key1")  # Hit
    cache.get("key3")  # Miss
    cache.get("key2")  # Hit
    cache.get("key4")  # Miss
    
    # Check stats
    stats = cache.stats()
    assert stats is not None
    assert "hits" in stats
    assert "misses" in stats
    assert "hit_rate" in stats
    assert stats["hits"] == initial_hits + 2
    assert stats["misses"] == initial_misses + 2
    assert stats["hit_rate"] == 0.5

def test_cache_size_limit():
    """Test cache size limit"""
    # Create a new cache with small size limit
    small_cache = SimpleCache(max_size=3)
    
    # Add more items than the limit
    for i in range(5):
        small_cache.set(f"key{i}", f"value{i}")
    
    # Check that cache size is limited
    assert len(small_cache.keys()) <= 3

def test_cache_decorator():
    """Test cache decorator"""
    call_count = 0
    
    @cache.cached(ttl=10)
    def expensive_function(x, y):
        nonlocal call_count
        call_count += 1
        return x + y
    
    # First call should execute the function
    result1 = expensive_function(1, 2)
    assert result1 == 3
    assert call_count == 1
    
    # Second call with same arguments should use cache
    result2 = expensive_function(1, 2)
    assert result2 == 3
    assert call_count == 1  # Should not increment
    
    # Call with different arguments should execute the function
    result3 = expensive_function(2, 3)
    assert result3 == 5
    assert call_count == 2