public class Computer {
    private String ram;
    private String cpu;
    private String type;
    private String gpu;
    private String storage;
    private String motherboard;
    private double price;
    private boolean isLaptop;
    private boolean isDesktop;
    private boolean isServer;
    private boolean isGaming;
    private int powerConsumption;
    private String coolingSystem;
    private String powerSupply;
    private String operatingSystem;
    private String networkCard;
    
    public Computer(String ram, String cpu, String type, String gpu, String storage, 
                   String motherboard, double price, boolean isLaptop, boolean isDesktop,
                   boolean isServer, boolean isGaming, int powerConsumption, 
                   String coolingSystem, String powerSupply, String operatingSystem,
                   String networkCard) {
        this.ram = ram;
        this.cpu = cpu;
        this.type = type;
        this.gpu = gpu;
        this.storage = storage;
        this.motherboard = motherboard;
        this.price = price;
        this.isLaptop = isLaptop;
        this.isDesktop = isDesktop; 
        this.isServer = isServer;
        this.isGaming = isGaming;
        this.powerConsumption = powerConsumption;
        this.coolingSystem = coolingSystem;
        this.powerSupply = powerSupply;
        this.operatingSystem = operatingSystem;
        this.networkCard = networkCard;
    }
    
    public void calculatePrice() {
        // Complex price calculation logic
    }
    
    public void setupOperatingSystem() {
        // OS installation logic
    }
    
    public void configureCooling() {
        // Cooling setup logic
    }
    
    public void runDiagnostics() {
        // Hardware testing logic
    }
    
    public void networkSetup() {
        // Network configuration logic  
    }
}
