public class Parser {
    private String format;
    private String data;
    private String type;
    private String encoding;
    private int maxSize;
    private boolean isValid;
    private String[] supportedFormats = {"JSON", "XML", "CSV", "YAML"};
    private String[] validEncodings = {"UTF-8", "ASCII", "ISO-8859-1"};
    
    public Parser(String format, String data) {
        this.format = format;
        this.data = data;
        this.type = "default";
        this.encoding = "UTF-8";
        this.maxSize = 1000;
        this.isValid = false;
    }
    
    public String parseJSON() {
        validateData();
        checkFormat();
        processEncoding();
        return "Parsed JSON: " + data;
    }
    
    public String parseXML() {
        validateData();
        checkFormat();
        processEncoding();
        return "Parsed XML: " + data;
    }
    
    public String parseCSV() {
        validateData();
        checkFormat();
        processEncoding();
        return "Parsed CSV: " + data;
    }
    
    public String parseYAML() {
        validateData();
        checkFormat();
        processEncoding();
        return "Parsed YAML: " + data;
    }
    
    private void validateData() {
        isValid = data != null && data.length() <= maxSize;
    }
    
    private void checkFormat() {
        boolean found = false;
        for (String f : supportedFormats) {
            if (f.equals(format)) {
                found = true;
                break;
            }
        }
        isValid = isValid && found;
    }
    
    private void processEncoding() {
        boolean validEncoding = false;
        for (String enc : validEncodings) {
            if (enc.equals(encoding)) {
                validEncoding = true;
                break;
            }
        }
        isValid = isValid && validEncoding;
    }
}