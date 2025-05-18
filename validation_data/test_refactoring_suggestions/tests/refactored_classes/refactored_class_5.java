// Interface for database connections
interface DatabaseConnection {
    String getDriver();
    int getPort();
    void connect(String url, String username, String password);
    void disconnect();
    // Add other common methods as needed
}

// Concrete implementation for MySQL
class MySQLConnection implements DatabaseConnection {
    @Override
    public String getDriver() {
        return "com.mysql.jdbc.Driver";
    }

    @Override
    public int getPort() {
        return 3306;
    }

    @Override
    public void connect(String url, String username, String password) {
        // Implementation for connecting to MySQL
    }

    @Override
    public void disconnect() {
        // Implementation for disconnecting from MySQL
    }
}

// Concrete implementation for PostgreSQL
class PostgreSQLConnection implements DatabaseConnection {
    @Override
    public String getDriver() {
        return "org.postgresql.Driver";
    }

    @Override
    public int getPort() {
        return 5432;
    }

    @Override
    public void connect(String url, String username, String password) {
        // Implementation for connecting to PostgreSQL
    }

    @Override
    public void disconnect() {
        // Implementation for disconnecting from PostgreSQL
    }
}

// Concrete implementation for Oracle
class OracleConnection implements DatabaseConnection {
    @Override
    public String getDriver() {
        return "oracle.jdbc.driver.OracleDriver";
    }

    @Override
    public int getPort() {
        return 1521;
    }

    @Override
    public void connect(String url, String username, String password) {
        // Implementation for connecting to Oracle
    }

    @Override
    public void disconnect() {
        // Implementation for disconnecting from Oracle
    }
}

// Factory class for creating database connections
class DatabaseConnectionFactory {
    public static DatabaseConnection createConnection(String type) {
        switch (type) {
            case "MySQL":
                return new MySQLConnection();
            case "PostgreSQL":
                return new PostgreSQLConnection();
            case "Oracle":
                return new OracleConnection();
            default:
                throw new IllegalArgumentException("Invalid database type: " + type);
        }
    }
}

// Usage
public class Database {
    private DatabaseConnection connection;

    public Database(String url, String username, String type, String password) {
        connection = DatabaseConnectionFactory.createConnection(type);
        connection.connect(url, username, password);
        // Other initialization logic
    }

    // Other methods for interacting with the database
}
