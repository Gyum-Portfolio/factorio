// Interface for computers
interface Computer {
    String getRam();
    String getCpu();
    String getType();
    String getGraphicsCard();
    String getStorage();
    String getMotherboard();
    String getPowerSupply();
    String getCase();
}

// Concrete classes for different types of computers
class Laptop implements Computer {
    private String ram;
    private String cpu;
    private String graphicsCard;
    private String storage;
    private String motherboard;
    private String powerSupply;
    private String case_;

    public Laptop(String ram, String cpu, String graphicsCard, String storage, String motherboard, String powerSupply, String case_) {
        this.ram = ram;
        this.cpu = cpu;
        this.graphicsCard = graphicsCard;
        this.storage = storage;
        this.motherboard = motherboard;
        this.powerSupply = powerSupply;
        this.case_ = case_;
    }

    // Getters for computer components
    public String getRam() { return ram; }
    public String getCpu() { return cpu; }
    public String getType() { return "laptop"; }
    public String getGraphicsCard() { return graphicsCard; }
    public String getStorage() { return storage; }
    public String getMotherboard() { return motherboard; }
    public String getPowerSupply() { return powerSupply; }
    public String getCase() { return case_; }
}

// Other concrete classes for Desktop, Server, Gaming, and Workstation

// Factory class for creating computers
class ComputerFactory {
    public static Computer createComputer(String type, String ram, String cpu, String graphicsCard, String storage, String motherboard, String powerSupply, String case_) {
        if (type.equalsIgnoreCase("laptop")) {
            return new Laptop(ram, cpu, graphicsCard, storage, motherboard, powerSupply, case_);
        } else if (type.equalsIgnoreCase("desktop")) {
            // Create and return a Desktop instance
        } else if (type.equalsIgnoreCase("server")) {
            // Create and return a Server instance
        } else if (type.equalsIgnoreCase("gaming")) {
            // Create and return a Gaming instance
        } else if (type.equalsIgnoreCase("workstation")) {
            // Create and return a Workstation instance
        } else {
            throw new IllegalArgumentException("Invalid computer type");
        }
    }
}
