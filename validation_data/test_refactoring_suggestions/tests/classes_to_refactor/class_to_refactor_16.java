public class Validator {
    private String type;
    private String rules;
    private String emailPattern;
    private int minLength;
    private int maxLength;
    private boolean isRequired;
    private String dateFormat;
    private double minValue;
    private double maxValue;
    private String phoneFormat;
    private String customRegex;
    private boolean allowSpecialChars;
    private boolean allowNumbers;
    private boolean caseSensitive;
    
    public Validator(String type, String rules) {
        this.type = type;
        this.rules = rules;
        this.emailPattern = "^[A-Za-z0-9+_.-]+@(.+)$";
        this.minLength = 0;
        this.maxLength = 100;
        this.isRequired = false;
        this.dateFormat = "yyyy-MM-dd";
        this.minValue = 0.0;
        this.maxValue = 1000.0;
        this.phoneFormat = "\\d{10}";
        this.customRegex = "";
        this.allowSpecialChars = true;
        this.allowNumbers = true;
        this.caseSensitive = true;
    }
    
    public boolean validateEmail(String email) {
        return email.matches(emailPattern);
    }
    
    public boolean validateLength(String input) {
        return input.length() >= minLength && input.length() <= maxLength;
    }
    
    public boolean validateRequired(String input) {
        return isRequired && !input.isEmpty();
    }
    
    public boolean validateDate(String date) {
        return date.matches("\\d{4}-\\d{2}-\\d{2}");
    }
    
    public boolean validateNumber(double number) {
        return number >= minValue && number <= maxValue;
    }
    
    public boolean validatePhone(String phone) {
        return phone.matches(phoneFormat);
    }
    
    public boolean validateCustom(String input) {
        return input.matches(customRegex);
    }
    
    public boolean validateText(String text) {
        if (!allowSpecialChars && text.matches(".*[^a-zA-Z0-9 ].*")) {
            return false;
        }
        if (!allowNumbers && text.matches(".*\\d.*")) {
            return false;
        }
        if (!caseSensitive) {
            text = text.toLowerCase();
        }
        return true;
    }
}