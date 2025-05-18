interface Parser {
    String parse(String data);
}

class JSONParser implements Parser {
    public String parse(String data) {
        // Validate data
        // Process encoding
        return "Parsed JSON: " + data;
    }
}

class XMLParser implements Parser {
    public String parse(String data) {
        // Validate data
        // Process encoding
        return "Parsed XML: " + data;
    }
}

class CSVParser implements Parser {
    public String parse(String data) {
        // Validate data
        // Process encoding
        return "Parsed CSV: " + data;
    }
}

class YAMLParser implements Parser {
    public String parse(String data) {
        // Validate data
        // Process encoding
        return "Parsed YAML: " + data;
    }
}

class ParserFactory {
    private static final String[] SUPPORTED_FORMATS = {"JSON", "XML", "CSV", "YAML"};

    public static Parser createParser(String format) {
        for (String supportedFormat : SUPPORTED_FORMATS) {
            if (supportedFormat.equalsIgnoreCase(format)) {
                switch (supportedFormat.toUpperCase()) {
                    case "JSON":
                        return new JSONParser();
                    case "XML":
                        return new XMLParser();
                    case "CSV":
                        return new CSVParser();
                    case "YAML":
                        return new YAMLParser();
                    // Add more cases for other parser types
                }
            }
        }
        throw new IllegalArgumentException("Unsupported format: " + format);
    }
}
