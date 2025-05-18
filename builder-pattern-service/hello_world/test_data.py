examples = [
    {
        "original_code": """
public class Computer {{
    private String ram;
    private String cpu;
    public Computer(String ram, String cpu) {{
        this.ram = ram;
        this.cpu = cpu;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Computer {{
    String getRam();
    String getCpu();
}}

class Desktop implements Computer {{
    private String ram;
    private String cpu;
    public Desktop(String ram, String cpu) {{
        this.ram = ram;
        this.cpu = cpu;
    }}
    public String getRam() {{ return ram; }}
    public String getCpu() {{ return cpu; }}
}}

class ComputerFactory {{
    public static Computer createComputer(String ram, String cpu) {{
        return new Desktop(ram, cpu);
    }}
}}"""
    },
    {
        "original_code": """
public class Vehicle {{
    private String type;
    private int wheels;
    public Vehicle(String type, int wheels) {{
        this.type = type;
        this.wheels = wheels;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Vehicle {{
    String getType();
    int getWheels();
}}

class Car implements Vehicle {{
    private String type;
    private int wheels;
    public Car(String type, int wheels) {{
        this.type = type;
        this.wheels = wheels;
    }}
    public String getType() {{ return type; }}
    public int getWheels() {{ return wheels; }}
}}

class VehicleFactory {{
    public static Vehicle createVehicle(String type, int wheels) {{
        return new Car(type, wheels);
    }}
}}"""
    },
    {
        "original_code": """
public class Animal {{
    private String species;
    private String sound;
    public Animal(String species, String sound) {{
        this.species = species;
        this.sound = sound;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Animal {{
    String getSpecies();
    String makeSound();
}}

class Dog implements Animal {{
    private String species;
    private String sound;
    public Dog(String species, String sound) {{
        this.species = species;
        this.sound = sound;
    }}
    public String getSpecies() {{ return species; }}
    public String makeSound() {{ return sound; }}
}}

class AnimalFactory {{
    public static Animal createAnimal(String species, String sound) {{
        return new Dog(species, sound);
    }}
}}"""
    },
    {
        "original_code": """
public class Shape {{
    private String type;
    private double area;
    public Shape(String type, double area) {{
        this.type = type;
        this.area = area;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Shape {{
    String getType();
    double calculateArea();
}}

class Circle implements Shape {{
    private String type;
    private double radius;
    public Circle(double radius) {{
        this.type = "Circle";
        this.radius = radius;
    }}
    public String getType() {{ return type; }}
    public double calculateArea() {{ return Math.PI * radius * radius; }}
}}

class ShapeFactory {{
    public static Shape createShape(String type, double dimension) {{
        if (type.equals("Circle")) return new Circle(dimension);
        return null;
    }}
}}"""
    },
    {
        "original_code": """
public class Database {{
    private String url;
    private String username;
    public Database(String url, String username) {{
        this.url = url;
        this.username = username;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Database {{
    void connect();
    void disconnect();
}}

class MySQLDatabase implements Database {{
    private String url;
    private String username;
    public MySQLDatabase(String url, String username) {{
        this.url = url;
        this.username = username;
    }}
    public void connect() {{}}
    public void disconnect() {{}}
}}

class DatabaseFactory {{
    public static Database createDatabase(String type, String url, String username) {{
        if (type.equals("MySQL")) return new MySQLDatabase(url, username);
        return null;
    }}
}}"""
    },
    {
        "original_code": """
public class Logger {{
    private String level;
    private String format;
    public Logger(String level, String format) {{
        this.level = level;
        this.format = format;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Logger {{
    void log(String message);
    String getLevel();
}}

class FileLogger implements Logger {{
    private String level;
    private String format;
    public FileLogger(String level, String format) {{
        this.level = level;
        this.format = format;
    }}
    public void log(String message) {{}}
    public String getLevel() {{ return level; }}
}}

class LoggerFactory {{
    public static Logger createLogger(String type, String level, String format) {{
        if (type.equals("File")) return new FileLogger(level, format);
        return null;
    }}
}}"""
    },
    {
        "original_code": """
public class Document {{
    private String type;
    private String content;
    public Document(String type, String content) {{
        this.type = type;
        this.content = content;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Document {{
    void save();
    String getContent();
}}

class PDFDocument implements Document {{
    private String type;
    private String content;
    public PDFDocument(String content) {{
        this.type = "PDF";
        this.content = content;
    }}
    public void save() {{}}
    public String getContent() {{ return content; }}
}}

class DocumentFactory {{
    public static Document createDocument(String type, String content) {{
        if (type.equals("PDF")) return new PDFDocument(content);
        return null;
    }}
}}"""
    },
    {
        "original_code": """
public class Connection {{
    private String protocol;
    private int timeout;
    public Connection(String protocol, int timeout) {{
        this.protocol = protocol;
        this.timeout = timeout;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Connection {{
    void open();
    void close();
}}

class TCPConnection implements Connection {{
    private String protocol;
    private int timeout;
    public TCPConnection(String protocol, int timeout) {{
        this.protocol = protocol;
        this.timeout = timeout;
    }}
    public void open() {{}}
    public void close() {{}}
}}

class ConnectionFactory {{
    public static Connection createConnection(String protocol, int timeout) {{
        return new TCPConnection(protocol, timeout);
    }}
}}"""
    },
    {
        "original_code": """
public class Payment {{
    private String method;
    private double amount;
    public Payment(String method, double amount) {{
        this.method = method;
        this.amount = amount;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Payment {{
    void process();
    double getAmount();
}}

class CreditCardPayment implements Payment {{
    private String method;
    private double amount;
    public CreditCardPayment(double amount) {{
        this.method = "Credit Card";
        this.amount = amount;
    }}
    public void process() {{}}
    public double getAmount() {{ return amount; }}
}}

class PaymentFactory {{
    public static Payment createPayment(String method, double amount) {{
        if (method.equals("Credit Card")) return new CreditCardPayment(amount);
        return null;
    }}
}}"""
    },
    {
        "original_code": """
public class Message {{
    private String type;
    private String content;
    public Message(String type, String content) {{
        this.type = type;
        this.content = content;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Message {{
    void send();
    String getContent();
}}

class EmailMessage implements Message {{
    private String type;
    private String content;
    public EmailMessage(String content) {{
        this.type = "Email";
        this.content = content;
    }}
    public void send() {{}}
    public String getContent() {{ return content; }}
}}

class MessageFactory {{
    public static Message createMessage(String type, String content) {{
        if (type.equals("Email")) return new EmailMessage(content);
        return null;
    }}
}}"""
    },
    {
        "original_code": """
public class Report {{
    private String format;
    private String data;
    public Report(String format, String data) {{
        this.format = format;
        this.data = data;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Report {{
    void generate();
    String getData();
}}

class PDFReport implements Report {{
    private String format;
    private String data;
    public PDFReport(String data) {{
        this.format = "PDF";
        this.data = data;
    }}
    public void generate() {{}}
    public String getData() {{ return data; }}
}}

class ReportFactory {{
    public static Report createReport(String format, String data) {{
        if (format.equals("PDF")) return new PDFReport(data);
        return null;
    }}
}}"""
    },
    {
        "original_code": """
public class Notification {{
    private String type;
    private String message;
    public Notification(String type, String message) {{
        this.type = type;
        this.message = message;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Notification {{
    void send();
    String getMessage();
}}

class PushNotification implements Notification {{
    private String type;
    private String message;
    public PushNotification(String message) {{
        this.type = "Push";
        this.message = message;
    }}
    public void send() {{}}
    public String getMessage() {{ return message; }}
}}

class NotificationFactory {{
    public static Notification createNotification(String type, String message) {{
        if (type.equals("Push")) return new PushNotification(message);
        return null;
    }}
}}"""
    },
    {
        "original_code": """
public class Product {{
    private String category;
    private double price;
    public Product(String category, double price) {{
        this.category = category;
        this.price = price;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Product {{
    double getPrice();
    String getCategory();
}}

class Electronics implements Product {{
    private String category;
    private double price;
    public Electronics(double price) {{
        this.category = "Electronics";
        this.price = price;
    }}
    public double getPrice() {{ return price; }}
    public String getCategory() {{ return category; }}
}}

class ProductFactory {{
    public static Product createProduct(String category, double price) {{
        if (category.equals("Electronics")) return new Electronics(price);
        return null;
    }}
}}"""
    },
    {
        "original_code": """
public class Cache {{
    private String type;
    private int size;
    public Cache(String type, int size) {{
        this.type = type;
        this.size = size;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Cache {{
    void store(String key, Object value);
    Object get(String key);
}}

class MemoryCache implements Cache {{
    private String type;
    private int size;
    public MemoryCache(int size) {{
        this.type = "Memory";
        this.size = size;
    }}
    public void store(String key, Object value) {{}}
    public Object get(String key) {{ return null; }}
}}

class CacheFactory {{
    public static Cache createCache(String type, int size) {{
        if (type.equals("Memory")) return new MemoryCache(size);
        return null;
    }}
}}"""
    },
    {
        "original_code": """
public class Filter {{
    private String type;
    private String pattern;
    public Filter(String type, String pattern) {{
        this.type = type;
        this.pattern = pattern;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Filter {{
    boolean apply(String input);
    String getPattern();
}}

class RegexFilter implements Filter {{
    private String type;
    private String pattern;
    public RegexFilter(String pattern) {{
        this.type = "Regex";
        this.pattern = pattern;
    }}
    public boolean apply(String input) {{ return input.matches(pattern); }}
    public String getPattern() {{ return pattern; }}
}}

class FilterFactory {{
    public static Filter createFilter(String type, String pattern) {{
        if (type.equals("Regex")) return new RegexFilter(pattern);
        return null;
    }}
}}"""
    },
    {
        "original_code": """
public class Validator {{
    private String type;
    private String rules;
    public Validator(String type, String rules) {{
        this.type = type;
        this.rules = rules;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Validator {{
    boolean validate(String input);
    String getRules();
}}

class EmailValidator implements Validator {{
    private String type;
    private String rules;
    public EmailValidator(String rules) {{
        this.type = "Email";
        this.rules = rules;
    }}
    public boolean validate(String input) {{ return input.contains("@"); }}
    public String getRules() {{ return rules; }}
}}

class ValidatorFactory {{
    public static Validator createValidator(String type, String rules) {{
        if (type.equals("Email")) return new EmailValidator(rules);
        return null;
    }}
}}"""
    },
    {
        "original_code": """
public class Parser {{
    private String format;
    private String data;
    public Parser(String format, String data) {{
        this.format = format;
        this.data = data;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Parser {{
    Object parse(String input);
    String getFormat();
}}

class JSONParser implements Parser {{
    private String format;
    private String data;
    public JSONParser(String data) {{
        this.format = "JSON";
        this.data = data;
    }}
    public Object parse(String input) {{ return null; }}
    public String getFormat() {{ return format; }}
}}

class ParserFactory {{
    public static Parser createParser(String format, String data) {{
        if (format.equals("JSON")) return new JSONParser(data);
        return null;
    }}
}}"""
    }
]