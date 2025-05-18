public class Database {
    private String url;
    private String username;
    private String type;
    private String driver;
    private int port;
    private boolean isConnected;
    private String password;
    private int timeout;
    private int maxConnections;
    private boolean autoCommit;
    
    public Database(String url, String username, String type) {
        this.url = url;
        this.username = username;
        this.type = type;
        this.driver = determineDriver();
        this.port = determinePort();
        this.isConnected = false;
        this.password = "default";
        this.timeout = 30;
        this.maxConnections = 100;
        this.autoCommit = true;
    }
    
    private String determineDriver() {
        if (type.equals("MySQL")) {
            return "com.mysql.jdbc.Driver";
        } else if (type.equals("PostgreSQL")) {
            return "org.postgresql.Driver";
        } else if (type.equals("Oracle")) {
            return "oracle.jdbc.driver.OracleDriver";
        }
        return "unknown";
    }
    
    private int determinePort() {
        if (type.equals("MySQL")) {
            return 3306;
        } else if (type.equals("PostgreSQL")) {
            return 5432;
        } else if (type.equals("Oracle")) {
            return 1521;
        }
        return 0;
    }
}