// Cache interface
interface Cache {
    void storeData(Object item);
    void clearCache();
    void updateStatistics(boolean isHit);
}

// Concrete cache implementations
class MemoryCache implements Cache {
    private int size;
    private int hitCount;
    private int missCount;
    private Object[] data;

    public MemoryCache(int size) {
        this.size = size;
        this.hitCount = 0;
        this.missCount = 0;
        this.data = new Object[size];
    }

    public void storeData(Object item) {
        data[size++] = item;
    }

    public void clearCache() {
        data = new Object[size];
        hitCount = 0;
        missCount = 0;
    }

    public void updateStatistics(boolean isHit) {
        if (isHit) hitCount++; else missCount++;
    }
}

class DiskCache implements Cache {
    // Implementation for disk cache
    public void storeData(Object item) { /* ... */ }
    public void clearCache() { /* ... */ }
    public void updateStatistics(boolean isHit) { /* ... */ }
}

class DistributedCache implements Cache {
    // Implementation for distributed cache
    public void storeData(Object item) { /* ... */ }
    public void clearCache() { /* ... */ }
    public void updateStatistics(boolean isHit) { /* ... */ }
}

// Cache factory
class CacheFactory {
    public static Cache createCache(String type, int size) {
        if (type.equalsIgnoreCase("memory")) {
            return new MemoryCache(size);
        } else if (type.equalsIgnoreCase("disk")) {
            return new DiskCache();
        } else if (type.equalsIgnoreCase("distributed")) {
            return new DistributedCache();
        }
        throw new IllegalArgumentException("Invalid cache type");
    }
}
