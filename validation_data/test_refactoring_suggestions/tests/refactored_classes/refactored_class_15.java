interface Filter {
    void processFilter();
}

class CategoryFilter implements Filter {
    private String category;
    private String pattern;
    // Constructor and other methods

    public void processFilter() {
        // Implementation specific to CategoryFilter
    }
}

class SeverityFilter implements Filter {
    private String severity;
    private String pattern;
    // Constructor and other methods

    public void processFilter() {
        // Implementation specific to SeverityFilter
    }
}

class FilterFactory {
    public static Filter createFilter(String type, String pattern, String category, String severity, boolean enabled) {
        if (type.equalsIgnoreCase("category")) {
            return new CategoryFilter(pattern, category, enabled);
        } else if (type.equalsIgnoreCase("severity")) {
            return new SeverityFilter(pattern, severity, enabled);
        }
        // Add more filter types as needed
        throw new IllegalArgumentException("Invalid filter type: " + type);
    }
}
