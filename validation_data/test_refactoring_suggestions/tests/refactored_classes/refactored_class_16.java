interface Validator {
    boolean validate(String input);
}

class EmailValidator implements Validator {
    private String emailPattern;

    public EmailValidator(String emailPattern) {
        this.emailPattern = emailPattern;
    }

    public boolean validate(String input) {
        return input.matches(emailPattern);
    }
}

class LengthValidator implements Validator {
    private int minLength;
    private int maxLength;

    public LengthValidator(int minLength, int maxLength) {
        this.minLength = minLength;
        this.maxLength = maxLength;
    }

    public boolean validate(String input) {
        return input.length() >= minLength && input.length() <= maxLength;
    }
}

// Other validator implementations (RequiredValidator, DateValidator, NumberValidator, etc.)

class ValidatorFactory {
    public static Validator createValidator(String type, String rules) {
        switch (type) {
            case "email":
                return new EmailValidator(rules);
            case "length":
                String[] lengthRules = rules.split(",");
                int minLength = Integer.parseInt(lengthRules[0]);
                int maxLength = Integer.parseInt(lengthRules[1]);
                return new LengthValidator(minLength, maxLength);
            // Other validator creation logic
            default:
                return null;
        }
    }
}
