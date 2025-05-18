interface Logger {
    void log(String message);
}

class ConsoleLogger implements Logger {
    private String level;
    private String format;

    public ConsoleLogger(String level, String format) {
        this.level = level;
        this.format = format;
    }

    public void log(String message) {
        System.out.println(formatMessage(message));
    }

    private String formatMessage(String message) {
        return format + " " + level + " " + message;
    }
}

class FileLogger implements Logger {
    private String level;
    private String format;
    private String destination;

    public FileLogger(String level, String format, String destination) {
        this.level = level;
        this.format = format;
        this.destination = destination;
    }

    public void log(String message) {
        writeToFile(formatMessage(message));
    }

    private String formatMessage(String message) {
        return format + " " + level + " " + message;
    }

    private void writeToFile(String message) {
        // File writing logic here
    }
}

class DatabaseLogger implements Logger {
    private String level;
    private String format;

    public DatabaseLogger(String level, String format) {
        this.level = level;
        this.format = format;
    }

    public void log(String message) {
        saveToDatabase(formatMessage(message));
    }

    private String formatMessage(String message) {
        return format + " " + level + " " + message;
    }

    private void saveToDatabase(String message) {
        // Database saving logic here
    }
}

class LoggerFactory {
    public static Logger createLogger(String type, String level, String format, String destination) {
        if (type.equals("console")) {
            return new ConsoleLogger(level, format);
        } else if (type.equals("file")) {
            return new FileLogger(level, format, destination);
        } else if (type.equals("database")) {
            return new DatabaseLogger(level, format);
        }
        throw new IllegalArgumentException("Invalid logger type");
    }
}
